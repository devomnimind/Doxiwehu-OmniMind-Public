"""Tests for DatasetIntegrator - Phase 26B"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from intelligence.dataset_integrator import DatasetIntegrator


class TestDatasetIntegrator:
    """Test DatasetIntegrator"""

    @pytest.fixture
    def mock_declarative(self):
        """Mock DeclarativeLayer"""
        mock = MagicMock()
        return mock

    @pytest.fixture
    def mock_procedural(self):
        """Mock ProceduralLayer"""
        mock = MagicMock()
        return mock

    @pytest.fixture
    def mock_semantic_memory(self):
        """Mock SemanticMemoryLayer"""
        mock = MagicMock()
        return mock

    @pytest.fixture
    def temp_dataset_concepts(self, tmp_path: Path) -> Path:
        """Create temporary concepts dataset"""
        dataset_file = tmp_path / "concepts.json"
        data = {
            "concepts": [
                {"id": "c1", "name": "Concept1", "definition": "Definition1", "category": "cat1"},
                {"id": "c2", "name": "Concept2", "definition": "Definition2", "category": "cat2"},
            ]
        }
        dataset_file.write_text(json.dumps(data, indent=2))
        return dataset_file

    @pytest.fixture
    def temp_dataset_rules(self, tmp_path: Path) -> Path:
        """Create temporary rules dataset"""
        dataset_file = tmp_path / "rules.json"
        data = {
            "rules": [
                {
                    "id": "r1",
                    "name": "Rule1",
                    "description": "Description1",
                    "rule_type": "process",
                    "conditions": ["cond1"],
                    "actions": ["action1"],
                },
                {
                    "id": "r2",
                    "name": "Rule2",
                    "description": "Description2",
                    "rule_type": "rule",
                },
            ]
        }
        dataset_file.write_text(json.dumps(data, indent=2))
        return dataset_file

    def test_init_default(self):
        """Test initialization with defaults"""
        with (
            patch("intelligence.dataset_integrator.DeclarativeLayer") as mock_decl,
            patch("intelligence.dataset_integrator.ProceduralLayer") as mock_proc,
            patch("memory.semantic_memory_layer.get_semantic_memory") as mock_get,
        ):
            mock_decl.return_value = MagicMock()
            mock_proc.return_value = MagicMock()
            mock_get.return_value = MagicMock()

            integrator = DatasetIntegrator()

            assert integrator.declarative is not None
            assert integrator.procedural is not None
            assert integrator.semantic_memory is not None

    def test_init_with_dependencies(self, mock_declarative, mock_procedural, mock_semantic_memory):
        """Test initialization with provided dependencies"""
        integrator = DatasetIntegrator(
            declarative=mock_declarative,
            procedural=mock_procedural,
            semantic_memory=mock_semantic_memory,
        )

        assert integrator.declarative == mock_declarative
        assert integrator.procedural == mock_procedural
        assert integrator.semantic_memory == mock_semantic_memory

    def test_integrate_dataset_concepts(
        self, mock_declarative, mock_procedural, mock_semantic_memory, temp_dataset_concepts
    ):
        """Test integrating concepts dataset"""
        integrator = DatasetIntegrator(
            declarative=mock_declarative,
            procedural=mock_procedural,
            semantic_memory=mock_semantic_memory,
        )

        stats = integrator.integrate_dataset(temp_dataset_concepts, dataset_type="concepts")

        assert stats["concepts"] == 2
        assert stats["rules"] == 0
        assert mock_declarative.store_concept.call_count == 2

    def test_integrate_dataset_rules(
        self, mock_declarative, mock_procedural, mock_semantic_memory, temp_dataset_rules
    ):
        """Test integrating rules dataset"""
        integrator = DatasetIntegrator(
            declarative=mock_declarative,
            procedural=mock_procedural,
            semantic_memory=mock_semantic_memory,
        )

        stats = integrator.integrate_dataset(temp_dataset_rules, dataset_type="rules")

        assert stats["concepts"] == 0
        assert stats["rules"] == 2
        assert mock_procedural.store_rule.call_count == 2

    def test_integrate_dataset_auto_detect_concepts(
        self, mock_declarative, mock_procedural, mock_semantic_memory, temp_dataset_concepts
    ):
        """Test auto-detection of concepts dataset"""
        integrator = DatasetIntegrator(
            declarative=mock_declarative,
            procedural=mock_procedural,
            semantic_memory=mock_semantic_memory,
        )

        stats = integrator.integrate_dataset(temp_dataset_concepts, dataset_type="auto")

        assert stats["concepts"] == 2
        assert stats["rules"] == 0

    def test_integrate_dataset_nonexistent(
        self, mock_declarative, mock_procedural, mock_semantic_memory, tmp_path: Path
    ):
        """Test integrating nonexistent dataset"""
        integrator = DatasetIntegrator(
            declarative=mock_declarative,
            procedural=mock_procedural,
            semantic_memory=mock_semantic_memory,
        )

        nonexistent = tmp_path / "nonexistent.json"
        stats = integrator.integrate_dataset(nonexistent)

        assert stats["concepts"] == 0
        assert stats["rules"] == 0
        assert stats["episodes"] == 0

    def test_integrate_multiple_datasets(
        self,
        mock_declarative,
        mock_procedural,
        mock_semantic_memory,
        temp_dataset_concepts,
        temp_dataset_rules,
    ):
        """Test integrating multiple datasets"""
        integrator = DatasetIntegrator(
            declarative=mock_declarative,
            procedural=mock_procedural,
            semantic_memory=mock_semantic_memory,
        )

        stats = integrator.integrate_multiple_datasets(
            [temp_dataset_concepts, temp_dataset_rules],
            dataset_types=["concepts", "rules"],
        )

        assert stats["concepts"] == 2
        assert stats["rules"] == 2
        assert mock_declarative.store_concept.call_count == 2
        assert mock_procedural.store_rule.call_count == 2

    def test_integrate_multiple_datasets_auto(
        self,
        mock_declarative,
        mock_procedural,
        mock_semantic_memory,
        temp_dataset_concepts,
        temp_dataset_rules,
    ):
        """Test integrating multiple datasets with auto-detection"""
        integrator = DatasetIntegrator(
            declarative=mock_declarative,
            procedural=mock_procedural,
            semantic_memory=mock_semantic_memory,
        )

        stats = integrator.integrate_multiple_datasets([temp_dataset_concepts, temp_dataset_rules])

        assert stats["concepts"] == 2
        assert stats["rules"] == 2
