"""Semantic Coherence Validator - Phase 26D Fase 3

Validates semantic coherence of knowledge base.

Author: OmniMind Development
License: MIT
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Dict, List

from integrity.conflict_detection_engine import ConflictDetectionEngine
from intelligence.semantic_search_engine import SemanticSearchEngine
from knowledge.knowledge_integrator import KnowledgeIntegrator

logger = logging.getLogger(__name__)


@dataclass
class CoherenceReport:
    """Semantic coherence validation report"""

    coherence_score: float  # 0.0 to 1.0
    total_entities: int
    conflicting_entities: int
    contradictions: int
    inconsistencies: int
    recommendations: List[str]
    details: Dict[str, Any] | None = None


class SemanticCoherenceValidator:
    """Validates semantic coherence of knowledge base"""

    def __init__(
        self,
        semantic_search: SemanticSearchEngine | None = None,
        knowledge_integrator: KnowledgeIntegrator | None = None,
        conflict_detector: ConflictDetectionEngine | None = None,
    ):
        """Initialize semantic coherence validator

        Args:
            semantic_search: SemanticSearchEngine instance
            knowledge_integrator: KnowledgeIntegrator instance
            conflict_detector: ConflictDetectionEngine instance
        """
        if semantic_search is None:
            semantic_search = SemanticSearchEngine()

        if knowledge_integrator is None:
            knowledge_integrator = KnowledgeIntegrator()

        if conflict_detector is None:
            conflict_detector = ConflictDetectionEngine()

        self.semantic_search = semantic_search
        self.knowledge_integrator = knowledge_integrator
        self.conflict_detector = conflict_detector

        logger.info("SemanticCoherenceValidator initialized")

    def validate_coherence(self, sample_queries: List[str] | None = None) -> CoherenceReport:
        """Validate semantic coherence of knowledge base

        Args:
            sample_queries: Sample queries to test (None = use defaults)

        Returns:
            CoherenceReport with validation results
        """
        if sample_queries is None:
            sample_queries = [
                "consciousness",
                "memory",
                "integration",
                "awareness",
            ]

        total_conflicts = 0
        contradictions = 0
        inconsistencies = 0
        conflicting_entities = set()

        # Check each query for conflicts
        for query in sample_queries:
            conflicts = self.conflict_detector.detect_conflicts(query)

            for conflict in conflicts:
                total_conflicts += 1
                if conflict.conflict_type == "contradiction":
                    contradictions += 1
                elif conflict.conflict_type == "incompatibility":
                    inconsistencies += 1

                # Track conflicting entities
                source1_name = conflict.source_1.get("name", "")
                source2_name = conflict.source_2.get("name", "")
                if source1_name:
                    conflicting_entities.add(source1_name)
                if source2_name:
                    conflicting_entities.add(source2_name)

        # Calculate coherence score
        total_entities = len(sample_queries) * 10  # Estimate
        coherence_score = self._calculate_coherence_score(
            total_conflicts, total_entities, contradictions, inconsistencies
        )

        # Generate recommendations
        recommendations = self._generate_recommendations(
            coherence_score, contradictions, inconsistencies
        )

        report = CoherenceReport(
            coherence_score=coherence_score,
            total_entities=total_entities,
            conflicting_entities=len(conflicting_entities),
            contradictions=contradictions,
            inconsistencies=inconsistencies,
            recommendations=recommendations,
            details={
                "sample_queries": sample_queries,
                "conflicting_entities": list(conflicting_entities),
            },
        )

        logger.info(
            f"✅ Coherence validation: score={coherence_score:.2f}, " f"conflicts={total_conflicts}"
        )
        return report

    def _calculate_coherence_score(
        self,
        total_conflicts: int,
        total_entities: int,
        contradictions: int,
        inconsistencies: int,
    ) -> float:
        """Calculate coherence score

        Args:
            total_conflicts: Total number of conflicts
            total_entities: Total number of entities
            contradictions: Number of contradictions
            inconsistencies: Number of inconsistencies

        Returns:
            Coherence score (0.0 to 1.0)
        """
        if total_entities == 0:
            return 1.0

        # Base score
        score = 1.0

        # Penalize for conflicts
        conflict_ratio = total_conflicts / total_entities
        score -= conflict_ratio * 0.5

        # Extra penalty for contradictions
        contradiction_ratio = contradictions / total_entities if total_entities > 0 else 0
        score -= contradiction_ratio * 0.3

        # Ensure minimum score
        return max(score, 0.0)

    def _generate_recommendations(
        self, coherence_score: float, contradictions: int, inconsistencies: int
    ) -> List[str]:
        """Generate recommendations for improving coherence

        Args:
            coherence_score: Coherence score
            contradictions: Number of contradictions
            inconsistencies: Number of inconsistencies

        Returns:
            List of recommendations
        """
        recommendations = []

        if coherence_score < 0.8:
            recommendations.append("Coherence score below target (0.8). Review conflicts.")

        if contradictions > 0:
            recommendations.append(f"Resolve {contradictions} contradictions in knowledge base.")

        if inconsistencies > 0:
            recommendations.append(f"Address {inconsistencies} inconsistencies in knowledge base.")

        if not recommendations:
            recommendations.append("Knowledge base is coherent. No action needed.")

        return recommendations

    def validate_entity_coherence(self, entity_name: str) -> Dict[str, Any]:
        """Validate coherence for a specific entity

        Args:
            entity_name: Entity name

        Returns:
            Validation results for entity
        """
        conflicts = self.conflict_detector.get_conflicts_for_entity(entity_name)

        return {
            "entity": entity_name,
            "conflicts": len(conflicts),
            "coherent": len(conflicts) == 0,
            "conflict_details": [
                {
                    "type": c.conflict_type,
                    "severity": c.severity,
                    "description": c.description,
                }
                for c in conflicts
            ],
        }
