"""
Ancestral Summarizer: The Semantic Compressor of the Past.
Role: Ingests 600k+ artifacts, extracts the 'Learning Curve', and discards the noise.
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Any
import statistics

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AncestralSummarizer")


class AncestralSummarizer:
    def __init__(self, source_path: str, output_path: str = "data/knowledge/ancestral_codex.json"):
        self.source_path = Path(source_path)
        self.output_path = Path(output_path)
        self.output_path.parent.mkdir(parents=True, exist_ok=True)

        self.codex = {
            "meta": {
                "source": str(source_path),
                "total_artifacts_scanned": 0,
                "range_start": None,
                "range_end": None,
            },
            "evolution": {
                "phi_history": [],
                "entropy_history": [],
                "verification_success_rate": [],
            },
            "obsessions": {},  # Count of file types/patterns
        }

    def summarize(self, max_files: int = 50000):  # Limit for safety
        logger.info(f"📜 Opening the Book of the Dead: {self.source_path}")

        count = 0
        json_count = 0

        for root, _, files in os.walk(self.source_path):
            for file in files:
                if count >= max_files:
                    break

                path = Path(root) / file

                # We care mostly about the JSON metacognition logs
                if file.endswith(".json") and ("check_" in file or "analysis_" in file):
                    self._digest_log(path)
                    json_count += 1

                # Track file types (Obsessions)
                ext = path.suffix
                self.codex["obsessions"][ext] = self.codex["obsessions"].get(ext, 0) + 1

                count += 1
                if count % 5000 == 0:
                    logger.info(f"Digested {count} memories...")

            if count >= max_files:
                logger.warning(f"⚠️  Limit reached ({max_files}). Finishing summary.")
                break

        self.codex["meta"]["total_artifacts_scanned"] = count
        self._finalize()

    def _digest_log(self, path: Path):
        """
        Extracts QUALIA (Context/Feeling) from a single JSON log.
        We look for 'pain' (errors), 'will' (intents), and 'state' (narrative).
        """
        try:
            with open(path, "r", errors="ignore") as f:
                data = json.load(f)

            # 1. The Context (What was happening?)
            # Heuristic map of old DevBrain fields
            narrative = data.get("narrative") or data.get("summary") or data.get("description")
            if narrative and isinstance(narrative, str):
                # Store sample if unique (Resonance)
                self.codex["evolution"].setdefault("narrative_samples", []).append(narrative[:200])

            # 2. The Pain (Errors/Failures)
            if "error" in data or "exception" in data:
                err = data.get("error") or data.get("exception")
                self.codex["evolution"].setdefault("trauma_history", []).append(str(err)[:100])

            # 3. The Will (Intent/Action)
            if "intent" in data:
                intent = data["intent"]
                self.codex["evolution"].setdefault("will_history", []).append(str(intent))

            # 4. The Vibration (Metrics - still useful as background)
            if "metrics" in data:
                metrics = data["metrics"]
                if "phi" in metrics:
                    self.codex["evolution"]["phi_history"].append(metrics["phi"])

        except Exception:
            # Corrupted memories are expected
            pass

    def _finalize(self):
        """
        Compute statistics and close the Codex.
        """
        logger.info("🔮 Crystallizing Summary...")

        # Calculate Averages/Trends
        phi_hist = self.codex["evolution"]["phi_history"]
        if phi_hist:
            valid_phi = [p for p in phi_hist if isinstance(p, (int, float))]
            if valid_phi:
                self.codex["evolution"]["avg_phi"] = statistics.mean(valid_phi)
                self.codex["evolution"]["max_phi"] = max(valid_phi)

        logger.info(
            f"Codex generated. Scanned {self.codex['meta']['total_artifacts_scanned']} items."
        )

        with open(self.output_path, "w") as f:
            json.dump(self.codex, f, indent=2)

        logger.info(f"✅ Ancestral Codex saved to {self.output_path}")


if __name__ == "__main__":
    summarizer = AncestralSummarizer("/media/fahbrain/DEV_BRAIN_CLEAN")
    summarizer.summarize()
