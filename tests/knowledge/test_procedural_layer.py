"""Tests for Procedural Knowledge Layer - Phase 26A"""

from __future__ import annotations

from knowledge.procedural_layer import ProceduralLayer, Rule


class TestProceduralLayer:
    """Test Procedural Knowledge Layer"""

    def test_init(self):
        """Test initialization"""
        layer = ProceduralLayer()
        assert layer is not None
        assert len(layer.rules) == 0

    def test_store_rule(self):
        """Test storing a rule"""
        layer = ProceduralLayer()

        rule = Rule(
            id="rule_1",
            name="Memory Optimization",
            description="Reduce batch size when memory is high",
            rule_type="process",
            conditions=["memory > 90%"],
            actions=["reduce batch_size", "disable cache"],
        )

        rule_id = layer.store_rule(rule)

        assert rule_id == "rule_1"
        assert "rule_1" in layer.rules
        assert layer.rules["rule_1"].name == "Memory Optimization"

    def test_get_rule(self):
        """Test retrieving a rule"""
        layer = ProceduralLayer()

        rule = Rule(
            id="rule_2",
            name="CPU Optimization",
            description="Enable GPU when CPU is high",
            rule_type="rule",
        )

        layer.store_rule(rule)

        retrieved = layer.get_rule("rule_2")

        assert retrieved is not None
        assert retrieved.name == "CPU Optimization"

    def test_get_rules_by_type(self):
        """Test getting rules by type"""
        layer = ProceduralLayer()

        rule1 = Rule(
            id="rule_3",
            name="Rule1",
            description="Description1",
            rule_type="process",
        )
        rule2 = Rule(
            id="rule_4",
            name="Rule2",
            description="Description2",
            rule_type="process",
        )
        rule3 = Rule(
            id="rule_5",
            name="Rule3",
            description="Description3",
            rule_type="rule",
        )

        layer.store_rule(rule1)
        layer.store_rule(rule2)
        layer.store_rule(rule3)

        process_rules = layer.get_rules_by_type("process")

        assert len(process_rules) == 2
        assert all(r.rule_type == "process" for r in process_rules)
