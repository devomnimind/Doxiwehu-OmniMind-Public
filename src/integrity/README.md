# Integrity Module - Phase 26D

**Status**: ✅ Fase 1 Implementada
**Data**: 2025-12-05

## Visão Geral

O **Phase 26D** implementa filtragem de viés e validação semântica para garantir integridade do conhecimento:

- **Conflict Detection**: Detecta contradições e incompatibilidades
- **Bias Quantification**: Quantifica viés em fontes de conhecimento
- **Intelligent Integration**: Integração inteligente com flags de incerteza
- **Semantic Coherence**: Validação de coerência semântica
- **Continuous Refinement**: Refinamento contínuo baseado em validação

## Componentes

### 1. ConflictDetectionEngine (`conflict_detection_engine.py`)

Detecta conflitos e contradições no conhecimento:

```python
from integrity import ConflictDetectionEngine

engine = ConflictDetectionEngine()

# Detectar conflitos
conflicts = engine.detect_conflicts("consciousness integration")

# Obter conflitos para uma entidade
entity_conflicts = engine.get_conflicts_for_entity("consciousness")
```

### 2. BiasQuantifier (`bias_quantifier.py`)

Quantifica viés em fontes de conhecimento:

```python
from integrity import BiasQuantifier

quantifier = BiasQuantifier()

# Quantificar viés
bias_score = quantifier.quantify_bias(
    source_id="paper_1",
    source_type="paper",
    content={"text": "Western approaches..."}
)

# Obter score de viés
score = quantifier.get_bias_score("paper_1")
```

## Integração

- **Phase 26B**: Usa `SemanticSearchEngine` e `KnowledgeIntegrator` para buscar conhecimento
- **Phase 26A**: Valida conhecimento nas 3 camadas (Declarative, Procedural, Episodic)

## Testes

```bash
# Rodar testes
pytest tests/integrity/ -v
```

## Status de Implementação

| Componente | Status | Notas |
|------------|-------|-------|
| ConflictDetectionEngine | ✅ Completo | Detecta contradições e incompatibilidades |
| BiasQuantifier | ✅ Completo | Quantifica viés em fontes |
| IntelligentIntegrator | ✅ Completo | Integração com flags de incerteza |
| SemanticCoherenceValidator | ✅ Completo | Validação de coerência semântica |
| ContinuousRefiner | ✅ Completo | Refinamento contínuo baseado em validação |

## Exemplos de Uso

### Fluxo Completo

```python
from integrity import (
    ConflictDetectionEngine,
    BiasQuantifier,
    IntelligentIntegrator,
    SemanticCoherenceValidator,
    ContinuousRefiner,
)

# 1. Integrar conhecimento com flags de incerteza
integrator = IntelligentIntegrator()
integrated = integrator.integrate_knowledge(
    "concept_1",
    {"name": "consciousness", "definition": "..."},
    source_type="paper"
)

# 2. Validar coerência
validator = SemanticCoherenceValidator()
coherence_report = validator.validate_coherence()

# 3. Refinar baseado em validação
refiner = ContinuousRefiner()
refined = refiner.refine_knowledge(
    "concept_1",
    {"timestamp": "2025-12-05T00:00:00Z"},
    was_correct=True
)

# 4. Obter relatório de qualidade
quality_report = refiner.get_knowledge_quality_report()
```

---

**Autor**: OmniMind Development
**License**: MIT
**Data**: 2025-12-05

