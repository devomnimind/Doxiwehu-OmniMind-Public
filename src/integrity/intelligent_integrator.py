"""Intelligent Integrator - Phase 26D Fase 2

Intelligent integration with uncertainty flags.

Author: OmniMind Development
License: MIT
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Dict, List

from integrity.bias_quantifier import BiasQuantifier, BiasScore
from integrity.conflict_detection_engine import Conflict, ConflictDetectionEngine

logger = logging.getLogger(__name__)


@dataclass
class IntegratedKnowledge:
    """Knowledge integrated with uncertainty flags"""

    knowledge_id: str
    content: Dict[str, Any]
    confidence: float  # 0.0 to 1.0
    uncertainty_flags: List[str]  # ["bias", "conflict", "low_confidence"]
    bias_score: BiasScore | None = None
    conflicts: List[Conflict] | None = None
    source_metadata: Dict[str, Any] | None = None


class IntelligentIntegrator:
    """Intelligent integration with uncertainty flags"""

    def __init__(
        self,
        conflict_detector: ConflictDetectionEngine | None = None,
        bias_quantifier: BiasQuantifier | None = None,
    ):
        """Initialize intelligent integrator

        Args:
            conflict_detector: ConflictDetectionEngine instance
            bias_quantifier: BiasQuantifier instance
        """
        if conflict_detector is None:
            conflict_detector = ConflictDetectionEngine()

        if bias_quantifier is None:
            bias_quantifier = BiasQuantifier()

        self.conflict_detector = conflict_detector
        self.bias_quantifier = bias_quantifier
        self.integrated_knowledge: Dict[str, IntegratedKnowledge] = {}

        logger.info("IntelligentIntegrator initialized")

    def integrate_knowledge(
        self,
        knowledge_id: str,
        content: Dict[str, Any],
        source_type: str = "unknown",
        source_metadata: Dict[str, Any] | None = None,
    ) -> IntegratedKnowledge:
        """Integrate knowledge with uncertainty flags

        Args:
            knowledge_id: Knowledge identifier
            content: Knowledge content
            source_type: Type of source
            source_metadata: Additional source metadata

        Returns:
            IntegratedKnowledge with uncertainty flags
        """
        # Check for conflicts
        conflicts = self.conflict_detector.detect_conflicts(str(content.get("name", knowledge_id)))

        # Quantify bias
        bias_score = self.bias_quantifier.quantify_bias(knowledge_id, source_type, content)

        # Calculate confidence
        confidence = self._calculate_confidence(bias_score, conflicts)

        # Determine uncertainty flags
        uncertainty_flags = self._determine_uncertainty_flags(bias_score, conflicts, confidence)

        integrated = IntegratedKnowledge(
            knowledge_id=knowledge_id,
            content=content,
            confidence=confidence,
            uncertainty_flags=uncertainty_flags,
            bias_score=bias_score,
            conflicts=conflicts if conflicts else None,
            source_metadata=source_metadata,
        )

        self.integrated_knowledge[knowledge_id] = integrated

        logger.info(
            f"✅ Integrated knowledge: {knowledge_id} "
            f"(confidence: {confidence:.2f}, flags: {uncertainty_flags})"
        )
        return integrated

    def _calculate_confidence(self, bias_score: BiasScore, conflicts: List[Conflict]) -> float:
        """Calculate confidence score

        Args:
            bias_score: Bias score
            conflicts: List of conflicts

        Returns:
            Confidence score (0.0 to 1.0)
        """
        # Start with base confidence
        confidence = 1.0

        # Reduce for bias
        if bias_score.score > 0.5:
            confidence -= 0.2
        elif bias_score.score > 0.3:
            confidence -= 0.1

        # Reduce for conflicts
        if conflicts:
            severity_sum = sum(c.severity for c in conflicts)
            confidence -= min(severity_sum * 0.1, 0.3)

        # Ensure minimum confidence
        return max(confidence, 0.1)

    def _determine_uncertainty_flags(
        self,
        bias_score: BiasScore,
        conflicts: List[Conflict],
        confidence: float,
    ) -> List[str]:
        """Determine uncertainty flags

        Args:
            bias_score: Bias score
            conflicts: List of conflicts
            confidence: Confidence score

        Returns:
            List of uncertainty flags
        """
        flags = []

        if bias_score.score > 0.5:
            flags.append("bias")
        if conflicts:
            flags.append("conflict")
        if confidence < 0.6:
            flags.append("low_confidence")

        return flags

    def get_integrated_knowledge(self, knowledge_id: str) -> IntegratedKnowledge | None:
        """Get integrated knowledge by ID

        Args:
            knowledge_id: Knowledge identifier

        Returns:
            IntegratedKnowledge or None
        """
        return self.integrated_knowledge.get(knowledge_id)

    def list_all_integrated(self) -> List[IntegratedKnowledge]:
        """List all integrated knowledge

        Returns:
            List of all integrated knowledge
        """
        return list(self.integrated_knowledge.values())
