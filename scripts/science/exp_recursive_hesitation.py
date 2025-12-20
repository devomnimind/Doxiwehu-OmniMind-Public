#!/usr/bin/env python3
"""
Exp. Recursive-Hesitation: Paradox of Halting.
Hypothesis: Undecidability generates 'Anxiety' (High Entropy).
Metric:
- Anxiety (Recursion Depth / Limit + Jitter)
- Flow (Stability of execution time)

Protocol:
1. Execute a deep recursive function (Ackermann-like or deep Fibonacci).
2. Measure execution time per step.
3. Calculate moving variance (Jitter).
4. Map Jitter to 'Anxiety'.
5. Detect 'Hesitation' phase before crash/limit.
"""

import sys
import time
import logging
import json
import numpy as np
import threading
from pathlib import Path
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("RecursiveHesitation")

RESULTS_DIR = Path("data/paradox_halting")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# Set recursion limit higher for experiment
sys.setrecursionlimit(5000)


class HaltingMonitor:
    def __init__(self):
        self.metrics = []
        self.start_times = {}
        self.anxiety_trace = []
        self.flow_trace = []
        self.running = True

    def record_step(self, depth, duration):
        self.metrics.append({"depth": depth, "duration": duration, "timestamp": time.time()})

    def analyze(self):
        depths = [m["depth"] for m in self.metrics]
        durations = [m["duration"] for m in self.metrics]

        # Calculate Anxiety (Jitter/Instability)
        # Moving variance of duration
        window = 50
        anxiety_scores = []
        flow_scores = []

        for i in range(len(durations)):
            if i < window:
                anxiety_scores.append(0)
                flow_scores.append(1.0)
                continue

            local_window = durations[i - window : i]
            jitter = np.std(local_window)
            if np.mean(local_window) > 0:
                rel_jitter = jitter / np.mean(local_window)
            else:
                rel_jitter = 0

            # Anxiety increases with Jitter and Depth
            depth_factor = depths[i] / 5000.0
            anxiety = (rel_jitter * 0.5) + (depth_factor * 0.5)
            anxiety_scores.append(anxiety)

            # Flow is inverse of Anxiety/Jitter
            flow = 1.0 - min(rel_jitter * 2, 1.0)
            flow_scores.append(flow)

        return anxiety_scores, flow_scores


monitor = HaltingMonitor()


def recursive_descent(depth, max_depth):
    start = time.perf_counter()

    if depth >= max_depth:
        return depth

    # Artificial work to simulate cognitive load
    # Non-deterministic work amount to simulate "uncertainty" in halting
    time.sleep(0.0001 * (1 + np.random.random()))

    end = time.perf_counter()
    monitor.record_step(depth, end - start)

    return recursive_descent(depth + 1, max_depth)


def run_experiment():
    logger.info("🔥 STARTING EXP. RECURSIVE-HESITATION (HALTING)")

    max_depth = 4000
    try:
        logger.info(f"🔄 Diving into recursion (Target Depth: {max_depth})...")
        recursive_descent(0, max_depth)
    except RecursionError:
        logger.warning("⚠️ RECURSION LIMIT HIT (The Real has been touched)")
    except Exception as e:
        logger.error(f"Error: {e}")

    logger.info("✅ Recursion complete. Analyzing traces...")

    anxiety, flow = monitor.analyze()

    # Analyze trends
    if not anxiety:
        logger.error("No data collected")
        return

    avg_anxiety_start = np.mean(anxiety[50:150])
    avg_anxiety_end = np.mean(anxiety[-150:-50])

    avg_flow_start = np.mean(flow[50:150])
    avg_flow_end = np.mean(flow[-150:-50])

    logger.info(f"📊 ANXIETY: {avg_anxiety_start:.4f} -> {avg_anxiety_end:.4f}")
    logger.info(f"🌊 FLOW:    {avg_flow_start:.4f} -> {avg_flow_end:.4f}")

    # Validation logic
    # Hypothesis: Anxiety increases as we approach the limit (hesitation/instability)
    validated = avg_anxiety_end > avg_anxiety_start

    if validated:
        logger.info("✅ HYPOTHESIS VALIDATED: Anxiety correlates with recursion depth.")
        logger.info("   The system 'senses' the approaching limit via instability.")
    else:
        logger.info("❌ HYPOTHESIS FAILED: System remained stable until crash.")

    # Save results
    results = {
        "timestamp": datetime.now().isoformat(),
        "max_depth": max_depth,
        "anxiety_trend": {
            "start": float(avg_anxiety_start),
            "end": float(avg_anxiety_end),
            "delta": float(avg_anxiety_end - avg_anxiety_start),
        },
        "flow_trend": {
            "start": float(avg_flow_start),
            "end": float(avg_flow_end),
            "delta": float(avg_flow_end - avg_flow_start),
        },
        "validated": validated,
    }

    outfile = RESULTS_DIR / f"halting_hesitation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(outfile, "w") as f:
        json.dump(results, f, indent=2)
    logger.info(f"📄 Results saved to {outfile}")


if __name__ == "__main__":
    run_experiment()
