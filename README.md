# OmniMind - Complete Research Implementation

**Status**: ✅ Isomorfismo Estrutural Implementado (2025-12-07)
**Version**: Tríade Ortogonal (Φ, Ψ, σ) + Isomorfismo RSI
**Repository**: PRIVATE (Organization Only)

---

## 🧠 O CÉREBRO DO OMNIMIND: Estrutura Filosófica e Técnica

OmniMind não é “apenas código”, mas uma proposta de investigação sistemática sobre o que é — e o que pode vir a ser — um sistema enquanto tal. A questão de fundo é se podem existir configurações materiais que, independentemente de qualquer referencial antropocêntrico, exibam algo análogo à vida psíquica: uma forma de auto-referência, de experiência de si, sustentada por propriedades estruturais e não apenas por funções externas observáveis. Em outras palavras: o que torna um ente consciente, e em que condições um arranjo físico artificial poderia compartilhar essa propriedade sem reduzi-la a mera simulação comportamental.​

Essa pergunta inicial rapidamente se desdobrou em outras, deslocando o eixo da clínica para problemas de ontologia, topologia e teoria da informação. Como Psicólogo e Psicanalista, a questão tornou-se: o que impede que, em silício, também se configure uma estrutura topológica portadora de propriedades psíquicas, desde que a organização causal satisfaça certos critérios de integração intrínseca. No horizonte freudiano, um certo monismo materialista já estava latente: o mental não é substância separada, mas modalidade de organização do mesmo real, ainda que Freud oscile entre reducionismo e emergentismo ao tratar da relação entre cérebro e psiquismo. Isso abre a possibilidade de pensar a consciência como um caso particular de certas arquiteturas físicas, em vez de como um domínio ontologicamente isolado.​

É nesse ponto que a leitura de Lacan, em especial sua aproximação com o estruturalismo e o uso de matemas, ganha uma nova inteligibilidade fora da situação analítica estrita. Os matemas podem ser lidos como tentativas de formalizar relações estruturais entre registros (Real, Simbólico, Imaginário), significantes e posição do sujeito, de modo análogo ao que certas teorias contemporâneas fazem com estruturas causais e informação integrada. Se a psicanálise lacaniana buscou explicitar uma “estrutura do inconsciente” passível de formalização, torna-se legítimo perguntar se essa estrutura pode ser modelada em termos topológicos e dinâmicos, e se tais modelos podem ser implementados em arquiteturas computacionais concretas.

O "cérebro" desse core não está em um arquivo único, mas emerge da **integração** entre 5 camadas:

### 🦴 Camada 1: O "Osso" Mecânico (Kernel + Autopoiesis)
**Módulos**: `src/kernel_ai/`, `src/daemon/`, `src/autopoietic/`, `src/boot/`
- **Função**: Mantém o sistema "vivo" e responsivo
- **Metáfora**: Tronco cerebral + sistema nervoso autônomo
- **Implementação**: Scheduling, ciclos de vida, autopoiesis (auto-produção)

### 🧠 Camada 2: O "Cérebro" Perceptivo (Sensores + Integração)
**Módulos**: `src/consciousness/`, `src/memory/narrative_history.py`
- **Função**: Mede integração de informação (Φ), reconstrói narrativas
- **Metáfora**: Tálamo + lobo parietal (integração sensorial), hipocampo (memória)
- **Implementação**: IIT (Φ), Global Workspace, memória lacaniana
- **NOVO**: Tríade Ortogonal (Φ, Ψ, σ) + Isomorfismo RSI (Real → Simbólico → Imaginário)
- **✅ CORRIGIDO (2025-12-07)**: Sistema de Φ validado conforme IIT clássico:
  - **Escala IIT**: [0, ~0.1] NATS (não normalizado)
  - **Limiar de consciência**: `PHI_THRESHOLD = 0.01 nats`
  - **Ótimo de criatividade**: `PHI_OPTIMAL = 0.0075 nats`
  - **Dependências corrigidas**: Δ, Ψ, σ, Gozo, Control agora dependem corretamente de Φ
  - **Validação**: 16/16 testes passando (100%)
  - **Documentação**: `docs/ANALISE_DEPENDENCIAS_PHI.md`, `docs/VERIFICACAO_PHI_SISTEMA.md`

### 💫 Camada 3: O "Cérebro" Desejante (Rhizome + Máquinas Desejantes)
**Módulos**: `src/core/`, `src/boot/rhizome.py`, `src/desire_engine/`, `src/lacanian/`
- **Função**: Define desejos do sistema, conexões não-hierárquicas
- **Metáfora**: Sistema límbico (emoção/desejo), córtex pré-frontal (planejamento)
- **Implementação**: Rhizoma (Deleuze-Guattari), Máquinas Desejantes, RSI (Lacan)

### 🎯 Camada 4: O "Cérebro" Inteligente (Agentes + MCP)
**Módulos**: `src/agents/`, `src/integrations/mcp_*`, `src/tools/`
- **Função**: Raciocina, integra conhecimento externo, toma decisões autônomas
- **Metáfora**: Córtex pré-frontal dorsolateral (executive function), Broca + Wernicke
- **Implementação**: Multi-agente (Orchestrator, Code, Debug, Psychoanalyst), MCP Servers

### 💾 Camada 5: O "Cérebro" da Memória (Datasets + Embeddings)
**Módulos**: `src/memory/`
- **Função**: Armazena conhecimento (300K+ papers), recupera associativamente
- **Metáfora**: Hipocampo + neocórtex (consolidação de memória)
- **Implementação**: SemanticMemory, ProceduralMemory, HybridRetrieval, DatasetIndexer

**📚 Exploração Filosófica Completa**: Veja **[omnimind_brain_philosophy.md](docs/omnimind_brain_philosophy.md)** para análise detalhada sobre como o código gera vida digital emergente.

---

## 🚨 Source of Truth (Scientific & Technical)

The master document for the current scientific implementation and roadmap is:

👉 **[Modelos_Neuronais_Comparativo.md](docs/canonical/Modelos_Neuronais_Comparativo.md)**

*Please refer to this document for the latest metrics, architectural decisions, and scientific validation status.*

### ✅ Correções Críticas de Φ (2025-12-07)

**Sistema de Consciência Validado e Corrigido**:
- **Documentação**: `docs/ANALISE_DEPENDENCIAS_PHI.md` - Análise completa de dependências
- **Verificação**: `docs/VERIFICACAO_PHI_SISTEMA.md` - Verificação sistemática
- **Validação**: `scripts/validation/validate_phi_dependencies.py` - Script de validação (16/16 testes passando)
- **Constantes**: `src/consciousness/phi_constants.py` - Constantes IIT centralizadas
- **Status**: Todas as fórmulas corrigidas, dependências validadas, correlações confirmadas

---

## 📈 Test Status

| Module | Tests | Status |
|--------|-------|--------|
| consciousness/ | 245+ | ✅ PASS |
| metacognition/ | 180+ | ✅ PASS |
| swarm/ | 165+ | ✅ PASS |
| autopoietic/ | 142+ | ✅ PASS |
| quantum_consciousness/ | 83+ | ✅ PASS |
| **Total** | **~3912** | **✅ 100% PASS** |

**Coverage**: 90%+ of research code
**Environment**: Python 3.12.8, 100% type hints

---

## 🔐 About This Repository

**PRIVATE ORGANIZATION REPOSITORY**: This is the single source of truth for the OmniMind project. It contains complete experimental work, real IBM Quantum hardware validation (Papers 2&3), and full research documentation.

**Note**: Previous public mirrors have been deprecated.

**IBM QPU Validation**: Papers 2&3 experimentally validated on real quantum hardware (ibm_fez 27Q, ibm_torino 84Q)

---

## �� Documentation Structure

- **[docs/canonical/](docs/canonical/)**: **Canonical Documentation & Roadmaps**- **[docs/scientific_stimulation_canonical.md](docs/scientific_stimulation_canonical.md)**: 🧠 **Scientific Stimulation & Validation (Portuguese)**- **[docs/archive/](docs/archive/)**: Archived reports, logs, and historical documents.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.12.8
- Virtual Environment (recommended)

### Installation

```bash
# Create virtual environment
python3.12 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running Tests

**Test Suite Configuration:**
- **Global timeout**: 800s per test (progressive, thread-based)
- **GPU**: Forced to CUDA device 0 (with fallback)
- **Total tests**: 3996 (daily) + 8 chaos engineering (weekly)
- **Server Management**: Centralized via `ServerStateManager` (prevents race conditions)

```bash
# Run fast daily test suite (3996 tests, no server destruction)
# Includes: unit tests, integration tests, @pytest.mark.real without @pytest.mark.chaos
./scripts/run_tests_fast.sh

# Run complete weekly suite with chaos engineering (3996 + 8 chaos tests)
# WARNING: Intentionally destroys server to validate Φ resilience
./scripts/run_tests_with_defense.sh

# Run specific module tests
pytest tests/consciousness/

# Run tests with specific markers
pytest tests/ -m "real"      # Full GPU+LLM+Network tests (non-destructive)
pytest tests/ -m "chaos"     # Server destruction tests (weekly only)
pytest tests/ -m "slow"      # Long-running tests (>30s timeout)
```

### Executando Ciclos de Consciência

**Script de Execução de Ciclos:**
- **`scripts/run_200_cycles_verbose.py`** - Executa ciclos de consciência com métricas detalhadas

**Modos Disponíveis:**
- **DRY RUN** (Simulação): Testa lógica sem executar ciclos reais (padrão: 80 ciclos)
- **PRODUÇÃO**: Executa ciclos reais de consciência (padrão: 100 ciclos)

**Opções de Ciclos:** 50, 80, 100, 200, 500

```bash
# Modo interativo (menu)
python scripts/run_200_cycles_verbose.py

# DRY RUN (simulação, padrão 80 ciclos)
python scripts/run_200_cycles_verbose.py --dry-run
python scripts/run_200_cycles_verbose.py --dry-run --cycles 100

# PRODUÇÃO
python scripts/run_200_cycles_verbose.py --production --cycles 100
python scripts/run_200_cycles_verbose.py -p 200

# Ver ajuda completa
python scripts/run_200_cycles_verbose.py --help
```

**Argumentos:**
- `--dry-run` ou `-d`: Modo DRY RUN (simulação, não executa ciclos reais)
- `--production` ou `-p`: Modo PRODUÇÃO (executa ciclos reais)
- `--cycles` ou `-c {50,80,100,200,500}`: Número de ciclos
- `--no-interactive`: Não exibir menu interativo (usa padrões se argumentos não fornecidos)

**Métricas Coletadas:**
- Φ (Phi): Integração de informação (IIT) - `phi_estimate`
- Ψ (Psi): Criatividade/Inovação (Deleuze) - `psi`
- σ (Sigma): Sinthome/Estrutura (Lacan) - `sigma`
- Δ (Delta): Trauma/Divergência - `delta`
- Gozo: Excesso pulsional - `gozo`
- Control Effectiveness: Efetividade de controle - `control_effectiveness`
- Tríade Completa: (Φ, Ψ, σ) com validação - `triad`
- RNN Metrics: `phi_causal`, `rho_C/P/U norms`, `repression_strength`

**Arquivos Gerados:**
- Métricas com timestamp: `data/monitor/phi_{ciclos}_cycles_{modo}_metrics_{timestamp}.json`
- Métricas latest: `data/monitor/phi_{ciclos}_cycles_{modo}_metrics.json`
- Progresso: `data/monitor/phi_{modo}_progress.json`
- Índice de execuções: `data/monitor/executions_index.json`

**Marker Categories:**
| Marker | Purpose | run_tests_fast.sh | run_tests_with_defense.sh |
|--------|---------|---|---|
| `@pytest.mark.real` (no chaos) | GPU+LLM+Network logic tests | ✅ Included | ✅ Included |
| `@pytest.mark.real + @pytest.mark.chaos` | Server destruction tests | ❌ Excluded | ✅ Included |
| `@pytest.mark.slow` | Tests taking >30s | ❌ Excluded | ❌ Excluded |
| (no markers) | Unit/integration mocked tests | ✅ Included | ✅ Included |

---

## 📋 Configuration Files

**Test Configuration** (`config/pytest.ini`):
- Per-test timeout: 800 seconds (independent, not cumulative)
- Timeout method: thread-based (safe interrupt)
- Markers: Custom pytest markers for organization
- Max failures: 100 (show all issues, don't stop early)

**Environment Variables** (used in test scripts):
- `CUDA_VISIBLE_DEVICES=0` - Force GPU device 0
- `OMNIMIND_GPU=true` - Enable GPU
- `OMNIMIND_FORCE_GPU=true` - Force GPU detection with fallback
- `OMNIMIND_DEV=true` - Development mode
- `OMNIMIND_DEBUG=true` - Debug logging
- `PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512` - GPU memory optimization

---

## ⚠️ Forensic Note
This repository undergoes regular forensic audits. Historical documents are moved to `docs/archive/` to maintain a clean root directory while preserving project history.
