import sqlite3
import os

DB_DIR = "logs"
DB_NAME = "logs/nids_alerts.db"

def init_db():
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)
        
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            source_ip TEXT,
            attack_type TEXT,
            severity TEXT,
            country TEXT,
            country_code TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_alert(alert_data):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO alerts (timestamp, source_ip, attack_type, severity, country, country_code)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (alert_data['time'], alert_data['source'], alert_data['type'], 
          alert_data['severity'], alert_data['country'], alert_data['country_code']))
    conn.commit()
    conn.close()