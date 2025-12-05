"""Knowledge Integrator - Phase 26A

Integrates the 3 knowledge layers for cross-layer queries.

Author: OmniMind Development
License: MIT
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List

from knowledge.declarative_layer import DeclarativeLayer
from knowledge.episodic_layer import EpisodicLayer
from knowledge.procedural_layer import ProceduralLayer

logger = logging.getLogger(__name__)


class KnowledgeIntegrator:
    """Integra as 3 camadas de conhecimento"""

    def __init__(
        self,
        declarative: DeclarativeLayer | None = None,
        procedural: ProceduralLayer | None = None,
        episodic: EpisodicLayer | None = None,
    ):
        """Initialize knowledge integrator

        Args:
            declarative: DeclarativeLayer instance
            procedural: ProceduralLayer instance
            episodic: EpisodicLayer instance
        """
        self.declarative = declarative or DeclarativeLayer()
        self.procedural = procedural or ProceduralLayer()
        self.episodic = episodic or EpisodicLayer()

        logger.info("KnowledgeIntegrator initialized")

    def query(self, query: str, layers: List[str] | None = None) -> Dict[str, Any]:
        """Query across knowledge layers

        Args:
            query: Search query
            layers: Which layers to search (None = all)

        Returns:
            Dict with results from each layer
        """
        if layers is None:
            layers = ["declarative", "procedural", "episodic"]

        results: Dict[str, Any] = {}

        if "declarative" in layers:
            concepts = self.declarative.search_concepts(query, top_k=5)
            results["concepts"] = [
                {
                    "id": c.id,
                    "name": c.name,
                    "definition": c.definition,
                    "category": c.category,
                }
                for c in concepts
            ]

        if "procedural" in layers:
            rules = self.procedural.search_rules(query, top_k=5)
            results["rules"] = [
                {
                    "id": r.id,
                    "name": r.name,
                    "description": r.description,
                    "type": r.rule_type,
                }
                for r in rules
            ]

        if "episodic" in layers:
            # Episodic search is time-based, so we get recent episodes
            episodes = self.episodic.get_recent_episodes(limit=5)
            # Filter by query relevance (simple keyword match)
            relevant = [
                e
                for e in episodes
                if query.lower() in e.event.lower()
                or (e.learned and query.lower() in e.learned.lower())
            ]
            results["episodes"] = [
                {
                    "id": e.id,
                    "event": e.event,
                    "timestamp": e.timestamp.isoformat(),
                    "outcome": e.outcome,
                }
                for e in relevant[:5]
            ]

        return results

    def get_full_knowledge(self, entity_name: str) -> Dict[str, Any]:
        """Get complete knowledge about an entity across all layers

        Args:
            entity_name: Entity name to query

        Returns:
            Complete knowledge dict
        """
        # Search in all layers
        concepts = self.declarative.search_concepts(entity_name, top_k=3)
        rules = self.procedural.search_rules(entity_name, top_k=3)
        episodes = [
            e
            for e in self.episodic.get_recent_episodes(limit=20)
            if entity_name.lower() in e.event.lower()
        ][:3]

        return {
            "entity": entity_name,
            "concepts": [
                {
                    "id": c.id,
                    "name": c.name,
                    "definition": c.definition,
                    "category": c.category,
                }
                for c in concepts
            ],
            "rules": [
                {
                    "id": r.id,
                    "name": r.name,
                    "description": r.description,
                    "type": r.rule_type,
                }
                for r in rules
            ],
            "experiences": [
                {
                    "id": e.id,
                    "event": e.event,
                    "timestamp": e.timestamp.isoformat(),
                    "outcome": e.outcome,
                    "learned": e.learned,
                }
                for e in episodes
            ],
        }

    def get_statistics(self) -> Dict[str, int]:
        """Get statistics about stored knowledge

        Returns:
            Dict with counts per layer
        """
        return {
            "concepts": len(self.declarative.list_all_concepts()),
            "rules": len(self.procedural.list_all_rules()),
            "episodes": len(self.episodic.list_all_episodes()),
        }
