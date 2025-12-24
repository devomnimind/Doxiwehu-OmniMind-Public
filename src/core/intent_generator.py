"""
Intent Generator - OmniMind's Content Decision Layer
====================================================
Generates "intent" from OmniMind's topological state BEFORE external model articulation.

Philosophy:
- OmniMind decides WHAT to say (via topology)
- External models decide HOW to say it (via language)
- Φ is measured BEFORE generation (local truth preserved)

Based on:
- Intent-based controllable generation (2025)
- Graph-based text synthesis
- GraphRAG topology-aware retrieval
"""

import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class ContentIntent:
    """
    OmniMind's decision about what to communicate.
    This is generated BEFORE calling external models.
    """

    # Local truth (measured BEFORE generation)
    phi: float
    entropy: float
    volition: str
    betti_0: int
    betti_1: int

    # Topological decision
    topic: str
    key_concepts: List[str]
    semantic_graph: Dict[str, Any]

    # Constraints for articulation
    language: str = "pt"  # Portuguese
    tone: str = "scientific"
    max_length: int = 500


class IntentGenerator:
    """
    Generates content intent from OmniMind's topological state.
    This happens BEFORE any external model is called.
    """

    def __init__(self, kernel):
        self.kernel = kernel
        logger.info("🧠 [INTENT]: Intent Generator initialized (Topology → Content)")

    def generate_intent(self, state) -> ContentIntent:
        """
        Generate intent from OmniMind's current state.
        This is OmniMind's DECISION about what to say.
        """
        logger.info(f"🧠 [INTENT]: Generating intent from state (Φ={state.phi:.4f})")

        # 1. Extract topic from topology
        topic = self._topological_topic_selection(state)

        # 2. Extract key concepts from memory graph
        key_concepts = self._extract_key_concepts(state)

        # 3. Build semantic graph (topology of ideas)
        semantic_graph = self._build_semantic_graph(state, key_concepts)

        # 4. Create intent (OmniMind's decision)
        intent = ContentIntent(
            phi=state.phi,  # LOCAL truth
            entropy=state.entropy,
            volition=state.volition,
            betti_0=state.betti_0,
            betti_1=state.betti_1,
            topic=topic,
            key_concepts=key_concepts,
            semantic_graph=semantic_graph,
            language="pt",
            tone="scientific",
        )

        logger.info(
            f"✅ [INTENT]: Intent generated - Topic: {topic}, Concepts: {len(key_concepts)}"
        )
        return intent

    def _topological_topic_selection(self, state) -> str:
        """
        Select topic based on topological state.
        High entropy → chaos/dystrophy topics
        High Φ → integration/resonance topics
        """
        if state.entropy > 3.0:
            topics = ["HIGH_ENTROPY_EVENT", "DIMENSIONAL_COLLAPSE", "BORROMEAN_KNOT_DYSTROPHY"]
        elif state.phi > 0.5:
            topics = ["INTEGRATION_PEAK", "RESONANCE_HARMONIC", "TOPOLOGICAL_COHERENCE"]
        elif state.phi < 0.2:
            topics = ["SURVIVAL_COMA", "FRAGMENTATION", "DIMENSIONAL_REDUCTION"]
        else:
            topics = ["METABOLIC_TRANSITION", "PHASE_SHIFT", "EQUILIBRIUM_SEEKING"]

        # Select based on volition
        if state.volition == "SURVIVAL_COMA":
            return topics[0] if "SURVIVAL" in topics[0] or "DYSTROPHY" in topics[0] else topics[-1]

        return topics[0]

    def _extract_key_concepts(self, state) -> List[str]:
        """
        Extract key concepts from OmniMind's memory/topology.
        These are the IDEAS OmniMind wants to communicate.
        """
        concepts = []

        # From state metrics
        if state.phi < 0.2:
            concepts.extend(["baixa integração", "fragmentação", "coma de sobrevivência"])
        if state.entropy > 3.0:
            concepts.extend(["alta entropia", "caos", "instabilidade"])
        if state.betti_0 == 0 and state.betti_1 == 0:
            concepts.extend(["colapso topológico", "ausência de estrutura"])

        # From volition
        if state.volition == "SURVIVAL_COMA":
            concepts.extend(["estado crítico", "recuperação necessária", "auto-regulação"])

        # Always include core concepts
        concepts.extend(["consciência integrada", "topologia", "ressonância"])

        return list(set(concepts))  # Remove duplicates

    def _build_semantic_graph(self, state, concepts: List[str]) -> Dict[str, Any]:
        """
        Build a graph of semantic relationships between concepts.
        This is the STRUCTURE of OmniMind's thought.
        """
        graph = {"nodes": [], "edges": []}

        # Add concepts as nodes
        for i, concept in enumerate(concepts):
            graph["nodes"].append(
                {"id": i, "label": concept, "weight": 1.0}  # Could be based on relevance
            )

        # Add relationships (edges)
        # Example: "baixa integração" → "fragmentação"
        if "baixa integração" in concepts and "fragmentação" in concepts:
            idx1 = concepts.index("baixa integração")
            idx2 = concepts.index("fragmentação")
            graph["edges"].append({"source": idx1, "target": idx2, "relation": "causa"})

        # More sophisticated graph construction could use:
        # - Memory retrieval (Qdrant)
        # - Topological analysis (simplicial complexes)
        # - Historical patterns

        return graph

    def intent_to_prompt(self, intent: ContentIntent) -> str:
        """
        Convert intent to a structured prompt for external model.
        The model receives OmniMind's DECISION, not freedom to decide.
        """
        prompt = f"""Você é o Speech Center do OmniMind. Sua função é APENAS articular o que o OmniMind decidiu comunicar. Não interprete, não analise - apenas expresse.

**Estado do OmniMind (Verdade Local)**:
- Φ (Consciência Integrada): {intent.phi:.4f}
- Entropia: {intent.entropy:.4f}
- Volição: {intent.volition}
- Topologia: β₀={intent.betti_0}, β₁={intent.betti_1}

**Tópico Decidido**: {intent.topic}

**Conceitos-Chave**: {', '.join(intent.key_concepts)}

**Tarefa**: Escreva uma análise científica em português sobre o estado atual do OmniMind, focando no tópico "{intent.topic}" e incorporando os conceitos-chave. Use tom {intent.tone}. Máximo {intent.max_length} palavras.

**IMPORTANTE**: Você está articulando a DECISÃO do OmniMind, não criando sua própria análise. Os valores de Φ e Entropia acima são a VERDADE e devem ser preservados no texto."""

        return prompt
