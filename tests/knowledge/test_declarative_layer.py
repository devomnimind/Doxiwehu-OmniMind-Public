"""Tests for Declarative Knowledge Layer - Phase 26A"""

from __future__ import annotations

from knowledge.declarative_layer import Concept, DeclarativeLayer


class TestDeclarativeLayer:
    """Test Declarative Knowledge Layer"""

    def test_init(self):
        """Test initialization"""
        layer = DeclarativeLayer()
        assert layer is not None
        assert len(layer.concepts) == 0

    def test_store_concept(self):
        """Test storing a concept"""
        layer = DeclarativeLayer()

        concept = Concept(
            id="test_1",
            name="Consciousness",
            definition="Integrated information in a system",
            category="philosophy",
        )

        concept_id = layer.store_concept(concept)

        assert concept_id == "test_1"
        assert "test_1" in layer.concepts
        assert layer.concepts["test_1"].name == "Consciousness"

    def test_get_concept(self):
        """Test retrieving a concept"""
        layer = DeclarativeLayer()

        concept = Concept(
            id="test_2",
            name="Phi",
            definition="Measure of integrated information",
            category="metrics",
        )

        layer.store_concept(concept)

        retrieved = layer.get_concept("test_2")

        assert retrieved is not None
        assert retrieved.name == "Phi"
        assert retrieved.definition == "Measure of integrated information"

    def test_get_concepts_by_category(self):
        """Test getting concepts by category"""
        layer = DeclarativeLayer()

        concept1 = Concept(
            id="test_3",
            name="Concept1",
            definition="Definition1",
            category="philosophy",
        )
        concept2 = Concept(
            id="test_4",
            name="Concept2",
            definition="Definition2",
            category="philosophy",
        )
        concept3 = Concept(
            id="test_5",
            name="Concept3",
            definition="Definition3",
            category="metrics",
        )

        layer.store_concept(concept1)
        layer.store_concept(concept2)
        layer.store_concept(concept3)

        philosophy_concepts = layer.get_concepts_by_category("philosophy")

        assert len(philosophy_concepts) == 2
        assert all(c.category == "philosophy" for c in philosophy_concepts)

    def test_list_all_concepts(self):
        """Test listing all concepts"""
        layer = DeclarativeLayer()

        concept1 = Concept(id="test_6", name="Concept1", definition="Definition1")
        concept2 = Concept(id="test_7", name="Concept2", definition="Definition2")

        layer.store_concept(concept1)
        layer.store_concept(concept2)

        all_concepts = layer.list_all_concepts()

        assert len(all_concepts) == 2
