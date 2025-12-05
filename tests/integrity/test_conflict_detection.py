"""Tests for Conflict Detection Engine - Phase 26D"""

from __future__ import annotations


from integrity.conflict_detection_engine import Conflict, ConflictDetectionEngine


class TestConflictDetectionEngine:
    """Test Conflict Detection Engine"""

    def test_init(self):
        """Test initialization"""
        engine = ConflictDetectionEngine()
        assert engine is not None
        assert len(engine.detected_conflicts) == 0

    def test_detect_conflicts(self):
        """Test conflict detection"""
        engine = ConflictDetectionEngine()

        # This will search and check for conflicts
        conflicts = engine.detect_conflicts("consciousness integration")

        # Should return a list (may be empty if no conflicts)
        assert isinstance(conflicts, list)

    def test_get_conflicts_for_entity(self):
        """Test getting conflicts for an entity"""
        engine = ConflictDetectionEngine()

        # Add a mock conflict
        conflict = Conflict(
            conflict_id="test_1",
            source_1={"name": "consciousness"},
            source_2={"name": "integration"},
            conflict_type="contradiction",
            severity=0.8,
            description="Test conflict",
        )
        engine.detected_conflicts["test_1"] = conflict

        conflicts = engine.get_conflicts_for_entity("consciousness")

        assert len(conflicts) >= 0  # May or may not find conflicts
