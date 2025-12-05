"""Tests for SemanticSearchEngine - Phase 26B"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from intelligence.semantic_search_engine import SemanticSearchEngine


class TestSemanticSearchEngine:
    """Test SemanticSearchEngine"""

    @pytest.fixture
    def mock_semantic_memory(self):
        """Mock SemanticMemoryLayer"""
        mock = MagicMock()
        mock.retrieve_similar.return_value = [
            {"content": "test content", "score": 0.9},
            {"content": "another content", "score": 0.8},
        ]
        return mock

    @pytest.fixture
    def mock_knowledge_integrator(self):
        """Mock KnowledgeIntegrator"""
        mock = MagicMock()
        mock.query.return_value = {
            "concepts": [{"name": "concept1", "definition": "def1"}],
            "rules": [{"name": "rule1", "description": "desc1"}],
            "episodes": [{"event": "episode1"}],
        }
        return mock

    def test_init_default(self):
        """Test initialization with defaults"""
        with (
            patch("memory.semantic_memory_layer.get_semantic_memory") as mock_get,
            patch("intelligence.semantic_search_engine.KnowledgeIntegrator"),
        ):
            mock_memory = MagicMock()
            mock_get.return_value = mock_memory

            engine = SemanticSearchEngine()

            assert engine.semantic_memory is not None
            assert engine.knowledge_integrator is not None

    def test_init_with_dependencies(self, mock_semantic_memory, mock_knowledge_integrator):
        """Test initialization with provided dependencies"""
        engine = SemanticSearchEngine(
            semantic_memory=mock_semantic_memory,
            knowledge_integrator=mock_knowledge_integrator,
        )

        assert engine.semantic_memory == mock_semantic_memory
        assert engine.knowledge_integrator == mock_knowledge_integrator

    def test_search(self, mock_semantic_memory, mock_knowledge_integrator):
        """Test basic search"""
        engine = SemanticSearchEngine(
            semantic_memory=mock_semantic_memory,
            knowledge_integrator=mock_knowledge_integrator,
        )

        results = engine.search("test query", top_k=5)

        assert "semantic_memory" in results
        assert "declarative" in results
        assert "procedural" in results
        assert "episodic" in results
        assert "total_results" in results
        assert results["total_results"] > 0

        mock_semantic_memory.retrieve_similar.assert_called_once_with("test query", top_k=5)
        mock_knowledge_integrator.query.assert_called_once_with("test query", layers=None)

    def test_search_with_layers(self, mock_semantic_memory, mock_knowledge_integrator):
        """Test search with specific layers"""
        engine = SemanticSearchEngine(
            semantic_memory=mock_semantic_memory,
            knowledge_integrator=mock_knowledge_integrator,
        )

        results = engine.search("test query", top_k=10, layers=["declarative", "procedural"])

        assert results["total_results"] > 0
        mock_knowledge_integrator.query.assert_called_once_with(
            "test query", layers=["declarative", "procedural"]
        )

    def test_search_with_context(self, mock_semantic_memory, mock_knowledge_integrator):
        """Test search with context filters"""
        engine = SemanticSearchEngine(
            semantic_memory=mock_semantic_memory,
            knowledge_integrator=mock_knowledge_integrator,
        )

        # Setup mock results with category
        mock_knowledge_integrator.query.return_value = {
            "concepts": [
                {"name": "concept1", "category": "system"},
                {"name": "concept2", "category": "other"},
            ],
            "rules": [
                {"name": "rule1", "type": "process"},
                {"name": "rule2", "type": "other"},
            ],
            "episodes": [],
        }

        context = {"category": "system", "rule_type": "process"}
        results = engine.search_with_context("test query", context, top_k=10)

        assert "declarative" in results
        assert "procedural" in results

        # Check filtering
        declarative_results = results["declarative"]
        assert all(c.get("category") == "system" for c in declarative_results)

        procedural_results = results["procedural"]
        assert all(r.get("type") == "process" for r in procedural_results)

    def test_search_with_context_no_filters(self, mock_semantic_memory, mock_knowledge_integrator):
        """Test search with context but no filters"""
        engine = SemanticSearchEngine(
            semantic_memory=mock_semantic_memory,
            knowledge_integrator=mock_knowledge_integrator,
        )

        context = {"other_key": "value"}
        results = engine.search_with_context("test query", context, top_k=10)

        assert results["total_results"] > 0
