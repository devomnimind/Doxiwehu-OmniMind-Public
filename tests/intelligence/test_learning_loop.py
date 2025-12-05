"""Tests for LearningLoop - Phase 26B"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from intelligence.learning_loop import LearningLoop


class TestLearningLoop:
    """Test LearningLoop"""

    @pytest.fixture
    def mock_semantic_search(self):
        """Mock SemanticSearchEngine"""
        mock = MagicMock()
        mock.search.return_value = {
            "declarative": [{"name": "concept1"}],
            "procedural": [{"name": "rule1"}],
            "episodic": [{"event": "episode1"}],
            "total_results": 3,
        }
        mock.search_with_context.return_value = {
            "declarative": [{"name": "concept1"}],
            "procedural": [],
            "episodic": [],
            "total_results": 1,
        }
        return mock

    @pytest.fixture
    def mock_dataset_integrator(self):
        """Mock DatasetIntegrator"""
        mock = MagicMock()
        mock.integrate_multiple_datasets.return_value = {
            "concepts": 5,
            "rules": 3,
            "episodes": 0,
        }
        return mock

    @pytest.fixture
    def mock_episodic_layer(self):
        """Mock EpisodicLayer"""
        mock = MagicMock()
        return mock

    def test_init_default(self):
        """Test initialization with defaults"""
        with (
            patch("intelligence.learning_loop.SemanticSearchEngine") as mock_search,
            patch("intelligence.learning_loop.DatasetIntegrator") as mock_integrator,
            patch("intelligence.learning_loop.KnowledgeIntegrator") as mock_knowledge,
            patch("intelligence.learning_loop.EpisodicLayer") as mock_episodic,
        ):
            mock_search.return_value = MagicMock()
            mock_integrator.return_value = MagicMock()
            mock_knowledge.return_value = MagicMock()
            mock_episodic.return_value = MagicMock()

            loop = LearningLoop()

            assert loop.semantic_search is not None
            assert loop.dataset_integrator is not None
            assert loop.knowledge_integrator is not None
            assert loop.episodic_layer is not None

    def test_init_with_dependencies(
        self, mock_semantic_search, mock_dataset_integrator, mock_episodic_layer
    ):
        """Test initialization with provided dependencies"""
        loop = LearningLoop(
            semantic_search=mock_semantic_search,
            dataset_integrator=mock_dataset_integrator,
            episodic_layer=mock_episodic_layer,
        )

        assert loop.semantic_search == mock_semantic_search
        assert loop.dataset_integrator == mock_dataset_integrator
        assert loop.episodic_layer == mock_episodic_layer

    def test_learn_from_query(self, mock_semantic_search, mock_episodic_layer):
        """Test learning from a query"""
        loop = LearningLoop(
            semantic_search=mock_semantic_search,
            episodic_layer=mock_episodic_layer,
        )

        insights = loop.learn_from_query("test query")

        assert "query" in insights
        assert insights["query"] == "test query"
        assert "concepts_found" in insights
        assert "rules_found" in insights
        assert "total_knowledge" in insights
        assert insights["total_knowledge"] == 3

        mock_semantic_search.search.assert_called_once_with("test query")
        assert mock_episodic_layer.store_episode.called

    def test_learn_from_query_with_context(self, mock_semantic_search, mock_episodic_layer):
        """Test learning from a query with context"""
        loop = LearningLoop(
            semantic_search=mock_semantic_search,
            episodic_layer=mock_episodic_layer,
        )

        context = {"domain": "neuroscience"}
        insights = loop.learn_from_query("test query", context=context)

        assert insights["query"] == "test query"
        mock_semantic_search.search_with_context.assert_called_once_with("test query", context)
        assert mock_episodic_layer.store_episode.called

    def test_learn_from_datasets(self, mock_dataset_integrator, mock_episodic_layer):
        """Test learning from datasets"""
        loop = LearningLoop(
            dataset_integrator=mock_dataset_integrator,
            episodic_layer=mock_episodic_layer,
        )

        dataset_paths = ["dataset1.json", "dataset2.json"]
        stats = loop.learn_from_datasets(dataset_paths)

        assert stats["concepts"] == 5
        assert stats["rules"] == 3
        assert mock_dataset_integrator.integrate_multiple_datasets.called
        assert mock_episodic_layer.store_episode.called

    def test_learn_from_datasets_with_types(self, mock_dataset_integrator, mock_episodic_layer):
        """Test learning from datasets with specified types"""
        loop = LearningLoop(
            dataset_integrator=mock_dataset_integrator,
            episodic_layer=mock_episodic_layer,
        )

        dataset_paths = ["dataset1.json", "dataset2.json"]
        dataset_types = ["concepts", "rules"]
        stats = loop.learn_from_datasets(dataset_paths, dataset_types=dataset_types)

        assert stats["concepts"] == 5
        assert stats["rules"] == 3
        mock_dataset_integrator.integrate_multiple_datasets.assert_called_once()
        call_args = mock_dataset_integrator.integrate_multiple_datasets.call_args
        assert len(call_args[0][0]) == 2  # Two paths
        assert call_args[0][1] == dataset_types
