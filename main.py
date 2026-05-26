import threading
import sys
import os
from sniffer import launch_sniffer, packet_queue
from detector import process_packets
from logger import init_db, log_alert
from dashboard import app, socketio, send_live_alert
from colorama import init, Fore

init(autoreset=True)

def on_alert_detected(alert_data):
    print(Fore.RED + f"[⚠️ ALERT] {alert_data['type']} detected from {alert_data['source']} ({alert_data['country']})")
    log_alert(alert_data)
    send_live_alert(alert_data)

if __name__ == '__main__':
    print(Fore.CYAN + "==================================================")
    print(Fore.CYAN + "      STARTING ADVANCED NIDS WITH ANALYTICS       ")
    print(Fore.CYAN + "==================================================")

    init_db()

    SELECTED_INTERFACE = "Wi-Fi" 
    launch_sniffer(interface=SELECTED_INTERFACE)

    detector_thread = threading.Thread(target=process_packets, args=(packet_queue, on_alert_detected))
    detector_thread.daemon = True
    detector_thread.start()

    print(Fore.GREEN + "[*] Dashboard Web UI is running on http://127.0.0.1:5000")
    try:
        socketio.run(app, host="127.0.0.1", port=5000, debug=False, allow_unsafe_werkzeug=True)
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n[-] Shutting down NIDS Core...")
        sys.exit(0)