"""Continuous Refiner - Phase 26D Fase 4

Continuous refinement based on validation results.

Author: OmniMind Development
License: MIT
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List

from integrity.intelligent_integrator import IntegratedKnowledge, IntelligentIntegrator
from integrity.semantic_coherence_validator import (
    CoherenceReport,
    SemanticCoherenceValidator,
)

logger = logging.getLogger(__name__)


class ContinuousRefiner:
    """Continuous refinement based on validation results"""

    def __init__(
        self,
        intelligent_integrator: IntelligentIntegrator | None = None,
        coherence_validator: SemanticCoherenceValidator | None = None,
    ):
        """Initialize continuous refiner

        Args:
            intelligent_integrator: IntelligentIntegrator instance
            coherence_validator: SemanticCoherenceValidator instance
        """
        if intelligent_integrator is None:
            intelligent_integrator = IntelligentIntegrator()

        if coherence_validator is None:
            coherence_validator = SemanticCoherenceValidator()

        self.integrator = intelligent_integrator
        self.validator = coherence_validator
        self.refinement_history: List[Dict[str, Any]] = []

        logger.info("ContinuousRefiner initialized")

    def refine_knowledge(
        self,
        knowledge_id: str,
        validation_result: Dict[str, Any],
        was_correct: bool,
    ) -> IntegratedKnowledge | None:
        """Refine knowledge based on validation result

        Args:
            knowledge_id: Knowledge identifier
            validation_result: Result of using the knowledge
            was_correct: Whether the knowledge was correct

        Returns:
            Updated IntegratedKnowledge or None
        """
        # Get current integrated knowledge
        integrated = self.integrator.get_integrated_knowledge(knowledge_id)

        if not integrated:
            logger.warning(f"Knowledge {knowledge_id} not found for refinement")
            return None

        # Adjust confidence based on validation
        if was_correct:
            # Increase confidence
            new_confidence = min(integrated.confidence + 0.1, 1.0)
            logger.info(
                f"✅ Knowledge {knowledge_id} validated: "
                f"confidence {integrated.confidence:.2f} → {new_confidence:.2f}"
            )
        else:
            # Decrease confidence
            new_confidence = max(integrated.confidence - 0.15, 0.1)
            logger.warning(
                f"⚠️ Knowledge {knowledge_id} invalidated: "
                f"confidence {integrated.confidence:.2f} → {new_confidence:.2f}"
            )

        # Update confidence
        integrated.confidence = new_confidence

        # Update uncertainty flags
        if new_confidence < 0.6 and "low_confidence" not in integrated.uncertainty_flags:
            integrated.uncertainty_flags.append("low_confidence")
        elif new_confidence >= 0.6 and "low_confidence" in integrated.uncertainty_flags:
            integrated.uncertainty_flags.remove("low_confidence")

        # Record refinement
        self.refinement_history.append(
            {
                "knowledge_id": knowledge_id,
                "timestamp": validation_result.get("timestamp"),
                "was_correct": was_correct,
                "old_confidence": integrated.confidence - (0.1 if was_correct else -0.15),
                "new_confidence": new_confidence,
            }
        )

        return integrated

    def refine_based_on_coherence(self, coherence_report: CoherenceReport) -> Dict[str, Any]:
        """Refine knowledge base based on coherence report

        Args:
            coherence_report: Coherence validation report

        Returns:
            Refinement actions taken
        """
        actions = []

        # If coherence is low, suggest actions
        if coherence_report.coherence_score < 0.8:
            actions.append("Review and resolve conflicts")
            actions.append("Update conflicting knowledge with higher confidence")

        # If there are contradictions, prioritize resolution
        if coherence_report.contradictions > 0:
            actions.append(f"Resolve {coherence_report.contradictions} contradictions")

        # Record refinement
        self.refinement_history.append(
            {
                "type": "coherence_refinement",
                "coherence_score": coherence_report.coherence_score,
                "actions": actions,
            }
        )

        logger.info(
            f"✅ Refined based on coherence: score={coherence_report.coherence_score:.2f}, "
            f"actions={len(actions)}"
        )

        return {
            "actions": actions,
            "coherence_score": coherence_report.coherence_score,
            "recommendations": coherence_report.recommendations,
        }

    def get_refinement_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get refinement history

        Args:
            limit: Maximum number of entries to return

        Returns:
            List of refinement history entries
        """
        return self.refinement_history[-limit:] if limit > 0 else self.refinement_history

    def get_knowledge_quality_report(self) -> Dict[str, Any]:
        """Get overall knowledge quality report

        Returns:
            Quality report with statistics
        """
        all_integrated = self.integrator.list_all_integrated()

        if not all_integrated:
            return {
                "total_knowledge": 0,
                "average_confidence": 0.0,
                "high_confidence_count": 0,
                "low_confidence_count": 0,
            }

        total = len(all_integrated)
        avg_confidence = sum(k.confidence for k in all_integrated) / total
        high_confidence = sum(1 for k in all_integrated if k.confidence >= 0.7)
        low_confidence = sum(1 for k in all_integrated if k.confidence < 0.5)

        return {
            "total_knowledge": total,
            "average_confidence": avg_confidence,
            "high_confidence_count": high_confidence,
            "low_confidence_count": low_confidence,
            "refinement_actions": len(self.refinement_history),
        }
