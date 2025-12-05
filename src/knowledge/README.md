# Knowledge Layers - Phase 26A

**Status**: ✅ Core Implementado & Testado
**Data**: 2025-12-05

## Visão Geral

O **Phase 26A** implementa a estrutura de conhecimento em 3 camadas do OmniMind, permitindo que o sistema armazene e recupere conhecimento de forma estruturada:

- **Layer 1 (Declarative)**: "O que são as coisas" (conceitos, definições)
- **Layer 2 (Procedural)**: "Como se relacionam" (regras, processos)
- **Layer 3 (Episodic)**: "O que já aconteceu" (histórico, experiência)

## Arquitetura

### 1. Declarative Layer (`declarative_layer.py`)

Armazena conceitos e definições:

```python
from knowledge import DeclarativeLayer, Concept

layer = DeclarativeLayer()

concept = Concept(
    id="consciousness_1",
    name="Consciousness",
    definition="Integrated information in a system",
    category="philosophy"
)

layer.store_concept(concept)
concepts = layer.search_concepts("consciousness")
```

### 2. Procedural Layer (`procedural_layer.py`)

Armazena regras e processos:

```python
from knowledge import ProceduralLayer, Rule

layer = ProceduralLayer()

rule = Rule(
    id="memory_opt_1",
    name="Memory Optimization",
    description="Reduce batch size when memory is high",
    rule_type="process",
    conditions=["memory > 90%"],
    actions=["reduce batch_size", "disable cache"]
)

layer.store_rule(rule)
rules = layer.search_rules("memory optimization")
```

### 3. Episodic Layer (`episodic_layer.py`)

Armazena histórico e experiências:

```python
from knowledge import EpisodicLayer, Episode
from datetime import datetime, timezone

layer = EpisodicLayer()

episode = Episode(
    id="ep_1",
    timestamp=datetime.now(timezone.utc),
    event="Memory issue detected and resolved",
    outcome="Memory usage reduced from 95% to 60%",
    learned="Reducing batch_size helps with memory"
)

layer.store_episode(episode)
recent = layer.get_recent_episodes(limit=10)
```

### 4. Knowledge Integrator (`knowledge_integrator.py`)

Integra as 3 camadas para queries cross-layer:

```python
from knowledge import KnowledgeIntegrator

integrator = KnowledgeIntegrator()

# Query across all layers
results = integrator.query("memory optimization")

# Get complete knowledge about an entity
knowledge = integrator.get_full_knowledge("consciousness")

# Get statistics
stats = integrator.get_statistics()
```

## Integração com Phase 24

- **Declarative Layer**: Usa `SemanticMemoryLayer` para busca semântica
- **Procedural Layer**: Usa `SemanticMemoryLayer` para armazenamento
- **Episodic Layer**: Usa `TemporalMemoryIndex` para queries temporais

## Testes

```bash
# Rodar todos os testes
pytest tests/knowledge/ -v

# Teste específico
pytest tests/knowledge/test_declarative_layer.py -v
```

## Status de Implementação

| Componente | Status | Notas |
|------------|-------|-------|
| Declarative Layer | ✅ Completo | Integrado com Phase 24 Semantic Memory |
| Procedural Layer | ✅ Completo | Integrado com Phase 24 Semantic Memory |
| Episodic Layer | ✅ Completo | Integrado com Phase 24 Temporal Memory |
| Knowledge Integrator | ✅ Completo | Queries cross-layer funcionais |

## Próximos Passos

1. **Integração com Phase 26C**: Usar knowledge layers no Solution Lookup Engine
2. **Integração com Phase 26B**: Usar knowledge layers no Learning Loop
3. **DBpedia Integration**: Popular Procedural Layer com DBpedia ontology
4. **Dataset Integration**: Popular Declarative Layer com datasets HuggingFace

---

## Integração DBpedia Ontology (Phase 26A Fase 1.3)

**Status**: ✅ Implementado (2025-12-05)

### Script de Integração

O script `scripts/integrate_dbpedia_ontology.py` integra triples do DBpedia no `ProceduralLayer`:

```bash
# Integrar todos os triples (pode demorar)
python scripts/integrate_dbpedia_ontology.py

# Integrar apenas 1000 triples relacionados a consciência
python scripts/integrate_dbpedia_ontology.py --limit 1000 --filter-consciousness

# Salvar relatório em arquivo customizado
python scripts/integrate_dbpedia_ontology.py --limit 500 --output data/my_report.json
```

### Funcionalidades

- **Carrega DBpedia do HuggingFace**: Usa `CleverThis/dbpedia-ontology`
- **Filtro de consciência**: Opção `--filter-consciousness` filtra triples relacionados
- **Conversão para regras**: Converte triples RDF em regras do `ProceduralLayer`
- **Integração automática**: Armazena regras no `ProceduralLayer`

### Exemplo de Uso

```python
from scripts.integrate_dbpedia_ontology import (
    load_dbpedia_from_huggingface,
    filter_consciousness_related,
    integrate_dbpedia_to_procedural_layer,
)
from knowledge.procedural_layer import ProceduralLayer

# Carregar triples
triples = load_dbpedia_from_huggingface(limit=1000)

# Filtrar relacionados a consciência
consciousness_triples = filter_consciousness_related(triples)

# Integrar no ProceduralLayer
procedural_layer = ProceduralLayer()
integrated = integrate_dbpedia_to_procedural_layer(
    consciousness_triples,
    procedural_layer
)

# Usar as regras
rules = integrated.list_rules()
print(f"Total de regras: {len(rules)}")
```

### Relatório de Integração

O script gera um relatório JSON com:
- `total_triples_loaded`: Total de triples carregados
- `rules_integrated`: Número de regras integradas
- `filter_consciousness`: Se o filtro foi aplicado

---

**Autor**: OmniMind Development
**License**: MIT
**Data**: 2025-12-05

