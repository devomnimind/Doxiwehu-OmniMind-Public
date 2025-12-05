"""Procedural Knowledge Layer - Phase 26A

Layer 2: "Como se relacionam" (regras, processos)

Author: OmniMind Development
License: MIT
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, List

from memory.semantic_memory_layer import SemanticMemoryLayer

logger = logging.getLogger(__name__)


@dataclass
class Rule:
    """Rule or process definition"""

    id: str
    name: str
    description: str
    rule_type: str  # "rule", "process", "procedure"
    conditions: List[str] | None = None
    actions: List[str] | None = None
    relations: Dict[str, str] | None = None  # subject -> predicate -> object
    timestamp: datetime | None = None

    def __post_init__(self) -> None:
        """Set default timestamp"""
        if self.timestamp is None:
            self.timestamp = datetime.now(timezone.utc)


class ProceduralLayer:
    """Armazena regras e processos (Layer 2)"""

    def __init__(self, semantic_memory: SemanticMemoryLayer | None = None):
        """Initialize procedural layer

        Args:
            semantic_memory: SemanticMemoryLayer instance (optional)
        """
        if semantic_memory is None:
            from memory.semantic_memory_layer import get_semantic_memory

            semantic_memory = get_semantic_memory()

        self.semantic_memory = semantic_memory
        self.rules: Dict[str, Rule] = {}

        logger.info("ProceduralLayer initialized")

    def store_rule(self, rule: Rule) -> str:
        """Store a rule/process in procedural layer

        Args:
            rule: Rule to store

        Returns:
            Rule ID
        """
        # Store in memory
        self.rules[rule.id] = rule

        # Store in semantic memory (Phase 24)
        rule_text = f"{rule.name}: {rule.description}"
        rule_data = {
            "type": "procedural_rule",
            "rule_id": rule.id,
            "name": rule.name,
            "rule_type": rule.rule_type,
            "conditions": rule.conditions or [],
            "actions": rule.actions or [],
            "relations": rule.relations or {},
        }

        self.semantic_memory.store_episode(
            episode_text=rule_text,
            episode_data=rule_data,
            timestamp=rule.timestamp or datetime.now(timezone.utc),
        )

        logger.info(f"Stored rule: {rule.name} (ID: {rule.id})")
        return rule.id

    def get_rule(self, rule_id: str) -> Rule | None:
        """Get rule by ID

        Args:
            rule_id: Rule identifier

        Returns:
            Rule or None
        """
        return self.rules.get(rule_id)

    def search_rules(self, query: str, top_k: int = 10) -> List[Rule]:
        """Search rules by semantic similarity

        Args:
            query: Search query
            top_k: Number of results

        Returns:
            List of matching rules
        """
        # Search in semantic memory
        results = self.semantic_memory.retrieve_similar(query, top_k=top_k)

        # Map to rules
        rules = []
        for result in results:
            rule_id = result.get("rule_id")
            if rule_id and rule_id in self.rules:
                rules.append(self.rules[rule_id])

        return rules

    def get_rules_by_type(self, rule_type: str) -> List[Rule]:
        """Get all rules of a specific type

        Args:
            rule_type: Rule type ("rule", "process", "procedure")

        Returns:
            List of rules
        """
        return [r for r in self.rules.values() if r.rule_type == rule_type]

    def list_all_rules(self) -> List[Rule]:
        """List all stored rules

        Returns:
            List of all rules
        """
        return list(self.rules.values())
