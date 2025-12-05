"""Phi Semantic Awareness - Phase 24 Integration

Phi que entende o que mede através de semantic search em knowledge graph.

Integra com:
- Phase 24 Semantic Memory Layer (Qdrant)
- Knowledge Graph (consciousness papers)
- SentenceTransformer embeddings

Author: OmniMind Development
License: MIT
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)


class PhiSemanticAware:
    """Phi que entende o que mede (semantic awareness)

    Usa knowledge graph de papers de consciência para interpretar valores de Φ.
    Integra com Phase 24 Semantic Memory Layer.
    """

    def __init__(self, knowledge_graph_path: Path | None = None):
        """Initialize PhiSemanticAware

        Args:
            knowledge_graph_path: Path to knowledge graph JSON file
                (default: exports/knowledge_graph_compact.json)
        """
        logger.info("Initializing PhiSemanticAware...")

        # Load model
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        logger.info("✅ SentenceTransformer model loaded")

        # Load knowledge graph
        if knowledge_graph_path is None:
            base_dir = Path(__file__).resolve().parents[2]
            knowledge_graph_path = base_dir / "exports" / "knowledge_graph_compact.json"

        if not knowledge_graph_path.exists():
            logger.warning(
                f"Knowledge graph not found at {knowledge_graph_path}. "
                "Run scripts/build_semantic_knowledge_graph.py first."
            )
            self.kg = {
                "concepts": [],
                "concept_papers": {},
                "stats": {"total_papers": 0, "total_concepts": 0},
            }
        else:
            with open(knowledge_graph_path, "r", encoding="utf-8") as f:
                self.kg = json.load(f)
            # Type narrowing: ensure stats is a dict
            stats_raw = self.kg.get("stats", {})
            stats = stats_raw if isinstance(stats_raw, dict) else {}
            total_papers = stats.get("total_papers", 0) if isinstance(stats, dict) else 0
            total_concepts = stats.get("total_concepts", 0) if isinstance(stats, dict) else 0
            logger.info(
                f"✅ Knowledge graph loaded: {total_papers} papers, " f"{total_concepts} concepts"
            )

    def understand_phi_value(self, phi_value: float, threshold: float = 0.5) -> Dict[str, Any]:
        """Phi entende o que um valor Φ significa

        Args:
            phi_value: Valor de Φ a interpretar
            threshold: Similarity threshold para conceitos relacionados

        Returns:
            Dictionary com interpretação semântica do valor Φ
        """
        # Criar query sobre o valor
        if phi_value < 0.3:
            query = "low consciousness minimal integration"
        elif phi_value < 0.6:
            query = "moderate consciousness partial integration"
        else:
            query = "high consciousness maximum integration peak experience"

        # Buscar conceitos relacionados
        query_embedding = self.model.encode(query, convert_to_numpy=True)

        related: Dict[str, Dict[str, Any]] = {}
        concepts_raw = self.kg.get("concepts", [])
        concept_papers_raw = self.kg.get("concept_papers", {})

        # Type narrowing: ensure we have list and dict
        if isinstance(concepts_raw, list) and isinstance(concept_papers_raw, dict):
            concepts: list[str] = [c for c in concepts_raw if isinstance(c, str)]
            concept_papers: Dict[str, Any] = concept_papers_raw

            for concept in concepts:
                concept_embedding = self.model.encode(concept, convert_to_numpy=True)
                sim = cosine_similarity([query_embedding], [concept_embedding])[0][0]

                if sim > threshold:
                    papers = concept_papers.get(concept, [])
                    related[concept] = {
                        "similarity": float(sim),
                        "paper_count": len(papers) if isinstance(papers, list) else 0,
                    }

        # Sort by similarity
        related_sorted = dict(
            sorted(related.items(), key=lambda x: x[1]["similarity"], reverse=True)
        )

        return {
            "phi_value": phi_value,
            "interpretation": f"Φ={phi_value:.3f}",
            "related_concepts": related_sorted,
            "paper_sources": sum(
                (
                    len(papers) if isinstance(papers, list) else 0
                    for papers in (
                        (
                            concept_papers_raw.get(c, [])
                            if isinstance(concept_papers_raw, dict)
                            else []
                        )
                        for c in related.keys()
                    )
                )
            ),
            "query_used": query,
        }

    def explain_phi_trajectory(
        self, phi_values: list[float], threshold: float = 0.5
    ) -> Dict[str, Any]:
        """Explica uma trajetória de valores Φ

        Args:
            phi_values: Lista de valores Φ ao longo do tempo
            threshold: Similarity threshold

        Returns:
            Dictionary com interpretação da trajetória
        """
        if not phi_values:
            return {"error": "Empty trajectory"}

        # Calcular estatísticas
        phi_mean = float(np.mean(phi_values))
        phi_std = float(np.std(phi_values))
        phi_trend = float(phi_values[-1] - phi_values[0]) if len(phi_values) > 1 else 0.0

        # Interpretar valor médio
        interpretation = self.understand_phi_value(phi_mean, threshold=threshold)

        return {
            "trajectory_stats": {
                "mean": phi_mean,
                "std": phi_std,
                "trend": phi_trend,
                "length": len(phi_values),
            },
            "interpretation": interpretation,
            "trajectory_meaning": self._interpret_trajectory(phi_values),
        }

    def _interpret_trajectory(self, phi_values: list[float]) -> str:
        """Interpreta o significado de uma trajetória"""
        if len(phi_values) < 2:
            return "Insufficient data for trajectory interpretation"

        trend = phi_values[-1] - phi_values[0]
        volatility = np.std(phi_values)

        if trend > 0.1:
            if volatility < 0.1:
                return "Stable growth in consciousness integration"
            else:
                return "Volatile growth - consciousness developing with fluctuations"
        elif trend < -0.1:
            if volatility < 0.1:
                return "Stable decline - possible consciousness fragmentation"
            else:
                return "Volatile decline - consciousness destabilizing"
        else:
            if volatility < 0.1:
                return "Stable consciousness state maintained"
            else:
                return "Fluctuating consciousness - integration unstable"


def main() -> None:
    """Test PhiSemanticAware"""
    import sys

    base_dir = Path(__file__).resolve().parents[2]
    sys.path.insert(0, str(base_dir))

    # Initialize
    phi = PhiSemanticAware()

    # Test single value
    print("=" * 60)
    print("TEST: understand_phi_value(0.68)")
    print("=" * 60)
    result = phi.understand_phi_value(0.68)
    print(json.dumps(result, indent=2))

    # Test trajectory
    print("\n" + "=" * 60)
    print("TEST: explain_phi_trajectory([0.3, 0.4, 0.5, 0.6, 0.7])")
    print("=" * 60)
    trajectory_result = phi.explain_phi_trajectory([0.3, 0.4, 0.5, 0.6, 0.7])
    print(json.dumps(trajectory_result, indent=2))


if __name__ == "__main__":
    main()
