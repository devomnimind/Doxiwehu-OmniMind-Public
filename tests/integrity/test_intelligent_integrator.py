"""Tests for Intelligent Integrator - Phase 26D"""

from __future__ import annotations

from integrity.intelligent_integrator import IntelligentIntegrator


class TestIntelligentIntegrator:
    """Test Intelligent Integrator"""

    def test_init(self):
        """Test initialization"""
        integrator = IntelligentIntegrator()
        assert integrator is not None
        assert len(integrator.integrated_knowledge) == 0

    def test_integrate_knowledge(self):
        """Test knowledge integration"""
        integrator = IntelligentIntegrator()

        content = {
            "name": "test_concept",
            "definition": "Test definition",
        }

        integrated = integrator.integrate_knowledge("test_1", content, source_type="test")

        assert integrated is not None
        assert integrated.knowledge_id == "test_1"
        assert 0.0 <= integrated.confidence <= 1.0

    def test_get_integrated_knowledge(self):
        """Test getting integrated knowledge"""
        integrator = IntelligentIntegrator()

        content = {"name": "test"}
        integrator.integrate_knowledge("test_1", content)

        integrated = integrator.get_integrated_knowledge("test_1")

        assert integrated is not None
        assert integrated.knowledge_id == "test_1"
