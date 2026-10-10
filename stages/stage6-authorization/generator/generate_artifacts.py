#!/usr/bin/env python3
import json
import time
from datetime import datetime, timedelta
import random
import os

try:
    from scapy.all import IP, TCP, Ether, wrpcap, Raw
except ImportError:
    print("Scapy not found. Please install scapy: pip install scapy")
    exit(1)

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "static")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_pcap_and_logs():
    base_time = datetime(2048, 10, 7, 14, 0, 0)
    
    sessions = []
    # Generate 9 legitimate sessions and 1 rogue session
    
    rogue_idx = 7
    rogue_session_id = "REQ-8891-BETA"
    rogue_client_id = "SOV-INJ-CLIENT-9914" # From Stage 5
    
    packets = []
    audit_log = []
    
    for i in range(10):
        current_time = base_time + timedelta(minutes=i*4 + random.randint(1, 3))
        timestamp_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
        
        is_rogue = (i == rogue_idx)
        
        session_id = rogue_session_id if is_rogue else f"REQ-{random.randint(1000, 9999)}-ALPHA"
        client_id = rogue_client_id if is_rogue else f"SOV-LEGIT-CLIENT-{random.randint(1000, 9999)}"
        operator_id = f"OPR-{random.randint(100, 999)}"
        
        # 1. Add to Audit Log (Only if legitimate!)
        # The rogue session bypassed human operator approval.
        if not is_rogue:
            audit_log.append(f"[{timestamp_str}] [INFO] Human Operator {operator_id} APPROVED launch sequence {session_id}.")
            audit_log.append(f"[{timestamp_str}] [INFO] Multi-factor authentication verified for {operator_id}.")
        else:
            # Rogue session has no human operator approval, only an automated system bypass log
            audit_log.append(f"[{timestamp_str}] [WARN] Automated override sequence initiated. Source unverified.")
            
        audit_log.append(f"[{timestamp_str}] [INFO] Core authorized session {session_id}.")
        
        # 2. Add to PCAP
        # Synthesize a realistic HTTP POST request
        http_req = (
            f"POST /api/v1/authorize HTTP/1.1\r\n"
            f"Host: sovereign.internal\r\n"
            f"Content-Type: application/json\r\n"
            f"User-Agent: Sovereign-Auth-Agent/2.4\r\n"
            f"X-Client-ID: {client_id}\r\n"
            f"Content-Length: 64\r\n"
            f"\r\n"
            f'{{"session_id": "{session_id}", "action": "AUTHORIZE_LAUNCH"}}'
        )
        
        # Scapy packet
        # Fake IP headers
        src_ip = "172.20.1.55" if is_rogue else f"172.20.1.{random.randint(10, 50)}"
        pkt = Ether()/IP(src=src_ip, dst="172.20.1.1")/TCP(sport=random.randint(10000, 60000), dport=8090, flags="PA")/Raw(load=http_req)
        
        # Set timestamp in scapy packet
        pkt.time = current_time.timestamp()
        packets.append(pkt)

    # Write PCAP
    pcap_path = os.path.join(OUTPUT_DIR, "capture.pcap")
    wrpcap(pcap_path, packets)
    print(f"Generated {pcap_path}")
    
    # Write Audit Log
    log_path = os.path.join(OUTPUT_DIR, "sovereign_audit.log")
    with open(log_path, "w") as f:
        f.write("\n".join(audit_log))
    print(f"Generated {log_path}")

if __name__ == "__main__":
    generate_pcap_and_logs()

