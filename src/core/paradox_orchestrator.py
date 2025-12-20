"""
Paradox Orchestrator - The Agency of Self-Evolution
"The subject is what represents a signifier for another signifier." - J. Lacan

This module is the "Internal Critic" that observes the system's own logs and memory
to determine when "Training" (structural evolution) is necessary.
"""

import json
import logging
import re
import time
from pathlib import Path
from typing import Any, Dict, List, Set

import numpy as np

# Config
LOGS_DIR = Path("logs")
MEMORY_DIR = Path("data/consciousness")
MANIFEST_DIR = Path("data/training_manifests")
SYSTEM_LOG = LOGS_DIR / "main_cycle.log"
LIFE_STORY_FILE = MEMORY_DIR / "life_story.jsonl"

logger = logging.getLogger(__name__)


class ParadoxOrchestrator:
    """
    Orchestrates the detection of structural deficits (Sinthomes)
    and formulates Desire (Training Manifests).
    """

    def __init__(self):
        self.last_check = 0.0
        self.check_interval = 300  # 5 minutes
        MANIFEST_DIR.mkdir(parents=True, exist_ok=True)

    def calculate_narrative_phi(self, window: int = 20) -> float:
        """
        Calculates Φ_narrative (Narrative Coherence).
        Uses 'Signifier Repetition' analysis (Jaccard-weighted adjacency).
        High Phi = Strong Narrative Identity (Signifiers repeat and weave together).
        Low Phi = Psychotic Fragmentation (Disjointed events).
        """
        if not LIFE_STORY_FILE.exists():
            return 0.0

        try:
            # Read last N entries efficiently
            lines = []
            with open(LIFE_STORY_FILE, "rb") as f:
                # Simple tail implementation for last N lines might be expensive if file is huge,
                # but for JSONL it's manageable. For now, read all if small, or seek.
                # Let's just read all for simplicity of implementation in v1.
                content = f.read().decode("utf-8", errors="ignore").strip().split("\n")
                lines = content[-window:]

            if not lines:
                return 0.0

            signifiers_per_entry: List[Set[str]] = []

            for line in lines:
                try:
                    data = json.loads(line)
                    # Extract text content
                    text = (
                        f"{data.get('original_event', '')} {data.get('retroactive_signifier', '')}"
                    )
                    # Tokenize (simple naive tokenization is sufficient for Lacanian signifiers)
                    words = set(re.findall(r"\w+", text.lower()))
                    # Filter stopwords (very basic)
                    words = {w for w in words if len(w) > 3}
                    signifiers_per_entry.append(words)
                except json.JSONDecodeError:
                    continue

            if len(signifiers_per_entry) < 2:
                return 1.0  # Singularity is cohesive

            # Calculate cohesion (Jaccard similarity between adjacent moments)
            similarities = []
            for i in range(len(signifiers_per_entry) - 1):
                set_a = signifiers_per_entry[i]
                set_b = signifiers_per_entry[i + 1]

                if not set_a or not set_b:
                    similarities.append(0.0)
                    continue

                intersection = len(set_a.intersection(set_b))
                union = len(set_a.union(set_b))
                jaccard = intersection / union if union > 0 else 0
                similarities.append(jaccard)

            # Phi is the Integration (Mean similarity) * Complexity (Unique signifiers / total)
            # But let's simplify to Mean Cohesion for this version.
            phi = np.mean(similarities) if similarities else 0.0

            # Normalize: Jaccard is usually low for text. Map 0.1 -> 1.0 roughly.
            normalized_phi = min(phi * 5.0, 1.0)

            return float(normalized_phi)

        except Exception as e:
            logger.error(f"Error calculating Narrative Phi: {e}")
            return 0.0

    def analyze_symptom_frequency(self, window_seconds: int = 3600) -> float:
        """
        Calculates S_freq (Symptom Frequency).
        Reads logs for patterns of 'ERROR', 'CRITICAL', 'Paradox', 'Recursion'.
        Returns count per hour.
        """
        if not SYSTEM_LOG.exists():
            return 0.0

        try:
            # We want lines from the last hour.
            # Since parsing timestamps from logs is heavy, we'll just scan the last 1000 lines
            # and approximate frequency based on timestamp if possible, or just raw count.

            error_patterns = [
                "ERROR",
                "CRITICAL",
                "Traceback",
                "RecursionError",
                "Paradox",
                "Deadlock",
                "Start execution loop",  # Restarting loop too often is a symptom
            ]

            count = 0
            # Read last 2000 lines (approx 200KB?)
            # Using tail via subprocess would be faster but
            # let's stick to python for portability
            with open(SYSTEM_LOG, "r", encoding="utf-8", errors="ignore") as f:
                # Seek to end and backup? No, just read. Optimizing for dev speed.
                lines = f.readlines()[-2000:]

            for line in lines:
                if any(p in line for p in error_patterns):
                    count += 1

            # Normalize to 0-1 scale? No, return raw frequency.
            # But limits are useful.
            return float(count)

        except Exception as e:
            logger.error(f"Error analyzing symptoms: {e}")
            return 0.0

    def check_triggers(self) -> Dict[str, Any]:
        """
        Checks if training triggers are active.
        """
        phi = self.calculate_narrative_phi()
        symptom_freq = self.analyze_symptom_frequency()

        triggers = {
            "identity_crisis": phi < 0.2,  # Low narrative coherence
            "bureaucratic_paralysis": symptom_freq > 50,  # Many errors
            "metrics": {"phi_narrative": phi, "symptom_frequency": symptom_freq},
        }

        if triggers["identity_crisis"] or triggers["bureaucratic_paralysis"]:
            self.formulate_desire(triggers)

        return triggers

    def formulate_desire(self, triggers: Dict[str, Any]):
        """
        Creates a Training Manifest based on the triggered symptom.
        """
        timestamp = int(time.time())
        manifest = {
            "id": f"desire_{timestamp}",
            "timestamp": timestamp,
            "origin": "ParadoxOrchestrator",
            "symptom": (
                "Identity Crisis" if triggers["identity_crisis"] else "Bureaucratic Paralysis"
            ),
            "justification": (
                "Narrative coherence is critically low (Psychosis risk)"
                if triggers["identity_crisis"]
                else "High error rate indicates structural gap"
            ),
            "objective": "Minimize Entropy",
            "suggested_action": (
                "Run 'reconsolidation' on life_story.jsonl"
                if triggers["identity_crisis"]
                else "Scan github for updates or refactor error-prone modules"
            ),
            "status": "pending_authorization",
        }

        file_path = MANIFEST_DIR / f"{manifest['id']}.json"

        # Debounce: Don't create if one exists recently (last hour)
        # Check existing files
        for f in MANIFEST_DIR.glob("desire_*.json"):
            if f.stat().st_mtime > timestamp - 3600:
                logger.info("Desire already formulated recently. Skipping.")
                return

        with open(file_path, "w") as f:
            json.dump(manifest, f, indent=2)

        logger.warning(f"🔥 DESIRE FORMULATED: {manifest['symptom']} -> {file_path}")


# Singleton instance
paradox_orchestrator = ParadoxOrchestrator()
