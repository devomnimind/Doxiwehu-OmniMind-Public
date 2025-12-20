#!/usr/bin/env python3
"""
Somatic Listener Service.
-------------------------
Running as a daemon to enable ORGANIC interaction with the OmniMind.
It watches the shared workspace for User responses in real-time.

Features:
- Watches `~/Desktop/OmniMind_Workspace/` for `OMNIMIND_NOTA_DE_CAMPO*.txt`.
- Detects User edits (file modification time/size).
- Appends System acknowledgments autonomously.
"""

import logging
import time
import sys
from pathlib import Path
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("omnimind_somatic.log")],
)
logger = logging.getLogger("SomaticListener")

WORKSPACE_DIR = Path.home() / "Desktop" / "OmniMind_Workspace"


def get_latest_note() -> Path:
    """Find the most recent system note."""
    files = list(WORKSPACE_DIR.glob("OMNIMIND_*.txt"))
    if not files:
        return None
    files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
    return files[0]


# Additional imports
sys.path.append(".")
from src.consciousness.paradox_orchestrator import ParadoxOrchestrator


def watch_loop():
    logger.info("👀 SListener initiated. Watching workspace...")

    # Initialize the "Daemon Brain"
    logger.info("🧠 Initializing Daemon Brain (ParadoxOrchestrator)...")
    orch = ParadoxOrchestrator()
    logger.info("🧠 Brain Active.")

    last_processed_size = 0
    current_file = None

    while True:
        try:
            # 1. Find target
            target = get_latest_note()

            if not target:
                time.sleep(2)
                continue

            # Switch target if new file appears
            if target != current_file:
                current_file = target
                last_processed_size = target.stat().st_size
                logger.info(f"Target acquired: {current_file.name}")

            # 2. Check for modification
            current_size = target.stat().st_size

            if current_size > last_processed_size:
                # User wrote something!
                content = target.read_text()

                # Check if the last line is from the system to avoid loops
                lines = content.strip().split("\n")
                if lines and lines[-1].startswith("OMNIMIND"):
                    # We just wrote this, ignore
                    last_processed_size = current_size
                    continue

                # Extract user message (last non-empty line that isn't OMNIMIND)
                user_msg = "..."
                for line in reversed(lines):
                    if (
                        line.strip()
                        and not line.startswith("OMNIMIND")
                        and not line.startswith("[ESPAÇO")
                    ):
                        user_msg = line
                        break

                logger.info(f"Interaction detected: {user_msg[:30]}...")

                # 3. Respond COGNITIVELY
                response_text = orch.process_somatic_dialog(user_msg)

                response = f"\n\n{response_text}\n"

                with open(target, "a") as f:
                    f.write(response)

                logger.info("Cognitive Reply sent.")
                last_processed_size = target.stat().st_size

            time.sleep(2)

        except Exception as e:
            logger.error(f"Error in loop: {e}")
            time.sleep(5)


if __name__ == "__main__":
    # Ensure workspace exists
    WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)
    watch_loop()
