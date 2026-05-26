import threading
from queue import Queue
from scapy.all import sniff, IP

packet_queue = Queue()

def packet_callback(packet):
    if IP in packet:
        packet_queue.put(packet)

def start_sniffing(interface):
    print(f"[*] Sniffer started on interface: {interface}")
    sniff(iface=interface, prn=packet_callback, store=False)

def launch_sniffer(interface):
    sniffer_thread = threading.Thread(target=start_sniffing, args=(interface,))
    sniffer_thread.daemon = True
    sniffer_thread.start()