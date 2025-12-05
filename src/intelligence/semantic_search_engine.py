"""Semantic Search Engine - Phase 26B Fase 1

Semantic search on 8B knowledge points.

Author: OmniMind Development
License: MIT
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List

from memory.semantic_memory_layer import SemanticMemoryLayer
from knowledge.knowledge_integrator import KnowledgeIntegrator

logger = logging.getLogger(__name__)


class SemanticSearchEngine:
    """Semantic search engine for 8B+ knowledge points"""

    def __init__(
        self,
        semantic_memory: SemanticMemoryLayer | None = None,
        knowledge_integrator: KnowledgeIntegrator | None = None,
    ):
        """Initialize semantic search engine

        Args:
            semantic_memory: SemanticMemoryLayer instance
            knowledge_integrator: KnowledgeIntegrator instance
        """
        if semantic_memory is None:
            from memory.semantic_memory_layer import get_semantic_memory

            semantic_memory = get_semantic_memory()

        if knowledge_integrator is None:
            knowledge_integrator = KnowledgeIntegrator()

        self.semantic_memory = semantic_memory
        self.knowledge_integrator = knowledge_integrator

        logger.info("SemanticSearchEngine initialized")

    def search(
        self, query: str, top_k: int = 10, layers: List[str] | None = None
    ) -> Dict[str, Any]:
        """Search across all knowledge layers

        Args:
            query: Search query
            top_k: Number of results per layer
            layers: Which layers to search (None = all)

        Returns:
            Dict with results from each layer
        """
        # Search in semantic memory (Phase 24)
        semantic_results = self.semantic_memory.retrieve_similar(query, top_k=top_k)

        # Search in knowledge layers (Phase 26A)
        knowledge_results = self.knowledge_integrator.query(query, layers=layers)

        return {
            "semantic_memory": semantic_results,
            "declarative": knowledge_results.get("concepts", []),
            "procedural": knowledge_results.get("rules", []),
            "episodic": knowledge_results.get("episodes", []),
            "total_results": len(semantic_results)
            + len(knowledge_results.get("concepts", []))
            + len(knowledge_results.get("rules", []))
            + len(knowledge_results.get("episodes", [])),
        }

    def search_with_context(
        self, query: str, context: Dict[str, Any], top_k: int = 10
    ) -> Dict[str, Any]:
        """Search with additional context

        Args:
            query: Search query
            context: Additional context (filters, preferences, etc.)
            top_k: Number of results

        Returns:
            Enhanced search results with context
        """
        # Base search
        results = self.search(query, top_k=top_k)

        # Apply context filters
        if "category" in context:
            results["declarative"] = [
                c for c in results["declarative"] if c.get("category") == context["category"]
            ]

        if "rule_type" in context:
            results["procedural"] = [
                r for r in results["procedural"] if r.get("type") == context["rule_type"]
            ]

        return results
