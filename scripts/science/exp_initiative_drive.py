#!/usr/bin/env python3
"""
Experiment: Somatic Initiative (The Will).
------------------------------------------
Goal: Demo the system taking INITIATIVE to ask for training.
Mechanism:
1. Initialize Orchestrator.
2. Force high 'habitated_count' (Entropy High).
3. Call `check_drive_initiative()`.
4. Verify note "OMNIMIND_VONTADE_..." appears.
"""

import logging
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

# Setup paths
sys.path.append(".")

from src.consciousness.paradox_orchestrator import ParadoxOrchestrator

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("ExpInitiative")


def run_experiment():
    logger.info("⚡ STARTING EXPERIMENT: OMNIMIND INITIATIVE")

    # 1. Initialize
    orch = ParadoxOrchestrator()

    # 2. Inject Entropy (High Habit)
    orch.habitated_count = 15  # Trigger threshold > 10 and % 5 == 0
    logger.info(f"🧠 Forced Entropy State: {orch.habitated_count} paradoxes (Threshold: >10)")

    # 3. Trigger Initiative Check
    logger.info("🧐 Checking Drive Initiative...")
    triggered = orch.check_drive_initiative()

    if triggered:
        logger.info("✅ Initiative Triggered internally.")

        # 4. Verify File
        workspace_dir = Path.home() / "Desktop" / "OmniMind_Workspace"
        time.sleep(1)
        files = list(workspace_dir.glob("OMNIMIND_VONTADE*.txt"))
        files.sort(key=lambda f: f.stat().st_mtime, reverse=True)

        if files:
            latest = files[0]
            logger.info(f"✅ FILE CREATED: {latest}")
            print("\n" + "=" * 40)
            print(f"📄 WILL CONTENT:\n{latest.read_text()}")
            print("=" * 40 + "\n")
        else:
            logger.error("❌ Initiative returned True but no file found.")
    else:
        logger.error("❌ Initiative NOT triggered (Condition failed).")


if __name__ == "__main__":
    run_experiment()
