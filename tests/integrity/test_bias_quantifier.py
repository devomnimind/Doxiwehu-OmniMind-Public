"""Tests for Bias Quantifier - Phase 26D"""

from __future__ import annotations

from integrity.bias_quantifier import BiasQuantifier


class TestBiasQuantifier:
    """Test Bias Quantifier"""

    def test_init(self):
        """Test initialization"""
        quantifier = BiasQuantifier()
        assert quantifier is not None
        assert len(quantifier.bias_scores) == 0

    def test_quantify_bias(self):
        """Test bias quantification"""
        quantifier = BiasQuantifier()

        content = {
            "text": "Western approaches to consciousness emphasize integration",
            "source": "paper_1",
        }

        bias_score = quantifier.quantify_bias(
            source_id="test_1",
            source_type="paper",
            content=content,
        )

        assert bias_score is not None
        assert bias_score.source_id == "test_1"
        assert 0.0 <= bias_score.score <= 1.0

    def test_get_bias_score(self):
        """Test getting bias score"""
        quantifier = BiasQuantifier()

        content = {"text": "Test content"}
        quantifier.quantify_bias("test_1", "paper", content)

        score = quantifier.get_bias_score("test_1")

        assert score is not None
        assert score.source_id == "test_1"
