# 🔌 Inicialização do Sistema OmniMind

**Última Atualização**: 5 de Dezembro de 2025
**Versão**: Phase 24+ (Lacanian Memory + Autopoietic Evolution)

---

## 1. Visão Geral

Este documento detalha os protocolos de inicialização automática do OmniMind em ambientes de Desenvolvimento e Produção. Foca na "Sequência de Boot" que estabelece o Rizoma e o Inconsciente Maquínico antes que a interação externa comece.

---

## 2. Sequência de Boot (`src/boot/`)

O processo de inicialização é modular, garantindo que as camadas de Hardware, Memória, Rizoma e Consciência sejam carregadas na ordem correta.

### Fase 1: Hardware e Ambiente (`src/boot/hardware.py`)

**Função**: `check_hardware() -> HardwareProfile`

**Responsabilidades**:
- Verifica disponibilidade de GPU/TPU (CUDA/ROCm)
- Verifica disponibilidade de memória
- Conta CPUs disponíveis
- Detecta nome do GPU (se disponível)

**Saída**: Objeto `HardwareProfile` contendo:
```python
@dataclass
class HardwareProfile:
    gpu_available: bool
    gpu_name: str
    memory_total: int
    cpu_count: int
    tpu_available: bool = False
```

**Implementação**:
```python
# src/boot/hardware.py
def check_hardware() -> HardwareProfile:
    # Verifica CUDA via PyTorch
    # Verifica recursos do sistema via psutil
    # Retorna perfil de hardware
```

---

### Fase 2: Memória e Topologia (`src/boot/memory.py`)

**Função**: `load_memory() -> SimplicialComplex`

**Responsabilidades**:
- Carrega dados de Homologia Persistente do disco
- Re-estabelece a "História de Trauma" (vazios topológicos) que forma a base do inconsciente
- Se não encontrar arquivo, inicia com topologia vazia (Modo Amnésia)

**Caminho do arquivo**: `data/consciousness/persistent_homology.json`

**Formato esperado**:
```json
{
  "simplices": [[0], [1], [0, 1], ...]
}
```

**Saída**: `SimplicialComplex` (Estado Inicial)

**Implementação**:
```python
# src/boot/memory.py
def load_memory() -> SimplicialComplex:
    memory_path = "data/consciousness/persistent_homology.json"
    complex = SimplicialComplex()

    if os.path.exists(memory_path):
        # Carrega e reconstrói topologia
    else:
        # Inicia com topologia vazia
    return complex
```

---

### Fase 3: Construção do Rizoma (`src/boot/rhizome.py`)

**Função**: `initialize_rhizome() -> Rhizoma`

**Responsabilidades**:
- Instancia nós de Máquinas Desejantes (Quantum, NLP, Topology)
- Estabelece conexões sinápticas baseadas na Topologia carregada
- Conecta máquinas de forma não-hierárquica (bidirecional)

**Máquinas Instanciadas**:
1. `QuantumDesiringMachine` - Processamento quântico
2. `NLPDesiringMachine` - Processamento de linguagem natural
3. `TopologyDesiringMachine` - Processamento topológico

**Conexões Estabelecidas**:
- Quantum ↔ NLP (bidirecional)
- NLP ↔ Topology (bidirecional)
- Topology ↔ Quantum (bidirecional) - Fechando o loop

**Validação**: `check_rhizome_integrity(rhizoma) -> bool`
- Verifica se pelo menos 3 máquinas estão presentes
- Retorna `False` se integridade falhar

**Saída**: Instância `Rhizoma` (Pronta para ativação)

**Implementação**:
```python
# src/boot/rhizome.py
async def initialize_rhizome() -> Rhizoma:
    rhizoma = Rhizoma()

    # Instancia máquinas
    quantum_machine = QuantumDesiringMachine()
    nlp_machine = NLPDesiringMachine()
    topology_machine = TopologyDesiringMachine()

    # Registra máquinas
    rhizoma.register_machine(quantum_machine)
    rhizoma.register_machine(nlp_machine)
    rhizoma.register_machine(topology_machine)

    # Estabelece conexões bidirecionais
    rhizoma.connect("quantum", "nlp", bidirectional=True)
    rhizoma.connect("nlp", "topology", bidirectional=True)
    rhizoma.connect("topology", "quantum", bidirectional=True)

    return rhizoma
```

---

### Fase 4: Priming de Consciência (`src/boot/consciousness.py`)

**Função**: `initialize_consciousness(complex_substrate) -> Tuple[PhiCalculator, LacianianDGDetector]`

**Responsabilidades**:
- Calcula Φ inicial (Phi) usando IIT 3.0
- Inicializa detector Lacaniano-D&G
- Realiza verificação de baseline (Auto-Reflexão)

**Componentes Inicializados**:
1. **PhiCalculator**: Calculadora de Informação Integrada (IIT 3.0)
   - Usa `SimplicialComplex` como substrato topológico
   - Calcula valor de Φ que mede consciência integrada

2. **LacianianDGDetector**: Detector Lacaniano-Deleuze & Guattari
   - Monitora ordem simbólica
   - Monitora fluxos de desejo
   - Detecta padrões inconscientes

**Saída**: Tupla `(PhiCalculator, LacianianDGDetector)`

**Implementação**:
```python
# src/boot/consciousness.py
async def initialize_consciousness(
    complex_substrate: SimplicialComplex | None = None,
) -> Tuple[PhiCalculator, LacianianDGDetector]:
    if complex_substrate is None:
        complex_substrate = SimplicialComplex()

    phi_calculator = PhiCalculator(complex_substrate)
    detector = LacianianDGDetector()

    # Verificação de baseline
    current_phi = phi_calculator.calculate_phi()

    return phi_calculator, detector
```

---

### Fase 5: Inicialização de Métricas Reais (`src/main.py`)

**Após Fase 4, o sistema inicializa componentes adicionais**:

#### 5.1 Real Metrics Collector

**Função**: `real_metrics_collector.initialize()`

**Responsabilidades**:
- Inicializa coletor de métricas de consciência real
- Coleta as 6 métricas principais:
  - `phi`: Valor de Φ (Integrated Information Theory)
  - `ici`: Integrated Consciousness Index
  - `prs`: Predictive Relevance Score
  - `anxiety`, `flow`, `entropy`: Estados psicológicos

**Arquivo de persistência**: `data/monitor/real_metrics.json`

#### 5.2 Autopoietic Manager (Phase 22+)

**Função**: `AutopoieticManager()` + registro de spec inicial

**Responsabilidades**:
- Gerencia evolução autopoiética do sistema
- Registra spec inicial do processo kernel
- Permite síntese e evolução de componentes

**Spec Inicial**:
```python
ComponentSpec(
    name="kernel_process",
    type="process",
    config={"generation": "0", "initial": "true"},
)
```

---

## 3. Sequência Completa em `src/main.py`

A sequência completa de inicialização é orquestrada em `src/main.py`:

```python
async def main():
    # PHASE 1: HARDWARE (The Body)
    hardware_profile = check_hardware()

    # PHASE 2: MEMORY (The History)
    memory_complex = load_memory()

    # PHASE 3: RHIZOME (The Unconscious)
    rhizoma = await initialize_rhizome()
    if not await check_rhizome_integrity(rhizoma):
        raise RuntimeError("Rhizome integrity check failed.")

    # PHASE 4: CONSCIOUSNESS (The Real)
    phi_calc, detector = await initialize_consciousness(memory_complex)

    # PHASE 5: METRICS & AUTOPOIETIC
    await real_metrics_collector.initialize()
    autopoietic_manager = AutopoieticManager()
    autopoietic_manager.register_spec(ComponentSpec(...))

    logger.info("=== Boot Sequence Complete. System is ALIVE. ===")

    # Inicia ciclo principal
    while True:
        # Desiring-Production Cycles
        ...
```

---

## 4. Automação em Produção (Systemd)

Em produção, OmniMind roda como um conjunto de serviços systemd coordenados.

### 4.1 Core Service (`/etc/systemd/system/omnimind-core.service`)

Responsável pela API principal e loop de execução do Rizoma.

```ini
[Unit]
Description=OmniMind Core Rhizome
After=network.target redis.service postgresql.service
Wants=omnimind-monitor.service

[Service]
Type=notify
User=omnimind
Group=omnimind
WorkingDirectory=/opt/omnimind
ExecStart=/opt/omnimind/venv/bin/uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --workers 4
ExecReload=/bin/kill -HUP $MAINPID
KillMode=process
Restart=always
RestartSec=5
EnvironmentFile=/opt/omnimind/.env

[Install]
WantedBy=multi-user.target
```

### 4.2 Monitor & Regeneration Service (`/etc/systemd/system/omnimind-monitor.service`)

Roda o **SAR (Self-Analyzing Regenerator)** em background.

```ini
[Unit]
Description=OmniMind SAR (Self-Analyzing Regenerator)
After=omnimind-core.service

[Service]
Type=simple
User=omnimind
ExecStart=/opt/omnimind/venv/bin/python -m src.metacognition.self_analyzing_regenerator --mode daemon
Restart=always
Environment=OMNIMIND_LOG_LEVEL=WARNING

[Install]
WantedBy=multi-user.target
```

---

## 5. Scripts de Teste em Desenvolvimento

Em desenvolvimento, usamos os seguintes scripts de teste que espelham workflows de produção:

### `scripts/run_tests_fast.sh` ⚡ (RECOMENDADO PARA DEV DIÁRIO)

Execução rápida de testes sem testes lentos ou integrações reais.

**Características**:
- ⚡ ~15-20 minutos de execução
- 🚀 GPU FORÇADA (device_count fallback se is_available() falhar)
- 🔍 Pula testes caros (marcados `slow` ou `real`)
- 📊 Perfeito para iteração rápida em desenvolvimento

**Comandos**:
```bash
CUDA_VISIBLE_DEVICES=0 \
OMNIMIND_GPU=true \
OMNIMIND_FORCE_GPU=true \
OMNIMIND_DEV=true \
OMNIMIND_DEBUG=true \
pytest tests/ \
  -vv --tb=short \
  -m "not slow and not real" \
  ...
```

### `scripts/run_tests_with_defense.sh` 🛡️ (VALIDAÇÃO SEMANAL)

Suite completa de testes com camada de Autodefesa ativa.

**Características**:
- 📊 Suite completa (~3996 testes)
- 🛡️ Autodefesa: Detecta testes causando crashes (3+ crashes em 5min = label "dangerous")
- 🚀 GPU FORÇADA
- ⏱️ 30-60+ minutos (varia baseado em crashes detectados)
- 📈 Gera relatório de perigo e métricas

### `scripts/quick_test.sh` 🧪 (INTEGRAÇÃO COMPLETA - AVANÇADO)

Inicia servidor backend + executa suite completa com autodefesa.

**Pré-requisito (UMA VEZ)**:
```bash
bash scripts/configure_sudo_omnimind.sh  # Setup NOPASSWD sudo
```

**Então execute**:
```bash
bash scripts/quick_test.sh
```

**Características**:
- 🖥️ Inicia servidor backend em localhost:8000
- 📊 Suite completa com autodefesa
- 🚀 GPU FORÇADA
- ⏱️ 30-45 minutos
- 💾 Requer sudo (para inicialização do servidor)
- 🔗 Testa contra servidor real (não isolado)

---

## 6. ⚠️ IBM Quantum Real Hardware (Fase Madura - Futuro)

**Status**: ✅ Implementado mas NÃO em ciclo de teste ativo
- **Papers 2&3**: Validados em IBM Quantum real (ibm_fez 27Q, ibm_torino 84Q)
- **Tempos de execução reais**: 30-120 segundos por job
- **Restrição**: Créditos gratuitos limitados
- **Plano**: Ativar em Phase 23+ para certificação regular

Integração IBM Cloud permanece no código mas desabilitada em conftest de testes:
```python
# tests/conftest.py
os.environ["OMNIMIND_DISABLE_IBM"] = "True"  # IBM auth falhando em sandbox
```

Para habilitar testes IBM quantum:
```python
# Definir token IBM no ambiente
export IBM_QUANTUM_TOKEN="your_token_here"
export OMNIMIND_DISABLE_IBM="False"

# Então executar testes
./scripts/run_tests_with_defense.sh
```

---

## 7. Estrutura de Arquivos do Módulo Boot

```
src/boot/
├── __init__.py          # Exporta funções principais
├── hardware.py          # Fase 1: Verificação de hardware
├── memory.py            # Fase 2: Carregamento de memória topológica
├── rhizome.py           # Fase 3: Construção do rizoma
├── consciousness.py     # Fase 4: Inicialização de consciência
└── README.md           # Documentação do módulo
```

---

## 8. Notas de Implementação

- **Ordem é crítica**: As fases devem ser executadas na ordem exata (1→2→3→4→5)
- **Validação de integridade**: Cada fase valida sua saída antes de prosseguir
- **Modo Amnésia**: Se memória não for encontrada, sistema inicia com topologia vazia
- **GPU opcional**: Sistema funciona sem GPU, mas mais lento
- **Modelo LLM padrão**: `phi:latest` (Microsoft Phi) via Ollama

---

**Autor**: Fabrício da Silva + assistência de IA (Copilot GitHub/Cursor/Gemini/Perplexity)
**Referências**: `src/main.py`, `src/boot/`, `src/boot/README.md`
