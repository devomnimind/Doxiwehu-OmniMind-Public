"""Declarative Knowledge Layer - Phase 26A

Layer 1: "O que são as coisas" (conceitos, definições)

Author: OmniMind Development
License: MIT
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List

from memory.semantic_memory_layer import SemanticMemoryLayer

logger = logging.getLogger(__name__)


@dataclass
class Concept:
    """Concept definition"""

    id: str
    name: str
    definition: str
    category: str | None = None
    properties: Dict[str, Any] | None = None
    timestamp: datetime | None = None

    def __post_init__(self) -> None:
        """Set default timestamp"""
        if self.timestamp is None:
            self.timestamp = datetime.now(timezone.utc)


class DeclarativeLayer:
    """Armazena conceitos e definições (Layer 1)"""

    def __init__(self, semantic_memory: SemanticMemoryLayer | None = None):
        """Initialize declarative layer

        Args:
            semantic_memory: SemanticMemoryLayer instance (optional)
        """
        if semantic_memory is None:
            from memory.semantic_memory_layer import get_semantic_memory

            semantic_memory = get_semantic_memory()

        self.semantic_memory = semantic_memory
        self.concepts: Dict[str, Concept] = {}

        logger.info("DeclarativeLayer initialized")

    def store_concept(self, concept: Concept) -> str:
        """Store a concept in declarative layer

        Args:
            concept: Concept to store

        Returns:
            Concept ID
        """
        # Store in memory
        self.concepts[concept.id] = concept

        # Store in semantic memory (Phase 24)
        concept_text = f"{concept.name}: {concept.definition}"
        concept_data = {
            "type": "declarative_concept",
            "concept_id": concept.id,
            "name": concept.name,
            "category": concept.category,
            "properties": concept.properties or {},
        }

        self.semantic_memory.store_episode(
            episode_text=concept_text,
            episode_data=concept_data,
            timestamp=concept.timestamp or datetime.now(timezone.utc),
        )

        logger.info(f"Stored concept: {concept.name} (ID: {concept.id})")
        return concept.id

    def get_concept(self, concept_id: str) -> Concept | None:
        """Get concept by ID

        Args:
            concept_id: Concept identifier

        Returns:
            Concept or None
        """
        return self.concepts.get(concept_id)

    def search_concepts(self, query: str, top_k: int = 10) -> List[Concept]:
        """Search concepts by semantic similarity

        Args:
            query: Search query
            top_k: Number of results

        Returns:
            List of matching concepts
        """
        # Search in semantic memory
        results = self.semantic_memory.retrieve_similar(query, top_k=top_k)

        # Map to concepts
        concepts = []
        for result in results:
            concept_id = result.get("concept_id")
            if concept_id and concept_id in self.concepts:
                concepts.append(self.concepts[concept_id])

        return concepts

    def get_concepts_by_category(self, category: str) -> List[Concept]:
        """Get all concepts in a category

        Args:
            category: Category name

        Returns:
            List of concepts
        """
        return [c for c in self.concepts.values() if c.category == category]

    def list_all_concepts(self) -> List[Concept]:
        """List all stored concepts

        Returns:
            List of all concepts
        """
        return list(self.concepts.values())
