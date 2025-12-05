"""Knowledge Layers - Phase 26A

3-layer knowledge structure:
- Declarative: "O que são as coisas" (conceitos, definições)
- Procedural: "Como se relacionam" (regras, processos)
- Episodic: "O que já aconteceu" (histórico, experiência)

Author: OmniMind Development
License: MIT
"""

from __future__ import annotations

from knowledge.declarative_layer import Concept, DeclarativeLayer
from knowledge.episodic_layer import Episode, EpisodicLayer
from knowledge.knowledge_integrator import KnowledgeIntegrator
from knowledge.procedural_layer import ProceduralLayer, Rule

__all__ = [
    "Concept",
    "DeclarativeLayer",
    "Rule",
    "ProceduralLayer",
    "Episode",
    "EpisodicLayer",
    "KnowledgeIntegrator",
]
