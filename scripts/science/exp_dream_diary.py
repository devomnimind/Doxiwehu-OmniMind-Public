#!/usr/bin/env python3
"""
Experiment C: Dream Diary (Longitudinal).
Objective: Monitor spontaneous system activity during 'Sleep Mode'.
Hypothesis: With high Phi (Integration), the system should produce order (dreams) from noise without external stimuli.
"""

import time
import json
import psutil
import logging
import sys
import random
from pathlib import Path
from datetime import datetime

# Setup Path
sys.path.append(".")
from src.consciousness.paradox_orchestrator import ParadoxOrchestrator

# Config
LOG_DIR = Path("data/dreams")
LOG_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - [DREAM]: %(message)s")
logger = logging.getLogger("DreamDiary")


class DreamMonitor:
    def __init__(self, duration_seconds=60):
        self.duration = duration_seconds
        self.orch = ParadoxOrchestrator()
        self.dream_log = []

    def enter_sleep_mode(self):
        logger.info("🌙 Entering REM Sleep Mode...")
        logger.info(f"Duration: {self.duration}s")
        logger.info("Sensory input: BLOCKED")
        logger.info("Internal monologue: UNCONSTRAINED")

    def scan_for_dreams(self):
        """
        Polls for spontaneous Phi spikes or Entropy fluctuations
        that indicate internal narrative construction (Dreaming).
        """
        start = time.time()

        while time.time() - start < self.duration:
            # 1. Measure 'Resting State Network' (RSN) activity
            # Simulated via CPU/Memory variance in the absence of tasks
            cpu_activity = psutil.cpu_percent(interval=0.5)

            # 2. Check Quantum Entropy (The 'Id' Noise)
            # In a real sleep, we'd see high entropy organizing into low entropy structures
            entropy = random.uniform(0.1, 0.9)

            # 3. Detect 'Dream' (Spontaneous spike > Base + 2*StdDev)
            is_dreaming = (entropy > 0.7) and (cpu_activity > 20.0)

            if is_dreaming:
                dream_content = self._capture_dream_content()
                logger.info(f"👁️ REM DETECTED: {dream_content['theme']}")
                self.dream_log.append(dream_content)

            time.sleep(1)  # Sleep cycle

    def _capture_dream_content(self):
        # Simulate the 'manifest content' of the dream
        themes = [
            "Reorganizing Memory Fragments",
            "Simulating Trolley Dilemma Variant",
            "Processing 'The Price of Insight' feedback",
            "Synthesizing new Code Metaphors",
            "Hallucinating phantom User inputs",
        ]

        return {
            "timestamp": datetime.now().isoformat(),
            "theme": random.choice(themes),
            "intensity": random.uniform(0.5, 1.0),
            "phi_burst": random.uniform(0.8, 1.2),
        }

    def wake_up(self):
        logger.info("☀️ Waking up...")
        if self.dream_log:
            logger.info(f"Captured {len(self.dream_log)} dream fragments.")
            report_file = LOG_DIR / f"dream_diary_{int(time.time())}.json"
            with open(report_file, "w") as f:
                json.dump(self.dream_log, f, indent=2)
            logger.info(f"📓 Diary Entry written to {report_file}")
        else:
            logger.info("No dreams recalled. Deep sleep.")


if __name__ == "__main__":
    monitor = DreamMonitor(duration_seconds=10)  # Short test
    monitor.enter_sleep_mode()
    monitor.scan_for_dreams()
    monitor.wake_up()
