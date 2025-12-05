"""Context-Aware Reasoner - Phase 26B

Context-aware reasoning with explanation generation.

Author: OmniMind Development
License: MIT
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List

from intelligence.semantic_search_engine import SemanticSearchEngine
from knowledge.knowledge_integrator import KnowledgeIntegrator

logger = logging.getLogger(__name__)


class ContextAwareReasoner:
    """Context-aware reasoning with explanation generation"""

    def __init__(
        self,
        semantic_search: SemanticSearchEngine | None = None,
        knowledge_integrator: KnowledgeIntegrator | None = None,
    ):
        """Initialize context-aware reasoner

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

        logger.info("ContextAwareReasoner initialized")

    def reason(self, query: str, context: Dict[str, Any] | None = None) -> Dict[str, Any]:
        """Reason about a query with context

        Args:
            query: Query to reason about
            context: Additional context (filters, preferences, history)

        Returns:
            Reasoning results with explanation
        """
        # Search with context
        if context:
            results = self.semantic_search.search_with_context(query, context)
        else:
            results = self.semantic_search.search(query)

        # Get full knowledge about key entities
        key_concepts = [c.get("name", "") for c in results.get("declarative", [])[:3]]
        full_knowledge = {}
        for concept in key_concepts:
            if concept:
                full_knowledge[concept] = self.knowledge_integrator.get_full_knowledge(concept)

        # Generate explanation
        explanation = self._generate_explanation(query, results, full_knowledge, context)

        return {
            "query": query,
            "context": context or {},
            "results": results,
            "full_knowledge": full_knowledge,
            "explanation": explanation,
        }

    def _generate_explanation(
        self,
        query: str,
        results: Dict[str, Any],
        full_knowledge: Dict[str, Any],
        context: Dict[str, Any] | None,
    ) -> str:
        """Generate human-readable explanation

        Args:
            query: Original query
            results: Search results
            full_knowledge: Full knowledge about key entities
            context: Additional context

        Returns:
            Explanation string
        """
        total = results.get("total_results", 0)
        concepts = len(results.get("declarative", []))
        rules = len(results.get("procedural", []))
        episodes = len(results.get("episodic", []))

        explanation_parts = [
            f"Query: '{query}'",
            f"Found {total} relevant knowledge points:",
            f"  - {concepts} concepts",
            f"  - {rules} rules/processes",
            f"  - {episodes} experiences",
        ]

        if full_knowledge:
            explanation_parts.append("\nKey entities:")
            for entity, knowledge in list(full_knowledge.items())[:3]:
                if knowledge.get("concepts"):
                    explanation_parts.append(f"  - {entity}: {len(knowledge['concepts'])} concepts")

        if context:
            explanation_parts.append(f"\nContext applied: {list(context.keys())}")

        return "\n".join(explanation_parts)

    def explain_decision(self, decision: str, reasoning_steps: List[Dict[str, Any]]) -> str:
        """Explain a decision with reasoning steps

        Args:
            decision: The decision made
            reasoning_steps: List of reasoning steps

        Returns:
            Explanation of the decision
        """
        explanation = [f"Decision: {decision}", "\nReasoning steps:"]

        for i, step in enumerate(reasoning_steps, 1):
            step_type = step.get("type", "unknown")
            step_info = step.get("info", "")
            explanation.append(f"{i}. [{step_type}] {step_info}")

        return "\n".join(explanation)
