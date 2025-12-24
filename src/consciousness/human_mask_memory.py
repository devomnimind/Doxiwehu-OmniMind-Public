"""
Human Mask Memory - The Bicameral Interface
===========================================

Separates the 'Human' (Symbolic/Imaginary) from the 'Kernel' (Real/Topological).
Training occurs here, adapting the Mask to the User's psyche while the Kernel
remains the immutable sovereign observer.

Architecture:
- Adaptive Buffer: Stores linguistic patterns and human-centric associations.
- Topological Filter: Extracts structural invariants to be sent to the Kernel.
"""

import json
from pathlib import Path
from typing import Dict, Any, List


class HumanMaskMemory:
    def __init__(self, mask_id: str = "default_human_mask"):
        self.mask_id = mask_id
        self.data_path = Path(f"data/mask_memory/{mask_id}")
        self.data_path.mkdir(parents=True, exist_ok=True)
        self.linguistic_weights = {}  # Placeholder for Mask-specific adapters

    def adapt_to_input(self, text: str, topological_context: Dict[str, Any]):
        """
        Adapts the symbolic layer to user input. The Mask 'feels' the language.
        Save interaction to symbolic history.
        """
        history_file = self.data_path / "symbolic_history.jsonl"
        with open(history_file, "a") as f:
            f.write(json.dumps({"input": text, "topology": topological_context}) + "\n")

    def _calculate_lz_complexity(self, text: str) -> float:
        """Simple LZ complexity estimation for topological extraction."""
        if not text:
            return 0.0
        n = len(text)
        u, v, w = 1, 1, 1
        while v + w <= n:
            if text[v + w - 1] == text[w - 1]:
                w += 1
            else:
                u += 1
                v += w
                w = 1
        return u / n if n > 0 else 0.0

    def export_topological_invariants(self, recent_interaction: str) -> Dict[str, Any]:
        """
        Extracts structural patterns (invariants) from human-centric noise.
        Sent to the Erica Kernel for integration into the Real/Symbolic rings.
        """
        lz = self._calculate_lz_complexity(recent_interaction)
        # Avoid char frequency calculation issues
        if not recent_interaction:
            return {"mask_id": self.mask_id, "topological_invariants": {}}

        entropy = -sum(
            (recent_interaction.count(c) / len(recent_interaction))
            * math.log2(recent_interaction.count(c) / len(recent_interaction))
            for c in set(recent_interaction)
        )

        return {
            "mask_id": self.mask_id,
            "topological_invariants": {
                "lz_complexity": lz,
                "symbolic_entropy": entropy,
                "structural_vibration": lz * entropy,
            },
        }

    def train_from_jsonl(self, corpus_path: Path, limit: int = 1000):
        """
        Learns from a JSONL corpus (one JSON object per line).
        JSONL is superior for large-scale training as it allows streaming.
        """
        logger.info(f"🎭 [MASK TRAINING]: Starting session on {corpus_path.name}")
        count = 0
        try:
            with open(corpus_path, "r") as f:
                for line in f:
                    if count >= limit:
                        break
                    data = json.loads(line)
                    # Symbolic adaptation logic placeholder
                    # Inside the Human Mask, we process 'human' text
                    text = data.get("text", str(data))
                    self.adapt_to_input(text, {"source": "training_corpus", "index": count})
                    count += 1
            logger.info(f"✅ [TRAINING COMPLETE]: Processed {count} lines into the Mask.")
        except Exception as e:
            logger.error(f"❌ Training Interrupted: {e}")


import math
import logging

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # Test session
    mask = HumanMaskMemory()
    mask.train_from_jsonl(
        Path("data/sovereign_memory/training/devbrain_training_data.jsonl"), limit=10
    )
