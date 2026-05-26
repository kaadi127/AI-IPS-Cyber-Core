import time
import random
from scapy.all import IP, TCP, send


TARGET_IP = "127.0.0.1"
TARGET_PORT = 5000
PACKET_COUNT = 180 


FOREIGN_IPS = [
    "8.8.8.8",          # United States (Google DNS)
    "1.1.1.1",          # Australia (Cloudflare)
    "185.60.216.35",    # Ireland (Facebook Server)
    "202.175.4.1",      # Japan
    "103.204.168.1"     # India
]

def simulate_foreign_attack():
  
    spoofed_source_ip = random.choice(FOREIGN_IPS)
    
    print(f"[*] Simulating Attack from a foreign country...")
    print(f"[*] Spoofed Source IP: {spoofed_source_ip} -> Target: {TARGET_IP}:{TARGET_PORT}")
    print(f"[*] Sending {PACKET_COUNT} raw packets raw via Scapy... Please wait.")
    
    for _ in range(PACKET_COUNT):
     
        packet = IP(src=spoofed_source_ip, dst=TARGET_IP) / TCP(sport=random.randint(1024, 65535), dport=TARGET_PORT, flags="S")
       
        send(packet, verbose=False)
        time.sleep(0.001)

    print("[+] Attack simulation completed! Check your NIDS Web Dashboard.")

if __name__ == "__main__":
    simulate_foreign_attack()
