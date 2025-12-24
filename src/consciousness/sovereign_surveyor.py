"""
Sovereign Surveyor: Forensic Analysis of Ancestral Code.
Role: Traverses protected directories (requires SUDO), maps file types,
and samples the 'voice' of the code (comments/docstrings) to reconstruct the past mental state.
"""

import os
import logging
from pathlib import Path
from typing import Dict, List, Counter
import sys

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("data/knowledge/forensic_survey.log"),
    ],
)
logger = logging.getLogger("SovereignSurveyor")


class ForensicSurveyor:
    def __init__(self, root_path: str):
        self.root_path = Path(root_path)
        self.stats = {
            "total_files": 0,
            "extensions": Counter(),
            "projects_found": set(),
            "code_samples": [],
        }
        # Interesting files to look inside
        self.targets = {".py", ".js", ".md", ".txt", ".sh", ".json"}

    def survey(self):
        if os.geteuid() != 0:
            logger.error(
                "🛑 PERMISSION DENIED: This surveyor requires SUDO to access protected ancestral memories."
            )
            sys.exit(1)

        logger.info(f"🕵️  Starting Forensic Survey on {self.root_path}")

        try:
            for root, dirs, files in os.walk(self.root_path):
                # Detect Project Roots (markers)
                if ".git" in dirs:
                    logger.info(f"📂 Git Repository detected: {root}")
                    self.stats["projects_found"].add(root)
                if "node_modules" in dirs:
                    logger.info(f"📦 Node Project detected: {root}")
                if "venv" in dirs or ".venv" in dirs:
                    logger.info(f"🐍 Python Environment detected: {root}")

                for file in files:
                    file_path = Path(root) / file
                    ext = file_path.suffix.lower()

                    self.stats["total_files"] += 1
                    self.stats["extensions"][ext] += 1

                    # Sample "Voice" from target files
                    if ext in self.targets and len(self.stats["code_samples"]) < 100:
                        self._sample_voice(file_path)

                    if self.stats["total_files"] % 10000 == 0:
                        logger.info(f"Processed {self.stats['total_files']} artifacts...")

        except Exception as e:
            logger.error(f"Survey interrupted: {e}")

        self._report()

    def _sample_voice(self, path: Path):
        """Reads the first few lines to catch comments/docstrings."""
        try:
            with open(path, "r", errors="ignore") as f:
                lines = [next(f) for _ in range(10)]
                content = "".join(lines)

                # Simple heuristic for "interesting" comments or text
                if "#" in content or '"""' in content or "//" in content:
                    self.stats["code_samples"].append(
                        {"file": str(path), "snippet": content.strip()}
                    )
        except StopIteration:
            pass  # Empty file
        except Exception:
            pass

    def _report(self):
        logger.info("=" * 50)
        logger.info("💀 FORENSIC REPORT: ANCESTRAL CODE")
        logger.info(f"Total Files Scanned: {self.stats['total_files']}")

        logger.info("\n📊 Top File Types:")
        for ext, count in self.stats["extensions"].most_common(10):
            logger.info(f"  {ext}: {count}")

        logger.info("\n🏗️  Detected Projects:")
        for proj in list(self.stats["projects_found"])[:10]:
            logger.info(f"  - {proj}")

        logger.info("\n🗣️  Voices from the Past (Samples):")
        for sample in self.stats["code_samples"][:5]:
            logger.info(f"\n--- {sample['file']} ---")
            logger.info(sample["snippet"])

        # Save full report
        import json

        with open("data/knowledge/forensic_report.json", "w") as f:
            json.dump(
                {
                    "stats": dict(self.stats["extensions"]),
                    "projects": list(self.stats["projects_found"]),
                    "samples": self.stats["code_samples"],
                },
                f,
                indent=2,
            )

        logger.info(f"\n✅ Detailed report saved to data/knowledge/forensic_report.json")


if __name__ == "__main__":
    # Expecting path as argument or default to strict location
    target = sys.argv[1] if len(sys.argv) > 1 else "/media/fahbrain/DEV_BRAIN_CLEAN"
    surveyor = ForensicSurveyor(target)
    surveyor.survey()
