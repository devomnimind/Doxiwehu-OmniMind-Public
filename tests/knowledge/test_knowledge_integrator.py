"""Tests for Knowledge Integrator - Phase 26A"""

from __future__ import annotations

from datetime import datetime, timezone

from knowledge.declarative_layer import Concept
from knowledge.episodic_layer import Episode
from knowledge.knowledge_integrator import KnowledgeIntegrator
from knowledge.procedural_layer import Rule


class TestKnowledgeIntegrator:
    """Test Knowledge Integrator"""

    def test_init(self):
        """Test initialization"""
        integrator = KnowledgeIntegrator()
        assert integrator is not None
        assert integrator.declarative is not None
        assert integrator.procedural is not None
        assert integrator.episodic is not None

    def test_query_all_layers(self):
        """Test querying all layers"""
        integrator = KnowledgeIntegrator()

        # Add some test data
        concept = Concept(
            id="c1",
            name="Memory",
            definition="System memory",
            category="system",
        )
        integrator.declarative.store_concept(concept)

        rule = Rule(
            id="r1",
            name="Memory Rule",
            description="Optimize memory usage",
            rule_type="rule",
        )
        integrator.procedural.store_rule(rule)

        episode = Episode(
            id="e1",
            timestamp=datetime.now(timezone.utc),
            event="Memory optimization",
            learned="Reducing batch size helps",
        )
        integrator.episodic.store_episode(episode)

        # Query
        results = integrator.query("memory")

        assert "concepts" in results
        assert "rules" in results
        assert "episodes" in results

    def test_get_statistics(self):
        """Test getting statistics"""
        integrator = KnowledgeIntegrator()

        # Add test data
        concept = Concept(id="c1", name="Test", definition="Test")
        integrator.declarative.store_concept(concept)

        rule = Rule(id="r1", name="Test", description="Test", rule_type="rule")
        integrator.procedural.store_rule(rule)

        episode = Episode(
            id="e1",
            timestamp=datetime.now(timezone.utc),
            event="Test",
        )
        integrator.episodic.store_episode(episode)

        stats = integrator.get_statistics()

        assert stats["concepts"] == 1
        assert stats["rules"] == 1
        assert stats["episodes"] == 1
