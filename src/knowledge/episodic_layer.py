"""Episodic Knowledge Layer - Phase 26A

Layer 3: "O que já aconteceu" (histórico, experiência)

Author: OmniMind Development
License: MIT
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List

from memory.temporal_memory_index import TemporalMemoryIndex

logger = logging.getLogger(__name__)


@dataclass
class Episode:
    """Episodic memory entry"""

    id: str
    timestamp: datetime
    event: str
    context: Dict[str, Any] | None = None
    outcome: str | None = None
    learned: str | None = None

    def __post_init__(self) -> None:
        """Ensure timestamp is timezone-aware"""
        if self.timestamp.tzinfo is None:
            self.timestamp = self.timestamp.replace(tzinfo=timezone.utc)


class EpisodicLayer:
    """Armazena histórico e experiências (Layer 3)"""

    def __init__(self, temporal_memory: TemporalMemoryIndex | None = None):
        """Initialize episodic layer

        Args:
            temporal_memory: TemporalMemoryIndex instance (optional)
        """
        if temporal_memory is None:
            from memory.temporal_memory_index import TemporalMemoryIndex

            temporal_memory = TemporalMemoryIndex()

        self.temporal_memory = temporal_memory
        self.episodes: Dict[str, Episode] = {}

        logger.info("EpisodicLayer initialized")

    def store_episode(self, episode: Episode) -> str:
        """Store an episode in episodic layer

        Args:
            episode: Episode to store

        Returns:
            Episode ID
        """
        # Store in memory
        self.episodes[episode.id] = episode

        # Store in temporal memory (Phase 24)
        self.temporal_memory.add_episode(
            episode_id=episode.id,
            timestamp=episode.timestamp,
            episode_data={
                "event": episode.event,
                "context": episode.context or {},
                "outcome": episode.outcome,
                "learned": episode.learned,
            },
        )

        logger.info(f"Stored episode: {episode.event} (ID: {episode.id})")
        return episode.id

    def get_episode(self, episode_id: str) -> Episode | None:
        """Get episode by ID

        Args:
            episode_id: Episode identifier

        Returns:
            Episode or None
        """
        return self.episodes.get(episode_id)

    def get_episodes_in_range(self, start_time: datetime, end_time: datetime) -> List[Episode]:
        """Get episodes within time range

        Args:
            start_time: Start time
            end_time: End time

        Returns:
            List of episodes
        """
        # Ensure timezone-aware
        if start_time.tzinfo is None:
            start_time = start_time.replace(tzinfo=timezone.utc)
        if end_time.tzinfo is None:
            end_time = end_time.replace(tzinfo=timezone.utc)

        # Query temporal memory
        episodes_data = self.temporal_memory.get_episodes_in_range(
            start_time=start_time, end_time=end_time
        )

        # Map to Episode objects
        episodes = []
        for ep_data in episodes_data:
            episode_id = ep_data.get("episode_id")
            if episode_id and episode_id in self.episodes:
                episodes.append(self.episodes[episode_id])

        return episodes

    def get_recent_episodes(self, limit: int = 10) -> List[Episode]:
        """Get most recent episodes

        Args:
            limit: Number of episodes

        Returns:
            List of recent episodes
        """
        sorted_episodes = sorted(self.episodes.values(), key=lambda e: e.timestamp, reverse=True)
        return sorted_episodes[:limit]

    def list_all_episodes(self) -> List[Episode]:
        """List all stored episodes

        Returns:
            List of all episodes
        """
        return list(self.episodes.values())
