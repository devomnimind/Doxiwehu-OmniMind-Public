"""Conflict Detection Engine - Phase 26D Fase 1

Detects conflicts and contradictions in knowledge base.

Author: OmniMind Development
License: MIT
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Dict, List

from intelligence.semantic_search_engine import SemanticSearchEngine
from knowledge.knowledge_integrator import KnowledgeIntegrator

logger = logging.getLogger(__name__)


@dataclass
class Conflict:
    """Detected conflict between knowledge points"""

    conflict_id: str
    source_1: Dict[str, Any]
    source_2: Dict[str, Any]
    conflict_type: str  # "contradiction", "incompatibility", "uncertainty"
    severity: float  # 0.0 to 1.0
    description: str
    resolution_suggestion: str | None = None


class ConflictDetectionEngine:
    """Detects conflicts and contradictions in knowledge"""

    def __init__(
        self,
        semantic_search: SemanticSearchEngine | None = None,
        knowledge_integrator: KnowledgeIntegrator | None = None,
    ):
        """Initialize conflict detection engine

        Args:
            semantic_search: SemanticSearchEngine instance
            knowledge_integrator: KnowledgeIntegrator instance
        """
        if semantic_search is None:
            semantic_search = SemanticSearchEngine()

        if knowledge_integrator is None:
            knowledge_integrator = KnowledgeIntegrator()

        self.semantic_search = semantic_search
        self.knowledge_integrator = knowledge_integrator
        self.detected_conflicts: Dict[str, Conflict] = {}

        logger.info("ConflictDetectionEngine initialized")

    def detect_conflicts(self, query: str, threshold: float = 0.7) -> List[Conflict]:
        """Detect conflicts for a given query

        Args:
            query: Query to check for conflicts
            threshold: Similarity threshold for conflict detection

        Returns:
            List of detected conflicts
        """
        # Search for knowledge about the query
        results = self.semantic_search.search(query, top_k=20)

        conflicts = []

        # Check concepts for contradictions
        concepts = results.get("declarative", [])
        for i, concept1 in enumerate(concepts):
            for concept2 in concepts[i + 1 :]:
                conflict = self._check_concept_conflict(concept1, concept2, query)
                if conflict:
                    conflicts.append(conflict)

        # Check rules for incompatibilities
        rules = results.get("procedural", [])
        for i, rule1 in enumerate(rules):
            for rule2 in rules[i + 1 :]:
                conflict = self._check_rule_conflict(rule1, rule2, query)
                if conflict:
                    conflicts.append(conflict)

        # Store conflicts
        for conflict in conflicts:
            self.detected_conflicts[conflict.conflict_id] = conflict

        logger.info(f"✅ Detected {len(conflicts)} conflicts for query: {query}")
        return conflicts

    def _check_concept_conflict(
        self, concept1: Dict[str, Any], concept2: Dict[str, Any], query: str
    ) -> Conflict | None:
        """Check if two concepts conflict

        Args:
            concept1: First concept
            concept2: Second concept
            query: Original query

        Returns:
            Conflict if detected, None otherwise
        """
        # Simple contradiction detection based on definitions
        def1 = concept1.get("definition", "").lower()
        def2 = concept2.get("definition", "").lower()

        # Check for explicit contradictions
        contradiction_keywords = [
            ("requires", "isolated"),
            ("needs", "does not need"),
            ("must", "cannot"),
            ("always", "never"),
        ]

        for keyword1, keyword2 in contradiction_keywords:
            if keyword1 in def1 and keyword2 in def2:
                return Conflict(
                    conflict_id=f"conflict_{len(self.detected_conflicts)}",
                    source_1=concept1,
                    source_2=concept2,
                    conflict_type="contradiction",
                    severity=0.8,
                    description=(
                        f"Contradiction detected: {concept1.get('name')} vs "
                        f"{concept2.get('name')}"
                    ),
                    resolution_suggestion="Review both definitions and reconcile",
                )

        return None

    def _check_rule_conflict(
        self, rule1: Dict[str, Any], rule2: Dict[str, Any], query: str
    ) -> Conflict | None:
        """Check if two rules conflict

        Args:
            rule1: First rule
            rule2: Second rule
            query: Original query

        Returns:
            Conflict if detected, None otherwise
        """
        # Check for incompatible actions
        actions1 = rule1.get("actions", [])
        actions2 = rule2.get("actions", [])

        # Simple incompatibility check
        incompatible_pairs = [
            ("enable", "disable"),
            ("increase", "decrease"),
            ("add", "remove"),
        ]

        for action1 in actions1:
            for action2 in actions2:
                for pair in incompatible_pairs:
                    if pair[0] in action1.lower() and pair[1] in action2.lower():
                        return Conflict(
                            conflict_id=f"conflict_{len(self.detected_conflicts)}",
                            source_1=rule1,
                            source_2=rule2,
                            conflict_type="incompatibility",
                            severity=0.6,
                            description=(
                                f"Incompatible actions: {rule1.get('name')} vs "
                                f"{rule2.get('name')}"
                            ),
                            resolution_suggestion="Prioritize based on context",
                        )

        return None

    def get_conflicts_for_entity(self, entity_name: str) -> List[Conflict]:
        """Get all conflicts related to an entity

        Args:
            entity_name: Entity name

        Returns:
            List of conflicts
        """
        return [
            c
            for c in self.detected_conflicts.values()
            if entity_name.lower()
            in (c.source_1.get("name", "") + c.source_2.get("name", "")).lower()
        ]

    def list_all_conflicts(self) -> List[Conflict]:
        """List all detected conflicts

        Returns:
            List of all conflicts
        """
        return list(self.detected_conflicts.values())
