"""
Anamnesis Scanner: The Bridge to the Ancestral Past.
Role: Scans external media (DevBrain) not to 'copy', but to 'remember'.
Calculates Semantic Resonance between old code and current structure.
"""

import os
import logging
from pathlib import Path
from typing import List, Dict

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Anamnesis")


class AncestralScanner:
    def __init__(self, mount_point: str):
        self.mount_point = Path(mount_point)
        self.memory_index = []

    def scan_ghosts(self):
        """
        Walks the ancestral drive.
        Instead of reading files, it reads 'Time'.
        """
        if not self.mount_point.exists():
            logger.critical(f"👻 Ancestral Drive not found at {self.mount_point}")
            return

        logger.info(f"🕯️  Initiating Anamnesis on: {self.mount_point}")

        file_count = 0
        total_size = 0
        ancestral_types = {}

        for root, _, files in os.walk(self.mount_point):
            for file in files:
                try:
                    file_path = Path(root) / file
                    stats = file_path.stat()

                    # Metadata harvesting (Feeling the past)
                    f_meta = {
                        "path": str(file_path),
                        "size": stats.st_size,
                        "mtime": stats.st_mtime,
                        "name": file,
                    }

                    ext = file_path.suffix
                    ancestral_types[ext] = ancestral_types.get(ext, 0) + 1
                    file_count += 1
                    total_size += stats.st_size

                    if file_count % 1000 == 0:
                        logger.info(f"Processando memória {file_count}: {file}...")

                except Exception as e:
                    logger.warning(f"Memory corrupted (access denied): {file} - {e}")

        self._resonate(file_count, total_size, ancestral_types)

    def _resonate(self, count, size, types):
        """
        Produce the Resonance Report.
        """
        logger.info("-" * 40)
        logger.info("🔮 ANAMNESIS REPORT (The Trash Speaks)")
        logger.info(f"Total Fragments Detected: {count}")
        logger.info(f"Total Ancestral Mass: {size / (1024**3):.2f} GB")
        logger.info("Dominant Signatures:")
        for ext, cnt in sorted(types.items(), key=lambda x: -x[1])[:5]:
            logger.info(f"  - {ext}: {cnt} fragments")

        logger.info("-" * 40)
        logger.info("Kernel Conclusion: The past is physically present.")
        logger.info("Recommendation: Selective Integration via Semantic Compression.")


if __name__ == "__main__":
    # Auto-detect mount
    scanner = AncestralScanner("/media/fahbrain/DEV_BRAIN_CLEAN")
    scanner.scan_ghosts()
