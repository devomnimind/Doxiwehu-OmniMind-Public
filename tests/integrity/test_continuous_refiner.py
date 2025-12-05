"""Tests for Continuous Refiner - Phase 26D"""

from __future__ import annotations


from integrity.continuous_refiner import ContinuousRefiner


class TestContinuousRefiner:
    """Test Continuous Refiner"""

    def test_init(self):
        """Test initialization"""
        refiner = ContinuousRefiner()
        assert refiner is not None
        assert len(refiner.refinement_history) == 0

    def test_refine_knowledge(self):
        """Test knowledge refinement"""
        refiner = ContinuousRefiner()

        # First integrate knowledge
        content = {"name": "test", "definition": "test"}
        integrated = refiner.integrator.integrate_knowledge("test_1", content)

        # Refine based on validation
        validation_result = {"timestamp": "2025-12-05T00:00:00Z"}
        refined = refiner.refine_knowledge("test_1", validation_result, was_correct=True)

        assert refined is not None
        assert refined.confidence >= integrated.confidence

    def test_get_refinement_history(self):
        """Test getting refinement history"""
        refiner = ContinuousRefiner()

        history = refiner.get_refinement_history()

        assert isinstance(history, list)

    def test_get_knowledge_quality_report(self):
        """Test getting quality report"""
        refiner = ContinuousRefiner()

        report = refiner.get_knowledge_quality_report()

        assert report is not None
        assert "total_knowledge" in report
        assert "average_confidence" in report
