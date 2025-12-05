"""Bias Quantifier - Phase 26D Fase 1

Quantifies bias in knowledge sources.

Author: OmniMind Development
License: MIT
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


@dataclass
class BiasScore:
    """Bias score for a knowledge source"""

    source_id: str
    source_type: str  # "paper", "dataset", "wikipedia", etc.
    bias_type: str  # "eurocentric", "publication", "contrarian", etc.
    score: float  # 0.0 to 1.0
    confidence: float  # 0.0 to 1.0
    evidence: List[str] | None = None


class BiasQuantifier:
    """Quantifies bias in knowledge sources"""

    def __init__(self):
        """Initialize bias quantifier"""
        self.bias_scores: Dict[str, BiasScore] = {}
        logger.info("BiasQuantifier initialized")

    def quantify_bias(self, source_id: str, source_type: str, content: Dict[str, Any]) -> BiasScore:
        """Quantify bias for a knowledge source

        Args:
            source_id: Source identifier
            source_type: Type of source
            content: Source content to analyze

        Returns:
            BiasScore object
        """
        # Simple bias detection patterns
        bias_patterns = {
            "eurocentric": ["western", "european", "american", "developed countries"],
            "publication": ["peer-reviewed", "high-impact", "citation count"],
            "contrarian": ["challenges", "contradicts", "alternative view"],
        }

        detected_biases = []
        max_score = 0.0
        bias_type = "none"

        text_content = str(content).lower()

        for bias_name, keywords in bias_patterns.items():
            matches = sum(1 for keyword in keywords if keyword in text_content)
            score = min(matches / len(keywords), 1.0)

            if score > max_score:
                max_score = score
                bias_type = bias_name

            if score > 0.3:  # Threshold for detection
                detected_biases.append(bias_name)

        bias_score = BiasScore(
            source_id=source_id,
            source_type=source_type,
            bias_type=bias_type,
            score=max_score,
            confidence=0.7 if max_score > 0.5 else 0.4,
            evidence=detected_biases if detected_biases else None,
        )

        self.bias_scores[source_id] = bias_score

        logger.info(f"✅ Quantified bias for {source_id}: {bias_type} (score: {max_score:.2f})")
        return bias_score

    def get_bias_score(self, source_id: str) -> BiasScore | None:
        """Get bias score for a source

        Args:
            source_id: Source identifier

        Returns:
            BiasScore or None
        """
        return self.bias_scores.get(source_id)

    def list_all_biases(self) -> List[BiasScore]:
        """List all bias scores

        Returns:
            List of all bias scores
        """
        return list(self.bias_scores.values())
