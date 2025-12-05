"""Learning Loop - Phase 26B

Continuous learning from knowledge base and experiences.

Author: OmniMind Development
License: MIT
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List

from intelligence.dataset_integrator import DatasetIntegrator
from intelligence.semantic_search_engine import SemanticSearchEngine
from knowledge.episodic_layer import Episode, EpisodicLayer
from knowledge.knowledge_integrator import KnowledgeIntegrator

logger = logging.getLogger(__name__)


class LearningLoop:
    """Continuous learning loop that learns from experiences"""

    def __init__(
        self,
        semantic_search: SemanticSearchEngine | None = None,
        dataset_integrator: DatasetIntegrator | None = None,
        knowledge_integrator: KnowledgeIntegrator | None = None,
        episodic_layer: EpisodicLayer | None = None,
    ):
        """Initialize learning loop

        Args:
            semantic_search: SemanticSearchEngine instance
            dataset_integrator: DatasetIntegrator instance
            knowledge_integrator: KnowledgeIntegrator instance
            episodic_layer: EpisodicLayer instance
        """
        if semantic_search is None:
            semantic_search = SemanticSearchEngine()

        if dataset_integrator is None:
            dataset_integrator = DatasetIntegrator()

        if knowledge_integrator is None:
            knowledge_integrator = KnowledgeIntegrator()

        if episodic_layer is None:
            episodic_layer = EpisodicLayer()

        self.semantic_search = semantic_search
        self.dataset_integrator = dataset_integrator
        self.knowledge_integrator = knowledge_integrator
        self.episodic_layer = episodic_layer

        logger.info("LearningLoop initialized")

    def learn_from_query(self, query: str, context: Dict[str, Any] | None = None) -> Dict[str, Any]:
        """Learn from a query by searching and storing insights

        Args:
            query: Search query
            context: Additional context

        Returns:
            Learning results with insights
        """
        # Search for relevant knowledge
        if context:
            results = self.semantic_search.search_with_context(query, context)
        else:
            results = self.semantic_search.search(query)

        # Extract insights
        insights = {
            "query": query,
            "concepts_found": len(results.get("declarative", [])),
            "rules_found": len(results.get("procedural", [])),
            "experiences_found": len(results.get("episodic", [])),
            "total_knowledge": results.get("total_results", 0),
        }

        # Store as episode
        from datetime import datetime, timezone

        episode = Episode(
            id=f"learn_{datetime.now(timezone.utc).timestamp()}",
            timestamp=datetime.now(timezone.utc),
            event=f"Learned from query: {query}",
            context=context or {},
            learned=f"Found {insights['total_knowledge']} relevant knowledge points",
        )
        self.episodic_layer.store_episode(episode)

        logger.info(f"✅ Learned from query: {query} ({insights['total_knowledge']} points)")
        return insights

    def learn_from_datasets(
        self, dataset_paths: List[str], dataset_types: List[str] | None = None
    ) -> Dict[str, int]:
        """Learn by integrating datasets

        Args:
            dataset_paths: List of dataset file paths
            dataset_types: List of dataset types (None = auto-detect)

        Returns:
            Integration statistics
        """
        from pathlib import Path

        paths = [Path(p) for p in dataset_paths]
        stats = self.dataset_integrator.integrate_multiple_datasets(paths, dataset_types)

        # Store as episode
        from datetime import datetime, timezone

        episode = Episode(
            id=f"learn_datasets_{datetime.now(timezone.utc).timestamp()}",
            timestamp=datetime.now(timezone.utc),
            event=f"Integrated {len(dataset_paths)} datasets",
            learned=f"Added {stats['concepts']} concepts, {stats['rules']} rules",
        )
        self.episodic_layer.store_episode(episode)

        logger.info(f"✅ Learned from {len(dataset_paths)} datasets: {stats}")
        return stats
