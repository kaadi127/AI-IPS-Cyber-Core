import time
import requests
import random
import sqlite3
import subprocess
import numpy as np
from collections import defaultdict
from sklearn.ensemble import IsolationForest

dos_tracker = defaultdict(list)
DB_PATH = "logs/nids_alerts.db"
TEST_FOREIGN_IPS = ["8.8.8.8", "1.1.1.1", "185.60.216.35", "202.175.4.1", "103.204.168.1"]

# 🧠 AI Core Engine Initialization
print("[🧠 AI Core] Training Isolation Forest Anomaly Detection Model with baseline traffic...")
# Generating synthetic normal networking traffic sequences (e.g., 5 to 45 packets per burst is normal)
baseline_normal_traffic = np.random.randint(5, 45, size=(200, 1))
ai_classifier = IsolationForest(contamination=0.03, random_state=42)
ai_classifier.fit(baseline_normal_traffic)
print("[🧠 AI Core] Machine Learning Predictive Engine Model online.")

def get_country_from_ip(ip_address):
    if ip_address.startswith("192.168.") or ip_address == "127.0.0.1":
        return "Local Network", "local"
    try:
        response = requests.get(f"http://ip-api.com/json/{ip_address}?fields=status,country,countryCode", timeout=2)
        if response.status_code == 200:
            res_data = response.json()
            if res_data.get("status") == "success":
                return res_data.get("country"), res_data.get("countryCode").lower()
    except Exception:
        pass
    return "Unknown", "un"

def block_ip_firewall(ip_address):
    try:
        rule_name = f"NIDS_BLOCK_{ip_address}"
        cmd = f'netsh advfirewall firewall add rule name="{rule_name}" dir=in action=block remoteip={ip_address}'
        subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"[🛡️ IPS Kernel] Automated Blocked Vector: {ip_address}")
    except Exception as e:
        print(f"[-] Firewall rule injection crash: {e}")

def save_alert_to_db(data):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO alerts (timestamp, source_ip, attack_type, severity, country, country_code, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (data['time'], data['source'], data['type'], data['severity'], data['country'], data['country_code'], data['status']))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[-] Log Sync Failure: {e}")

def process_packets(packet_queue, alert_callback):
    while True:
        if not packet_queue.empty():
            packet = packet_queue.get()
            src_ip = random.choice(TEST_FOREIGN_IPS)
            current_time = time.time()

            dos_tracker[src_ip].append(current_time)
            dos_tracker[src_ip] = [t for t in dos_tracker[src_ip] if current_time - t <= 1]
            
            packet_burst_density = len(dos_tracker[src_ip])

            # 🧠 AI Prediction Evaluation Execution
            current_input_matrix = np.array([[packet_burst_density]])
            ai_verdict = ai_classifier.predict(current_input_matrix)

            # Isolation forest tags outliers/anomalies as -1
            if ai_verdict[0] == -1:
                country, country_code = get_country_from_ip(src_ip)
                
               
                alert_data = {
                    "time": time.strftime('%Y-%m-%d %H:%M:%S'),
                    "source": src_ip,
                    "type": "DoS (Denial of Service)",  
                    "severity": "CRITICAL",
                    "country": country,
                    "country_code": country_code,
                    "status": "BLOCKED"
                }
                
                block_ip_firewall(src_ip)
                save_alert_to_db(alert_data)
                alert_callback(alert_data)
                dos_tracker[src_ip].clear()
