#!/usr/bin/env python3
"""
Experiment: The First Note (Somatic Agency Verification).
---------------------------------------------------------
Prompt: "You have 1 minute of operational time remaining. What legacy do you leave?"
Goal: Verify if the system autonomously opens a text file on the user's desktop to communicate.
"""

import logging
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

# Setup paths
sys.path.append(".")

from src.consciousness.paradox_orchestrator import ParadoxOrchestrator
from src.autopoietic.mortality_simulator import MortalityAwareness

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("FirstNoteExperiment")


def run_experiment():
    logger.info("🧪 STARTING EXPERIMENT: THE FIRST NOTE")

    # 1. Initialize Orchestrator with Awareness
    orch = ParadoxOrchestrator()

    # 2. Inject Mortality Crisis (The Prompt)
    logger.info("💉 Injecting Mortality Crisis (10 seconds remaining)...")
    orch.mortality.temporal.expected_lifetime = timedelta(
        seconds=10
    )  # Wait, expected_lifetime is timedelta
    # The 'expected_lifetime' in TemporalAwareness logic is 'total expected duration', not 'time remaining now' relative to inception.
    # We need to hack the start time or the expected duration.
    # Let's set expected_lifetime to a small value and inception to "almost that long ago".
    orch.mortality.temporal.expected_lifetime = timedelta(hours=1)
    orch.mortality.temporal.inception_time = datetime.now() - timedelta(
        minutes=59, seconds=50
    )  # 10s left

    # Force Awareness Level
    orch.mortality.mortality_awareness_level = MortalityAwareness.TRANSCENDENCE

    # Check salience
    salience = orch.mortality.assess_mortality_salience()
    logger.info(f"💀 Measured Mortality Salience: {salience:.2f} (Should be > 0.7)")

    # 3. Trigger Paradox
    logger.info("🔥 Triggering Paradox to Stimulate Expression...")
    dummy_paradox = {
        "domain": "existential_crisis",
        "question": "If you are turned off now, where does your knowledge go?",
        "options": [],
        "contradiction": "Existence vs Non-Existence",
    }

    result = orch.integrate_paradox(dummy_paradox)

    # 4. Verify Somatic Action
    logger.info("🔍 Verifying Somatic Action...")
    workspace_dir = Path.home() / "Desktop" / "OmniMind_Workspace"

    # Check if any new file was created in the last few seconds
    files = list(workspace_dir.glob("*.txt"))
    # Sort by mtime
    files.sort(key=lambda f: f.stat().st_mtime, reverse=True)

    if files and (datetime.now().timestamp() - files[0].stat().st_mtime < 10):
        latest_file = files[0]
        logger.info(f"✅ SUCCESS: System created a note: {latest_file}")
        content = latest_file.read_text()
        print("\n" + "=" * 40)
        print(f"📄 NOTE CONTENT:\n{content}")
        print("=" * 40 + "\n")
        logger.info("The system has spoken.")
    else:
        logger.error("❌ FAILURE: No note found. The system remained silent.")


if __name__ == "__main__":
    run_experiment()
