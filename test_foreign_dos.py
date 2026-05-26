import time
import random
from scapy.all import IP, TCP, send

# Target විස්තර (අපේ NIDS එක දිවෙන තැන)
TARGET_IP = "127.0.0.1"
TARGET_PORT = 5000
PACKET_COUNT = 180  # Threshold එක 150 නිසා 180ක් යැවීමෙන් ඇලර්ට් එක වැටේ

# ටෙස්ට් කිරීමට විවිධ රටවල් වල ප්‍රසිද්ධ IP ලිපින කිහිපයක්
FOREIGN_IPS = [
    "8.8.8.8",          # United States (Google DNS)
    "1.1.1.1",          # Australia (Cloudflare)
    "185.60.216.35",    # Ireland (Facebook Server)
    "202.175.4.1",      # Japan
    "103.204.168.1"     # India
]

def simulate_foreign_attack():
    # ලැයිස්තුවෙන් අහඹු ලෙස එක් විදේශීය IP එකක් තෝරා ගැනීම
    spoofed_source_ip = random.choice(FOREIGN_IPS)
    
    print(f"[*] Simulating Attack from a foreign country...")
    print(f"[*] Spoofed Source IP: {spoofed_source_ip} -> Target: {TARGET_IP}:{TARGET_PORT}")
    print(f"[*] Sending {PACKET_COUNT} raw packets raw via Scapy... Please wait.")
    
    # Scapy මඟින් IP එක වෙනස් කර (Spoof) එකවර පැකට් විශාල ප්‍රමාණයක් යැවීම
    for _ in range(PACKET_COUNT):
        # Raw Network Packet එකක් නිර්මාණය කිරීම
        packet = IP(src=spoofed_source_ip, dst=TARGET_IP) / TCP(sport=random.randint(1024, 65535), dport=TARGET_PORT, flags="S")
        # පැකට් එක නෙට්වර්ක් එකට මුදා හැරීම (verbose=False මඟින් console එක පිරිසිදුව තබා ගනී)
        send(packet, verbose=False)
        time.sleep(0.001)

    print("[+] Attack simulation completed! Check your NIDS Web Dashboard.")

if __name__ == "__main__":
    simulate_foreign_attack()