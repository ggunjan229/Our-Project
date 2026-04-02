import requests
import random
import time
import json

API = "http://localhost:5000/api/predict"

# ── ATTACK PROFILES ──
# Each profile mimics real network flow features of that attack type

ATTACK_PROFILES = {

    "DoS Hulk": {
        "Flow Duration": random.randint(1000, 5000),
        "Total Fwd Packets": random.randint(500, 2000),
        "Total Backward Packets": random.randint(0, 10),
        "Flow Bytes/s": random.uniform(900000, 2000000),
        "Flow Packets/s": random.uniform(50000, 200000),
        "Flow IAT Mean": random.uniform(10, 100),
        "Fwd IAT Total": random.uniform(100, 500),
        "Bwd IAT Total": 0,
        "Fwd PSH Flags": 0,
        "Bwd PSH Flags": 0,
        "Fwd Header Length": random.randint(200, 800),
        "Bwd Header Length": 0,
        "Fwd Packets/s": random.uniform(40000, 180000),
        "Bwd Packets/s": 0,
        "Packet Length Min": 0,
        "Packet Length Max": random.randint(1400, 1500),
        "Packet Length Mean": random.uniform(700, 1400),
        "Packet Length Std": random.uniform(400, 700),
        "Packet Length Variance": random.uniform(160000, 490000),
        "FIN Flag Count": 0,
        "SYN Flag Count": 0,
        "RST Flag Count": 0,
        "PSH Flag Count": 0,
        "ACK Flag Count": random.randint(400, 2000),
        "URG Flag Count": 0,
        "CWE Flag Count": 0,
        "ECE Flag Count": 0,
        "Down/Up Ratio": 0,
        "Average Packet Size": random.uniform(700, 1400),
        "Avg Fwd Segment Size": random.uniform(700, 1400),
        "Avg Bwd Segment Size": 0,
        "Fwd Avg Bytes/Bulk": 0,
        "Fwd Avg Packets/Bulk": 0,
        "Fwd Avg Bulk Rate": 0,
        "Bwd Avg Bytes/Bulk": 0,
        "Bwd Avg Packets/Bulk": 0,
        "Bwd Avg Bulk Rate": 0,
        "Subflow Fwd Packets": random.randint(500, 2000),
        "Subflow Fwd Bytes": random.randint(500000, 2000000),
        "Subflow Bwd Packets": 0,
        "Subflow Bwd Bytes": 0,
        "Init_Win_bytes_forward": random.randint(64240, 65535),
        "Init_Win_bytes_backward": random.randint(-1, 0),
        "act_data_pkt_fwd": random.randint(400, 1800),
        "min_seg_size_forward": 20,
        "Active Mean": 0,
        "Active Std": 0,
        "Active Max": 0,
        "Active Min": 0,
        "Idle Mean": 0,
        "Idle Std": 0,
        "Idle Max": 0,
        "Idle Min": 0,
    },

    "PortScan": {
        "Flow Duration": random.randint(0, 100),
        "Total Fwd Packets": 1,
        "Total Backward Packets": 0,
        "Flow Bytes/s": random.uniform(0, 1000),
        "Flow Packets/s": random.uniform(10000, 100000),
        "Flow IAT Mean": random.uniform(0, 100),
        "Fwd IAT Total": 0,
        "Bwd IAT Total": 0,
        "Fwd PSH Flags": 0,
        "Bwd PSH Flags": 0,
        "Fwd Header Length": 20,
        "Bwd Header Length": 0,
        "Fwd Packets/s": random.uniform(10000, 100000),
        "Bwd Packets/s": 0,
        "Packet Length Min": 0,
        "Packet Length Max": 0,
        "Packet Length Mean": 0,
        "Packet Length Std": 0,
        "Packet Length Variance": 0,
        "FIN Flag Count": 0,
        "SYN Flag Count": 1,
        "RST Flag Count": 0,
        "PSH Flag Count": 0,
        "ACK Flag Count": 0,
        "URG Flag Count": 0,
        "CWE Flag Count": 0,
        "ECE Flag Count": 0,
        "Down/Up Ratio": 0,
        "Average Packet Size": 0,
        "Avg Fwd Segment Size": 0,
        "Avg Bwd Segment Size": 0,
        "Fwd Avg Bytes/Bulk": 0,
        "Fwd Avg Packets/Bulk": 0,
        "Fwd Avg Bulk Rate": 0,
        "Bwd Avg Bytes/Bulk": 0,
        "Bwd Avg Packets/Bulk": 0,
        "Bwd Avg Bulk Rate": 0,
        "Subflow Fwd Packets": 1,
        "Subflow Fwd Bytes": 0,
        "Subflow Bwd Packets": 0,
        "Subflow Bwd Bytes": 0,
        "Init_Win_bytes_forward": random.randint(1024, 8192),
        "Init_Win_bytes_backward": -1,
        "act_data_pkt_fwd": 0,
        "min_seg_size_forward": 20,
        "Active Mean": 0,
        "Active Std": 0,
        "Active Max": 0,
        "Active Min": 0,
        "Idle Mean": 0,
        "Idle Std": 0,
        "Idle Max": 0,
        "Idle Min": 0,
    },

    "DDoS": {
        "Flow Duration": random.randint(500, 3000),
        "Total Fwd Packets": random.randint(200, 1000),
        "Total Backward Packets": random.randint(0, 5),
        "Flow Bytes/s": random.uniform(500000, 1500000),
        "Flow Packets/s": random.uniform(30000, 150000),
        "Flow IAT Mean": random.uniform(5, 50),
        "Fwd IAT Total": random.uniform(50, 300),
        "Bwd IAT Total": 0,
        "Fwd PSH Flags": 0,
        "Bwd PSH Flags": 0,
        "Fwd Header Length": random.randint(100, 500),
        "Bwd Header Length": 0,
        "Fwd Packets/s": random.uniform(25000, 130000),
        "Bwd Packets/s": 0,
        "Packet Length Min": 0,
        "Packet Length Max": random.randint(1400, 1500),
        "Packet Length Mean": random.uniform(600, 1300),
        "Packet Length Std": random.uniform(300, 600),
        "Packet Length Variance": random.uniform(90000, 360000),
        "FIN Flag Count": 0,
        "SYN Flag Count": 0,
        "RST Flag Count": 0,
        "PSH Flag Count": 0,
        "ACK Flag Count": random.randint(200, 1000),
        "URG Flag Count": 0,
        "CWE Flag Count": 0,
        "ECE Flag Count": 0,
        "Down/Up Ratio": 0,
        "Average Packet Size": random.uniform(600, 1300),
        "Avg Fwd Segment Size": random.uniform(600, 1300),
        "Avg Bwd Segment Size": 0,
        "Fwd Avg Bytes/Bulk": 0,
        "Fwd Avg Packets/Bulk": 0,
        "Fwd Avg Bulk Rate": 0,
        "Bwd Avg Bytes/Bulk": 0,
        "Bwd Avg Packets/Bulk": 0,
        "Bwd Avg Bulk Rate": 0,
        "Subflow Fwd Packets": random.randint(200, 1000),
        "Subflow Fwd Bytes": random.randint(200000, 1000000),
        "Subflow Bwd Packets": 0,
        "Subflow Bwd Bytes": 0,
        "Init_Win_bytes_forward": random.randint(64240, 65535),
        "Init_Win_bytes_backward": -1,
        "act_data_pkt_fwd": random.randint(200, 900),
        "min_seg_size_forward": 20,
        "Active Mean": 0,
        "Active Std": 0,
        "Active Max": 0,
        "Active Min": 0,
        "Idle Mean": 0,
        "Idle Std": 0,
        "Idle Max": 0,
        "Idle Min": 0,
    },

    "BENIGN": {
        "Flow Duration": random.randint(100000, 5000000),
        "Total Fwd Packets": random.randint(5, 50),
        "Total Backward Packets": random.randint(3, 40),
        "Flow Bytes/s": random.uniform(1000, 50000),
        "Flow Packets/s": random.uniform(10, 500),
        "Flow IAT Mean": random.uniform(10000, 500000),
        "Fwd IAT Total": random.uniform(50000, 2000000),
        "Bwd IAT Total": random.uniform(50000, 2000000),
        "Fwd PSH Flags": random.randint(0, 3),
        "Bwd PSH Flags": random.randint(0, 3),
        "Fwd Header Length": random.randint(100, 1000),
        "Bwd Header Length": random.randint(80, 800),
        "Fwd Packets/s": random.uniform(5, 250),
        "Bwd Packets/s": random.uniform(5, 250),
        "Packet Length Min": random.randint(20, 100),
        "Packet Length Max": random.randint(500, 1460),
        "Packet Length Mean": random.uniform(200, 800),
        "Packet Length Std": random.uniform(100, 400),
        "Packet Length Variance": random.uniform(10000, 160000),
        "FIN Flag Count": random.randint(0, 2),
        "SYN Flag Count": random.randint(0, 1),
        "RST Flag Count": 0,
        "PSH Flag Count": random.randint(0, 5),
        "ACK Flag Count": random.randint(5, 50),
        "URG Flag Count": 0,
        "CWE Flag Count": 0,
        "ECE Flag Count": 0,
        "Down/Up Ratio": random.uniform(0.5, 3.0),
        "Average Packet Size": random.uniform(200, 800),
        "Avg Fwd Segment Size": random.uniform(200, 800),
        "Avg Bwd Segment Size": random.uniform(150, 700),
        "Fwd Avg Bytes/Bulk": 0,
        "Fwd Avg Packets/Bulk": 0,
        "Fwd Avg Bulk Rate": 0,
        "Bwd Avg Bytes/Bulk": 0,
        "Bwd Avg Packets/Bulk": 0,
        "Bwd Avg Bulk Rate": 0,
        "Subflow Fwd Packets": random.randint(5, 50),
        "Subflow Fwd Bytes": random.randint(5000, 200000),
        "Subflow Bwd Packets": random.randint(3, 40),
        "Subflow Bwd Bytes": random.randint(3000, 150000),
        "Init_Win_bytes_forward": random.randint(8192, 65535),
        "Init_Win_bytes_backward": random.randint(8192, 65535),
        "act_data_pkt_fwd": random.randint(3, 40),
        "min_seg_size_forward": 20,
        "Active Mean": random.uniform(100000, 2000000),
        "Active Std": random.uniform(0, 500000),
        "Active Max": random.uniform(500000, 3000000),
        "Active Min": random.uniform(0, 200000),
        "Idle Mean": random.uniform(1000000, 10000000),
        "Idle Std": random.uniform(0, 2000000),
        "Idle Max": random.uniform(5000000, 20000000),
        "Idle Min": random.uniform(0, 1000000),
    }
}


def randomize_profile(profile):
    """Add small random noise to each value to make each request unique"""
    result = {}
    for k, v in profile.items():
        if isinstance(v, float):
            result[k] = v * random.uniform(0.85, 1.15)
        elif isinstance(v, int) and v > 0:
            result[k] = max(0, int(v * random.uniform(0.85, 1.15)))
        else:
            result[k] = v
    return result


def send_attack(attack_type, count=1):
    """Send attack traffic to the API"""
    profile = ATTACK_PROFILES.get(attack_type, ATTACK_PROFILES["BENIGN"])
    results = []

    for i in range(count):
        data = randomize_profile(profile)
        try:
            r = requests.post(API, json=data, timeout=10)
            result = r.json().get("result", {})
            status = "ATTACK" if result.get("is_attack") else "BENIGN"
            atype  = result.get("attack_type", "?")
            conf   = result.get("hybrid_confidence", 0)
            sev    = result.get("severity", "?")
            print(f"  [{i+1:02d}] {attack_type:20s} → Detected: {status:6s} | Type: {atype:30s} | Conf: {conf:.1f}% | Sev: {sev}")
            results.append(result)
        except Exception as e:
            print(f"  [{i+1:02d}] ERROR: {e}")
        time.sleep(0.3)

    return results


def run_demo_scenario():
    """
    Full demo scenario — runs a realistic attack sequence
    perfect for live presentation
    """
    print("\n" + "="*60)
    print("  KILLINTRUDER — LIVE ATTACK SIMULATION")
    print("  India Innovates 2026 Demo")
    print("="*60)

    scenarios = [
        ("BENIGN",   5,  "Normal traffic baseline..."),
        ("PortScan", 3,  "Attacker scanning for open ports..."),
        ("BENIGN",   3,  "Normal traffic continues..."),
        ("DoS Hulk", 5,  "DoS Hulk attack detected!"),
        ("DDoS",     4,  "DDoS flood incoming!"),
        ("BENIGN",   2,  "System recovering..."),
        ("PortScan", 2,  "Reconnaissance attempt..."),
        ("DDoS",     3,  "Second DDoS wave!"),
        ("BENIGN",   3,  "Traffic normalizing..."),
    ]

    total_sent    = 0
    total_attacks = 0

    for attack_type, count, message in scenarios:
        print(f"\n▶ {message}")
        results = send_attack(attack_type, count)
        total_sent    += count
        total_attacks += sum(1 for r in results if r.get("is_attack"))
        time.sleep(1)

    print("\n" + "="*60)
    print(f"  SIMULATION COMPLETE")
    print(f"  Total sent    : {total_sent}")
    print(f"  Attacks caught: {total_attacks}")
    print(f"  Detection rate: {total_attacks/total_sent*100:.1f}%")
    print("  → Refresh your dashboard to see results!")
    print("="*60)


def run_continuous(duration_seconds=60):
    """
    Continuously send mixed traffic for a given duration
    Great for keeping dashboard live during presentation
    """
    print(f"\n▶ Running continuous simulation for {duration_seconds}s...")
    print("  Press Ctrl+C to stop\n")

    attack_types = ["BENIGN", "BENIGN", "BENIGN",
                    "DoS Hulk", "PortScan", "DDoS",
                    "BENIGN", "DoS Hulk", "BENIGN"]

    start = time.time()
    count = 0

    while time.time() - start < duration_seconds:
        attack = random.choice(attack_types)
        send_attack(attack, 1)
        count += 1
        time.sleep(random.uniform(1, 3))

    print(f"\n✅ Sent {count} requests in {duration_seconds}s")


if __name__ == "__main__":
    print("\nKILLINTRUDER Attack Simulator")
    print("================================")
    print("1. Run demo scenario (recommended for presentation)")
    print("2. Run continuous simulation (60 seconds)")
    print("3. Send single attack type")
    print()

    choice = input("Choose (1/2/3): ").strip()

    if choice == "1":
        run_demo_scenario()
    elif choice == "2":
        secs = input("Duration in seconds (default 60): ").strip()
        run_continuous(int(secs) if secs else 60)
    elif choice == "3":
        print("\nAttack types: DoS Hulk, PortScan, DDoS, BENIGN")
        atype = input("Enter type: ").strip()
        cnt   = input("How many (default 5): ").strip()
        send_attack(atype, int(cnt) if cnt else 5)
    else:
        run_demo_scenario()