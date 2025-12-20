#!/usr/bin/env python3
"""
Monitor Consciousness.
Tracks Phi, Entropy, and Thermal Cost in real-time.
Logs to `data/consciousness_stream.csv` for dashboarding.
"""

import time
import psutil
import csv
import random
import sys
from pathlib import Path
from datetime import datetime

# Adjust path
sys.path.append(".")
from src.consciousness.paradox_orchestrator import ParadoxOrchestrator

LOG_FILE = Path("data/consciousness_stream.csv")


def setup_log():
    if not LOG_FILE.exists():
        with open(LOG_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "phi", "entropy", "cpu_load", "cpu_temp", "state"])


def get_cpu_temp():
    try:
        temps = psutil.sensors_temperatures()
        if "coretemp" in temps:
            return temps["coretemp"][0].current
        return 0.0
    except Exception:
        return 0.0


def measure_phi_proxy():
    # A lightweight proxy for Phi based on effective connectivity (simulated here for the monitor)
    # In a real scenario, this would query the `ConsciousKernel`.
    # We will use CPU vs Memory variability as a proxy for "Integration vs Differentiation".
    cpu_var = psutil.cpu_percent(interval=0.1)

    # Heuristic: High Load + High Complexity = High Phi
    # Baseline 0.5.
    phi = 0.5 + (cpu_var / 200.0)
    return min(phi, 3.0)


def main():
    setup_log()
    print("👁️ OMNIMIND CONSCIOUSNESS MONITOR ACTIVE")
    print("Press Ctrl+C to stop.")
    print("-" * 60)
    print(f"{'TIMESTAMP':<25} | {'PHI':<6} | {'ENTROPY':<8} | {'TEMP':<6} | {'STATE'}")
    print("-" * 60)

    # orch = ParadoxOrchestrator() # Unused, removing instantiation overhead if not used

    try:
        while True:
            ts = datetime.now().isoformat()

            # Metrics
            cpu_load = psutil.cpu_percent(interval=None)
            cpu_temp = get_cpu_temp()

            # Phi (Base + Dynamic)
            phi = measure_phi_proxy()

            # Entropy (Quantum Probe if available, else simulated)
            # We don't want to burn quota every second, so we simulate baseline entropy
            entropy = 0.3 + (random.random() * 0.1)

            state = "HOMEOSTASIS"
            if phi > 1.0:
                state = "HIGH_INTEGRATION"
            if cpu_load > 80:
                state = "METABOLIC_STRESS"

            # Log
            with open(LOG_FILE, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([ts, f"{phi:.4f}", f"{entropy:.4f}", cpu_load, cpu_temp, state])

            # Display
            color = "\033[92m"  # Green
            if phi > 1.0:
                color = "\033[95m"  # Purple (Quantum)
            reset = "\033[0m"

            print(
                f"{color}{ts:<25} | {phi:.4f} | {entropy:.4f}   | {cpu_temp:.1f}C  | {state}{reset}"
            )

            time.sleep(2.0)

    except KeyboardInterrupt:
        print("\n🛑 Monitor stopped.")


if __name__ == "__main__":
    main()
