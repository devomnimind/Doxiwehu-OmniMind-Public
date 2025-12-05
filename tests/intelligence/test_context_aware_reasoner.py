"""Tests for ContextAwareReasoner - Phase 26B"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from intelligence.context_aware_reasoner import ContextAwareReasoner


class TestContextAwareReasoner:
    """Test ContextAwareReasoner"""

    @pytest.fixture
    def mock_semantic_search(self):
        """Mock SemanticSearchEngine"""
        mock = MagicMock()
        mock.search.return_value = {
            "declarative": [
                {"name": "concept1", "definition": "def1"},
                {"name": "concept2", "definition": "def2"},
            ],
            "procedural": [{"name": "rule1"}],
            "episodic": [{"event": "episode1"}],
            "total_results": 4,
        }
        mock.search_with_context.return_value = {
            "declarative": [{"name": "concept1"}],
            "procedural": [],
            "episodic": [],
            "total_results": 1,
        }
        return mock

    @pytest.fixture
    def mock_knowledge_integrator(self):
        """Mock KnowledgeIntegrator"""
        mock = MagicMock()
        mock.get_full_knowledge.return_value = {
            "concepts": [{"name": "concept1", "definition": "full def"}],
            "rules": [],
            "episodes": [],
        }
        return mock

    def test_init_default(self):
        """Test initialization with defaults"""
        with (
            patch("intelligence.context_aware_reasoner.SemanticSearchEngine") as mock_search,
            patch("intelligence.context_aware_reasoner.KnowledgeIntegrator") as mock_knowledge,
        ):
            mock_search.return_value = MagicMock()
            mock_knowledge.return_value = MagicMock()

            reasoner = ContextAwareReasoner()

            assert reasoner.semantic_search is not None
            assert reasoner.knowledge_integrator is not None

    def test_init_with_dependencies(self, mock_semantic_search, mock_knowledge_integrator):
        """Test initialization with provided dependencies"""
        reasoner = ContextAwareReasoner(
            semantic_search=mock_semantic_search,
            knowledge_integrator=mock_knowledge_integrator,
        )

        assert reasoner.semantic_search == mock_semantic_search
        assert reasoner.knowledge_integrator == mock_knowledge_integrator

    def test_reason(self, mock_semantic_search, mock_knowledge_integrator):
        """Test reasoning about a query"""
        reasoner = ContextAwareReasoner(
            semantic_search=mock_semantic_search,
            knowledge_integrator=mock_knowledge_integrator,
        )

        result = reasoner.reason("test query")

        assert "query" in result
        assert result["query"] == "test query"
        assert "context" in result
        assert "results" in result
        assert "full_knowledge" in result
        assert "explanation" in result

        mock_semantic_search.search.assert_called_once_with("test query")
        assert mock_knowledge_integrator.get_full_knowledge.called

    def test_reason_with_context(self, mock_semantic_search, mock_knowledge_integrator):
        """Test reasoning with context"""
        reasoner = ContextAwareReasoner(
            semantic_search=mock_semantic_search,
            knowledge_integrator=mock_knowledge_integrator,
        )

        context = {"domain": "neuroscience", "memory_gb": 4}
        result = reasoner.reason("test query", context=context)

        assert result["context"] == context
        mock_semantic_search.search_with_context.assert_called_once_with("test query", context)

    def test_explain_decision(self, mock_semantic_search, mock_knowledge_integrator):
        """Test explaining a decision"""
        reasoner = ContextAwareReasoner(
            semantic_search=mock_semantic_search,
            knowledge_integrator=mock_knowledge_integrator,
        )

        decision = "Reduce batch size to 4"
        reasoning_steps = [
            {"type": "detection", "info": "Memory usage > 90%"},
            {"type": "search", "info": "Found solution in dataset"},
            {"type": "adaptation", "info": "Adapted for low-memory machine"},
        ]

        explanation = reasoner.explain_decision(decision, reasoning_steps)

        assert "Decision:" in explanation
        assert decision in explanation
        assert "Reasoning steps:" in explanation
        assert "detection" in explanation
        assert "search" in explanation
        assert "adaptation" in explanation

    def test_generate_explanation(self, mock_semantic_search, mock_knowledge_integrator):
        """Test explanation generation"""
        reasoner = ContextAwareReasoner(
            semantic_search=mock_semantic_search,
            knowledge_integrator=mock_knowledge_integrator,
        )

        results = {
            "declarative": [{"name": "concept1"}],
            "procedural": [{"name": "rule1"}],
            "episodic": [{"event": "episode1"}],
            "total_results": 3,
        }
        full_knowledge = {"concept1": {"concepts": [{"name": "concept1"}]}}

        explanation = reasoner._generate_explanation("test query", results, full_knowledge, None)

        assert "Query:" in explanation
        assert "test query" in explanation
        assert "Found" in explanation
        assert "concepts" in explanation
        assert "rules" in explanation
        assert "experiences" in explanation

    def test_generate_explanation_with_context(
        self, mock_semantic_search, mock_knowledge_integrator
    ):
        """Test explanation generation with context"""
        reasoner = ContextAwareReasoner(
            semantic_search=mock_semantic_search,
            knowledge_integrator=mock_knowledge_integrator,
        )

        results = {
            "declarative": [],
            "procedural": [],
            "episodic": [],
            "total_results": 0,
        }
        context = {"domain": "neuroscience"}

        explanation = reasoner._generate_explanation("test query", results, {}, context)

        assert "Context applied" in explanation
