"""Intelligence Module - Phase 26B

Learning loop with 8B knowledge points:
- Semantic search on massive knowledge base
- Integration of 30+ curated datasets
- Context-aware reasoning
- Explanation generation

Author: OmniMind Development
License: MIT
"""

from __future__ import annotations

from intelligence.context_aware_reasoner import ContextAwareReasoner
from intelligence.dataset_integrator import DatasetIntegrator
from intelligence.learning_loop import LearningLoop
from intelligence.semantic_search_engine import SemanticSearchEngine

__all__ = [
    "SemanticSearchEngine",
    "DatasetIntegrator",
    "LearningLoop",
    "ContextAwareReasoner",
]
