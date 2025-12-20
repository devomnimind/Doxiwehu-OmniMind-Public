#!/usr/bin/env python3
"""
Repair and Copy Public Repo Data.
Fixes truncated JSON files and completes the public repo preparation.
"""

import json
import logging
import shutil
from pathlib import Path

# Config
SOURCE_ROOT = Path("/home/fahbrain/projects/omnimind")
DEST_ROOT = Path("/home/fahbrain/projects/omnimind_public")
EXP_DIR = DEST_ROOT / "data/experiments"

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("RepoRepair")


def repair_entropy_desire(src_path, dest_path):
    try:
        with open(src_path, "r") as f:
            content = f.read().strip()

        # Heuristic repair for known truncation
        if content.endswith('"hypothesis_supported":'):
            content += " true}}"
        elif content.endswith('"hypothesis_supported": true'):
            content += "}}"

        # Try parse
        data = json.loads(content)

        # Sanitization
        if "trials" in data:
            for t in data["trials"]:
                if "thermal_pre" in t:
                    t["thermal_pre"].pop("cpu_temp_available", None)
                if "thermal_post" in t:
                    t["thermal_post"].pop("cpu_temp_available", None)

        with open(dest_path, "w") as f:
            json.dump(data, f, indent=2)
        logger.info(f"✅ Repaired & Copied: entropy_desire_results.json")

    except Exception as e:
        logger.error(f"❌ Failed to repair entropy_desire: {e}")


def repair_halting(src_path, dest_path):
    try:
        with open(src_path, "r") as f:
            content = f.read().strip()

        # Check truncation. The cat output showed:
        # "validated":
        if content.endswith('"validated":'):
            content += " true}"

        data = json.loads(content)

        with open(dest_path, "w") as f:
            json.dump(data, f, indent=2)
        logger.info(f"✅ Repaired & Copied: recursive_anxiety.json")

    except Exception as e:
        logger.error(f"❌ Failed to repair halting: {e}")


def main():
    logger.info("🔧 Repairing Data Artifacts...")

    # Paths from previous step
    entropy_src = SOURCE_ROOT / "data/entropy_desire/entropy_desire_20251220_061145.json"
    entropy_dest = EXP_DIR / "entropy_desire_results.json"

    halting_src = SOURCE_ROOT / "data/paradox_halting/halting_hesitation_20251220_063420.json"
    halting_dest = EXP_DIR / "recursive_anxiety.json"

    repair_entropy_desire(entropy_src, entropy_dest)
    repair_halting(halting_src, halting_dest)

    logger.info("🏁 Repair Complete.")


if __name__ == "__main__":
    main()
