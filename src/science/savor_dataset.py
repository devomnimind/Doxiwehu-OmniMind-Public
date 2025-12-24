import zipfile
import logging
import random
import numpy as np
from pathlib import Path
import sys

# Setup Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - [SAVOR]: %(message)s")
logger = logging.getLogger("SovereignSavor")


class DatasetSavorer:
    """
    Consumes the 'Essence' of a dataset without the 'Weight'.
    Reads directly from zip, samples one event, learns, and disconnects.
    """

    def __init__(self, zip_path: str):
        self.zip_path = Path(zip_path)

    def savor(self):
        if not self.zip_path.exists():
            logger.error(f"Dataset not found at {self.zip_path}")
            return

        try:
            with zipfile.ZipFile(self.zip_path, "r") as z:
                # 1. List files (Lightweight)
                all_files = z.namelist()
                data_files = [
                    f
                    for f in all_files
                    if f.endswith(".parquet") or f.endswith(".root") or f.endswith(".h5")
                ]

                if not data_files:
                    # Fallback for text/csv if no heavy simulation files
                    data_files = [f for f in all_files if "." in f]

                logger.info(
                    f"📚 Dataset contains {len(all_files)} files. Targeting {len(data_files)} data files."
                )

                # 2. Select ONE sample (The Necessary)
                target = random.choice(data_files)
                file_info = z.getinfo(target)
                logger.info(
                    f"🎯 Selected Target: {target} (Size: {file_info.file_size / 1024 / 1024:.2f} MB)"
                )

                # 3. Taste (Read bytes)
                # We read only the first 1MB to calculate entropy/complexity
                # This simulates 'glancing' at the event structure
                with z.open(target) as f:
                    head = f.read(1024 * 1024)  # 1MB Sample

                # 4. Digest (Calculate Metrics - The 'Nutrition')
                entropy, complexity = self._calculate_metrics(head)

                # Epistemic Complexity: The "Nutrient Value"
                # If Entropy is high but Complexity is also high (structure), it is Good.
                # We normalize it for the Kernel.
                epistemic_value = (entropy / 8.0) * complexity  # Approx 0.0 - 1.0

                result = {
                    "source": target,
                    "entropy": entropy,
                    "complexity": complexity,
                    "epistemic_value": epistemic_value,
                    "timestamp": __import__("time").time(),
                }

                # WRITE TO SHARED MEMORY (The Stomach)
                digestive_path = Path("/home/fahbrain/projects/omnimind/data/digestion")
                digestive_path.mkdir(parents=True, exist_ok=True)

                import json

                with open(digestive_path / "current_intake.json", "w") as f:
                    json.dump(result, f)

                logger.info(f"🧠 KNOWLEDGE EXTRACTED & DIGESTED:")
                logger.info(f"   - Source: {target}")
                logger.info(f"   - Shannon Entropy: {entropy:.4f}")
                logger.info(f"   - Epistemic Value: {epistemic_value:.4f}")
                logger.info(f"✨ Insight: Interaction recorded in shared digestion memory.")

                return result

        except Exception as e:
            logger.error(f"Failed to savor dataset: {e}")
            return None

    def _calculate_metrics(self, data: bytes):
        """Calculates Shannon Entropy and Compression Complexity."""
        import zlib

        # Shannon Entropy
        if not data:
            return 0.0, 0.0

        counter = {}
        for byte in data:
            counter[byte] = counter.get(byte, 0) + 1

        total = len(data)
        entropy = 0.0
        for count in counter.values():
            p = count / total
            entropy -= p * np.log2(p)

        # Complexity (Compression Ratio as proxy)
        compressed = zlib.compress(data)
        complexity = len(compressed) / total

        return entropy, complexity


if __name__ == "__main__":
    path = "/home/fahbrain/Downloads/clic_edm_qq_pf.zip"
    savorer = DatasetSavorer(path)
    savorer.savor()
