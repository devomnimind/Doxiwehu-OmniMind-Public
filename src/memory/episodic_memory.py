"""
Episodic Memory System for OmniMind
Stores agent experiences in Qdrant vector database for learning and improvement.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
import hashlib
import json
import logging

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
)


logger = logging.getLogger(__name__)


def _load_embedding_model(model_name: str) -> Optional[Any]:
    try:
        from sentence_transformers import SentenceTransformer
    except Exception as exc:
        logger.warning(
            "SentenceTransformer import failed: %s. Using deterministic embeddings.",
            exc,
        )
        return None

    try:
        return SentenceTransformer(model_name)
    except Exception as exc:
        logger.warning(
            "Failed to load SentenceTransformer %s: %s. Falling back to deterministic embeddings.",
            model_name,
            exc,
        )
        return None


class EpisodicMemory:
    """
    Manages episodic memory using Qdrant vector database.
    Stores experiences as: (task, action, result, reward) tuples.
    """

    def __init__(
        self,
        qdrant_url: str = "http://localhost:6333",
        collection_name: str = "omnimind_episodes",
        embedding_dim: int = 384,
    ):
        self.client = QdrantClient(url=qdrant_url)
        self.collection_name = collection_name
        self.embedding_dim = embedding_dim
        self._embedding_model = _load_embedding_model("all-MiniLM-L6-v2")

        # Initialize collection if doesn't exist
        self._ensure_collection()

    def _ensure_collection(self):
        """Create collection if it doesn't exist."""
        collections = self.client.get_collections().collections
        collection_names = [c.name for c in collections]

        if self.collection_name not in collection_names:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.embedding_dim, distance=Distance.COSINE
                ),
            )
            print(f"✓ Created collection: {self.collection_name}")

    def _generate_embedding(self, text: str) -> List[float]:
        """Generate embedding from text using SentenceTransformer with fallback."""
        if self._embedding_model:
            try:
                encoded = self._embedding_model.encode(
                    text, normalize_embeddings=True
                )
                return [float(x) for x in encoded]
            except Exception as exc:
                logger.warning(
                    "Embedding model error for text snippet '%s': %s. Using deterministic fallback.",
                    text[:32],
                    exc,
                )
        # TODO: Phase 8 plan → replace deterministic hash fallback with a resilient hybrid embedding
        # pipeline (e.g., lightweight local models plus verification cache) to avoid semantic drift and
        # ensure consistent semantics when the primary model is unavailable.
        return self._hash_based_embedding(text)

    def _hash_based_embedding(self, text: str) -> List[float]:
        hash_obj = hashlib.sha256(text.encode())
        hash_bytes = hash_obj.digest()

        embedding = []
        for i in range(self.embedding_dim):
            byte_val = hash_bytes[i % len(hash_bytes)]
            embedding.append((byte_val / 255.0) * 2 - 1)
        return embedding

    def store_episode(
        self,
        task: str,
        action: str,
        result: str,
        reward: float = 0.0,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Store an episode (experience) in memory.

        Args:
            task: What the agent was trying to do
            action: What action the agent took
            result: What happened (outcome)
            reward: Reward signal (-1.0 to 1.0, used for RLAIF)
            metadata: Additional context

        Returns:
            episode_id: Unique identifier for this episode
        """
        timestamp = datetime.now(timezone.utc).isoformat()

        # Create episode text for embedding
        episode_text = f"Task: {task}\nAction: {action}\nResult: {result}"
        embedding = self._generate_embedding(episode_text)

        # Generate unique ID (Qdrant requires UUID or int)
        hash_int = int(
            hashlib.sha256(f"{timestamp}{task}{action}".encode()).hexdigest()[:16], 16
        )  # Convert hex to int

        # Prepare payload
        payload = {
            "episode_id": str(hash_int),
            "timestamp": timestamp,
            "task": task,
            "action": action,
            "result": result,
            "reward": reward,
            "metadata": metadata or {},
        }

        # Store in Qdrant
        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                PointStruct(
                    id=hash_int, vector=embedding, payload=payload  # Use integer ID
                )
            ],
        )

        return str(hash_int)

    def search_similar(
        self, query: str, top_k: int = 3, min_reward: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar past experiences.

        Args:
            query: Current task/situation to search for
            top_k: Number of similar episodes to return
            min_reward: Only return episodes with reward >= this value

        Returns:
            List of similar episodes with their scores
        """
        query_embedding = self._generate_embedding(query)

        # Build filter
        query_filter = None
        if min_reward is not None:
            query_filter = Filter(
                must=[FieldCondition(key="reward", range={"gte": min_reward})]
            )

        # Search
        search_result = self.client.query_points(
            collection_name=self.collection_name,
            query=query_embedding,
            query_filter=query_filter,
            limit=top_k,
        ).points

        # Format results
        results = []
        for hit in search_result:
            results.append(
                {
                    "score": hit.score,
                    "episode_id": hit.payload["episode_id"],
                    "task": hit.payload["task"],
                    "action": hit.payload["action"],
                    "result": hit.payload["result"],
                    "reward": hit.payload["reward"],
                    "timestamp": hit.payload["timestamp"],
                }
            )

        return results

    def get_episode(self, episode_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve specific episode by ID."""
        try:
            points = self.client.retrieve(
                collection_name=self.collection_name,
                ids=[int(episode_id)],  # Convert string ID to int
            )

            if points:
                return points[0].payload
            return None
        except Exception as e:
            print(f"Error retrieving episode {episode_id}: {e}")
            return None

    def get_stats(self) -> Dict[str, Any]:
        """Get memory statistics."""
        collection_info = self.client.get_collection(self.collection_name)

        return {
            "total_episodes": collection_info.points_count,
            "vector_dim": self.embedding_dim,
            "collection_name": self.collection_name,
        }

    def consolidate_memory(self, min_episodes: int = 100) -> Dict[str, Any]:
        """Consolidate similar experiences to reduce duplicates."""
        stats = self.get_stats()
        total = stats["total_episodes"]

        if total == 0 or total < min_episodes:
            return {
                "status": "skipped",
                "total_episodes": total,
                "duplicates_removed": 0,
                "remaining": total,
            }

        seen = set()
        duplicates = []
        offset = 0
        batch = 128

        while True:
            scroll_result = self.client.scroll(
                collection_name=self.collection_name,
                offset=offset,
                limit=batch,
                with_payload=True,
                with_vectors=False,
            )
            points = getattr(scroll_result, "points", [])
            if not points:
                break

            for point in points:
                payload = point.payload
                key = (
                    payload.get("task"),
                    payload.get("action"),
                    payload.get("result"),
                )
                if key in seen:
                    duplicates.append(point.id)
                else:
                    seen.add(key)

            offset += len(points)
            if len(points) < batch:
                break

        removed = 0
        if duplicates:
            self.client.delete(collection_name=self.collection_name, points=duplicates)
            removed = len(duplicates)

        remaining_stats = self.get_stats()
        remaining = remaining_stats["total_episodes"]
        print(
            f"⚙️  Consolidated memory: removed {removed} duplicate(s), {remaining} entries remain"
        )

        return {
            "status": "consolidated",
            "total_episodes": total,
            "duplicates_removed": removed,
            "remaining": remaining,
        }
