"""Tests for Narrative History - Lacanian Memory"""

from __future__ import annotations

from memory.narrative_history import NarrativeHistory


class TestNarrativeHistory:
    """Test Narrative History (Lacanian)"""

    def test_init(self):
        """Test initialization"""
        history = NarrativeHistory()
        assert history is not None
        assert len(history.retroactive_significations) == 0

    def test_inscribe_event(self):
        """Test inscribing an event without meaning"""
        history = NarrativeHistory()

        event = {
            "task": "test_task",
            "action": "test_action",
            "result": "test_result",
        }

        event_id = history.inscribe_event(event, without_meaning=True)

        assert event_id is not None
        assert event_id in history.retroactive_significations

    def test_retroactive_signification(self):
        """Test retroactive signification (Nachträglichkeit)"""
        history = NarrativeHistory()

        event = {"task": "test", "action": "test", "result": "test"}
        event_id = history.inscribe_event(event, without_meaning=True)

        history.retroactive_signification(
            event_id, "This event now means understanding", {"trigger": "new_event"}
        )

        signification = history.retroactive_significations[event_id]
        assert signification["awaiting"] is False
        assert "retroactive_meaning" in signification

    def test_construct_narrative(self):
        """Test narrative construction"""
        history = NarrativeHistory()

        # Inscribe some events
        event1 = {"task": "learn", "action": "read", "result": "understood"}
        event2 = {"task": "apply", "action": "implement", "result": "success"}

        history.inscribe_event(event1, without_meaning=True)
        history.inscribe_event(event2, without_meaning=True)

        # Construct narrative
        narrative = history.construct_narrative("learning process")

        assert "narrative" in narrative
        assert "coherence" in narrative
