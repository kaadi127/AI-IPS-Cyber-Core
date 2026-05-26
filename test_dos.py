import socket
import threading
import time
import random

TARGET_IP = "127.0.0.1"
TARGET_PORT = 5000
PACKET_COUNT = 250  # Threshold එක ඉක්මවා යාමට

# ටෙස්ට් කිරීමට විවිධ රටවල් වල සැබෑ IP ලිපින
FOREIGN_IPS = [
    "8.8.8.8",          # United States
    "1.1.1.1",          # Australia
    "185.60.216.35",    # Ireland
    "202.175.4.1",      # Japan
    "103.204.168.1"     # India
]

def send_packet(spoofed_ip):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.2)
        s.connect((TARGET_IP, TARGET_PORT))
        
        # HTTP Header එකක් හරහා NIDS එකට බොරු IP එකක් pass කිරීම (HTTP Spoofing Trick)
        custom_header = f"GET / HTTP/1.1\r\nHost: {TARGET_IP}\r\nX-Forwarded-For: {spoofed_ip}\r\n\r\n"
        s.sendall(custom_header.encode())
        s.close()
    except Exception:
        pass

def start_test():
    # අහඹු ලෙස රටක IP එකක් තෝරා ගැනීම
    chosen_ip = random.choice(FOREIGN_IPS)
    print(f"[*] Simulating Attack via Threat Intelligence...")
    print(f"[*] Selected Target IP: {chosen_ip}")
    print(f"[*] Sending {PACKET_COUNT} fast requests to trigger NIDS...")
    
    threads = []
    for _ in range(PACKET_COUNT):
        t = threading.Thread(target=send_packet, args=(chosen_ip,))
        threads.append(t)
        t.start()
        time.sleep(0.002)

    for t in threads:
        t.join()
        
    print("[+] Test completed! Check your Dashboard now.")

if __name__ == "__main__":
    start_test()