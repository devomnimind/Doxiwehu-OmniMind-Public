"""Dataset Integrator - Phase 26B Fase 2

Integration of 30+ curated datasets.

Author: OmniMind Development
License: MIT
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict, List

from knowledge.declarative_layer import Concept, DeclarativeLayer
from knowledge.procedural_layer import ProceduralLayer, Rule
from memory.semantic_memory_layer import SemanticMemoryLayer

logger = logging.getLogger(__name__)


class DatasetIntegrator:
    """Integrates multiple datasets into knowledge layers"""

    def __init__(
        self,
        declarative: DeclarativeLayer | None = None,
        procedural: ProceduralLayer | None = None,
        semantic_memory: SemanticMemoryLayer | None = None,
    ):
        """Initialize dataset integrator

        Args:
            declarative: DeclarativeLayer instance
            procedural: ProceduralLayer instance
            semantic_memory: SemanticMemoryLayer instance
        """
        if declarative is None:
            declarative = DeclarativeLayer()

        if procedural is None:
            procedural = ProceduralLayer()

        if semantic_memory is None:
            from memory.semantic_memory_layer import get_semantic_memory

            semantic_memory = get_semantic_memory()

        self.declarative = declarative
        self.procedural = procedural
        self.semantic_memory = semantic_memory

        logger.info("DatasetIntegrator initialized")

    def integrate_dataset(self, dataset_path: Path, dataset_type: str = "auto") -> Dict[str, int]:
        """Integrate a dataset into knowledge layers

        Args:
            dataset_path: Path to dataset file
            dataset_type: Type of dataset ("concepts", "rules", "auto")

        Returns:
            Dict with integration statistics
        """
        if not dataset_path.exists():
            logger.warning(f"Dataset not found: {dataset_path}")
            return {"concepts": 0, "rules": 0, "episodes": 0}

        # Load dataset
        import json

        with open(dataset_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        stats = {"concepts": 0, "rules": 0, "episodes": 0}

        # Auto-detect type
        if dataset_type == "auto":
            if (
                "concepts" in data
                or isinstance(data, list)
                and all("name" in item and "definition" in item for item in data[:5])
            ):
                dataset_type = "concepts"
            elif (
                "rules" in data
                or isinstance(data, list)
                and all("name" in item and "description" in item for item in data[:5])
            ):
                dataset_type = "rules"

        # Integrate based on type
        if dataset_type == "concepts":
            concepts_data = data.get("concepts", data) if isinstance(data, dict) else data
            for item in concepts_data:
                if isinstance(item, dict):
                    concept = Concept(
                        id=item.get("id", f"concept_{stats['concepts']}"),
                        name=item.get("name", ""),
                        definition=item.get("definition", ""),
                        category=item.get("category"),
                    )
                    self.declarative.store_concept(concept)
                    stats["concepts"] += 1

        elif dataset_type == "rules":
            rules_data = data.get("rules", data) if isinstance(data, dict) else data
            for item in rules_data:
                if isinstance(item, dict):
                    rule = Rule(
                        id=item.get("id", f"rule_{stats['rules']}"),
                        name=item.get("name", ""),
                        description=item.get("description", ""),
                        rule_type=item.get("rule_type", "rule"),
                        conditions=item.get("conditions"),
                        actions=item.get("actions"),
                    )
                    self.procedural.store_rule(rule)
                    stats["rules"] += 1

        logger.info(f"✅ Integrated dataset: {stats}")
        return stats

    def integrate_multiple_datasets(
        self, dataset_paths: List[Path], dataset_types: List[str] | None = None
    ) -> Dict[str, int]:
        """Integrate multiple datasets

        Args:
            dataset_paths: List of dataset paths
            dataset_types: List of dataset types (None = auto-detect all)

        Returns:
            Total integration statistics
        """
        total_stats = {"concepts": 0, "rules": 0, "episodes": 0}

        if dataset_types is None:
            dataset_types = ["auto"] * len(dataset_paths)

        for path, dtype in zip(dataset_paths, dataset_types):
            stats = self.integrate_dataset(path, dtype)
            total_stats["concepts"] += stats["concepts"]
            total_stats["rules"] += stats["rules"]
            total_stats["episodes"] += stats["episodes"]

        logger.info(f"✅ Integrated {len(dataset_paths)} datasets: {total_stats}")
        return total_stats
