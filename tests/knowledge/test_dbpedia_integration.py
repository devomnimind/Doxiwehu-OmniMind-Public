"""Tests for DBpedia Ontology Integration - Phase 26A Fase 1.3"""

from __future__ import annotations


class TestDBpediaIntegration:
    """Test DBpedia ontology integration"""

    def test_convert_triple_to_rule(self):
        """Test converting DBpedia triple to rule format"""
        from scripts.integrate_dbpedia_ontology import convert_triple_to_rule

        triple = {
            "subject": "Consciousness",
            "predicate": "isRelatedTo",
            "object": "Awareness",
        }

        rule = convert_triple_to_rule(triple)

        assert rule is not None
        assert "name" in rule
        assert "description" in rule
        assert "process" in rule
        assert rule["process"]["type"] == "rdf_triple"
        assert rule["process"]["subject"] == "Consciousness"

    def test_integrate_triple(self):
        """Test integrating a single triple"""
        from scripts.integrate_dbpedia_ontology import (
            integrate_dbpedia_to_procedural_layer,
        )

        triple = {
            "subject": "Consciousness",
            "predicate": "isRelatedTo",
            "object": "Awareness",
        }

        procedural_layer = integrate_dbpedia_to_procedural_layer([triple])

        assert len(procedural_layer.rules) > 0

    def test_filter_consciousness_related(self):
        """Test filtering consciousness-related triples"""
        from scripts.integrate_dbpedia_ontology import filter_consciousness_related

        triples = [
            {"subject": "Consciousness", "predicate": "isA", "object": "MentalState"},
            {"subject": "Car", "predicate": "isA", "object": "Vehicle"},
            {"subject": "Memory", "predicate": "isRelatedTo", "object": "Cognition"},
        ]

        filtered = filter_consciousness_related(triples)

        assert len(filtered) >= 2  # At least Consciousness and Memory
        assert any("Consciousness" in str(t) for t in filtered)
