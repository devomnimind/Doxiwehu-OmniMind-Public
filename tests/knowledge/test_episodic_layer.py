"""Tests for Episodic Knowledge Layer - Phase 26A"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from knowledge.episodic_layer import Episode, EpisodicLayer


class TestEpisodicLayer:
    """Test Episodic Knowledge Layer"""

    def test_init(self):
        """Test initialization"""
        layer = EpisodicLayer()
        assert layer is not None
        assert len(layer.episodes) == 0

    def test_store_episode(self):
        """Test storing an episode"""
        layer = EpisodicLayer()

        episode = Episode(
            id="ep_1",
            timestamp=datetime.now(timezone.utc),
            event="Memory issue detected and resolved",
            outcome="Memory usage reduced from 95% to 60%",
            learned="Reducing batch_size helps with memory",
        )

        episode_id = layer.store_episode(episode)

        assert episode_id == "ep_1"
        assert "ep_1" in layer.episodes
        assert layer.episodes["ep_1"].event == "Memory issue detected and resolved"

    def test_get_episode(self):
        """Test retrieving an episode"""
        layer = EpisodicLayer()

        episode = Episode(
            id="ep_2",
            timestamp=datetime.now(timezone.utc),
            event="CPU optimization applied",
            outcome="CPU usage reduced",
        )

        layer.store_episode(episode)

        retrieved = layer.get_episode("ep_2")

        assert retrieved is not None
        assert retrieved.event == "CPU optimization applied"

    def test_get_recent_episodes(self):
        """Test getting recent episodes"""
        layer = EpisodicLayer()

        now = datetime.now(timezone.utc)

        episode1 = Episode(
            id="ep_3",
            timestamp=now - timedelta(hours=1),
            event="Event1",
        )
        episode2 = Episode(
            id="ep_4",
            timestamp=now - timedelta(hours=2),
            event="Event2",
        )
        episode3 = Episode(
            id="ep_5",
            timestamp=now,
            event="Event3",
        )

        layer.store_episode(episode1)
        layer.store_episode(episode2)
        layer.store_episode(episode3)

        recent = layer.get_recent_episodes(limit=2)

        assert len(recent) == 2
        # Most recent first
        assert recent[0].id == "ep_5"
        assert recent[1].id == "ep_3"
