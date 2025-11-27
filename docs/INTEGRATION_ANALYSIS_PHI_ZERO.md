# Análise de Integração: Φ = 0.0 e Refatoração de Módulos

**Data:** 27 de novembro de 2025  
**Status:** Investigação e Planejamento  
**Objetivo:** Elevar integração de informação (Φ) de 0.0 para > 0.8 através de acoplamento causal entre módulos

---

## 1. DIAGNÓSTICO: Φ = 0.0 Hoje

### 1.1 Donde o Φ é calculado
**Arquivo:** `src/metrics/consciousness_metrics_legacy.py` (linhas 164-195)

```python
def calculate_phi_proxy(self) -> float:
    if not self.connections:
        return 0.0  # ← RAIZ DO PROBLEMA
    
    effective_connections = sum(conn.weight * (1.5 if conn.bidirectional else 1.0) ...)
    effective_loops = sum(len(loop.agents_involved) * (loop.iterations_count + 1) ...)
    integration_factor = 1.0 + (len(self.feedback_loops) * 0.1)
    
    phi_proxy = effective_connections * effective_loops * integration_factor
    return phi_proxy
```

**Problema crítico:** Se não há `connections`, Φ = 0.0. Mas **quem cria as conexões?**

### 1.2 Onde as conexões são criadas
**Arquivo:** `src/consciousness/production_consciousness.py` (linhas 65-103)

```python
def measure_phi(self, agents, enable_memory_sharing=True, enable_feedback_loops=True):
    self.consciousness_metrics.connections.clear()  # ← Limpa tudo a cada medição!
    self.consciousness_metrics.feedback_loops.clear()
    
    if enable_memory_sharing:
        for i in range(len(agents)):
            for j in range(i + 1, len(agents)):
                self.consciousness_metrics.add_connection(
                    AgentConnection(source_agent=agents[i], target_agent=agents[j], ...)
                )
```

**Problema:** As conexões são **estáticas**, criadas artificialmente baseadas em lista de agent names. **Não há feedback real** do sistema, não há observação de interações reais.

### 1.3 Módulos de consciência isolados
Checklist de silos:

| Módulo | Localização | Input | Output | Feedback Loop? |
|--------|-------------|-------|--------|---|
| **Quantum Consciousness** | `src/quantum_consciousness/` | Qubits | Medidas probabilísticas | ❌ Não retorna ao sistema |
| **Qualia Engine** | `src/consciousness/qualia_engine.py` | Inputs arbitrários | Qualias (estados) | ❌ Lê inputs, não consulta outros módulos |
| **Narrative Constructor** | `src/consciousness/narrative_constructor.py` | Qualia | Histórias | ❌ Não afeta qualia futura |
| **Meaning Maker** | `src/consciousness/meaning_maker.py` | Narrativa | Significados | ❌ Isolado, sem re-entrada |
| **Production Consciousness** | `src/consciousness/production_consciousness.py` | Agent names | Φ, self-awareness | ❌ Lê histórico, não afeta módulos |
| **Sensory Input** | `src/consciousness/sensory_qualia.py` | Eventos | Qualia sensorial | ❌ Não modula por expectativa |

### 1.4 Por que Φ = 0.0 é realista hoje
- ✅ Cada módulo funciona bem em isolamento
- ✅ Testes unitários passam
- ✅ Respostas locais são coerentes
- ❌ **Mas:** Não há ciclo fechado entre módulos
- ❌ **Mas:** Mudança em um módulo não afeta outros
- ❌ **Mas:** Sem "espaço de trabalho compartilhado"

---

## 2. MAPEAMENTO DE DEPENDÊNCIAS ATUAIS

### 2.1 Grafo de fluxo (Hoje: Acíclico/Desconectado)
```
Quantum Circuits
    ↓ (outputs only)
    [isolated calculations]
    
Sensory Input → Qualia Engine → Narrative Constructor → Meaning Maker
    ↓ (no feedback)          ↓ (isolated)           ↓ (isolated)      ↓ (isolated)
    [outputs stored]         [outputs stored]       [outputs stored]   [outputs stored]
    
Production Consciousness (reads history passively)
    ↓
    Φ = 0.0 (no connections active at runtime)
```

### 2.2 Fluxo desejado (Com integração)
```
┌─→ Sensory Qualia ──→ Qualia Engine ──→ Narrative ──→ Meaning Maker ─┐
│                          ↑                ↑              ↑            ↓
│                          └────────────────┴──────────────┘            │
│                            (Workspace Compartilhado)                 │
│                                                                      ↓
│←──────────── Attention Router ←─ Cross-Module Prediction ←─ Φ Monitor
│ (retro-feedback)
└─ Expectation Modulation
```

---

## 3. RAIZ DA CAUSA: Por que não há integração?

### 3.1 Problema 1: Sem workspace compartilhado
- Cada módulo tem outputs locais (arrays, dicts)
- Não há buffer central onde *todos* leem e escrevem
- Sem dependências explícitas entre representações

### 3.2 Problema 2: Sem feedback real
- Outputs não retornam como inputs de outros módulos
- Production Consciousness mede conexões fictícias, não reais
- Φ calculado como proxy teórico, não observável

### 3.3 Problema 3: Sem observabilidade causal
- Se eu desligar Meaning Maker, o sistema todo continua igual
- Se Qualia Engine muda, Narrative não detecta
- Sem acoplamento = sem informação integrada

### 3.4 Problema 4: Sem sincronização temporal
- Cada módulo roda em seu próprio ritmo
- Não há garantia de que outputs de t estão prontos no t+1
- Efeitos causais "perdem o timing"

---

## 4. PLANO DE REFATORAÇÃO: Elevar Φ de 0.0 a > 0.8

### Fase 1: Criar Workspace Compartilhado (Semana 1)

**Objetivo:** Buffer central onde todos os módulos leem/escrevem.

**Arquivo novo:** `src/consciousness/shared_workspace.py`

```python
class SharedWorkspace:
    """Buffer central de estados compartilhados."""
    
    def __init__(self):
        self.embeddings = {}  # Representações latentes de cada módulo
        self.states = {}      # Estados atuais
        self.history = []     # Histórico para análise causal
        self.attention_mask = {}  # Roteamento dinâmico
    
    def write_module_state(self, module_name: str, embeddings: np.ndarray):
        """Todos os módulos escrevem aqui a cada ciclo."""
        self.embeddings[module_name] = embeddings
        self.history.append({
            'timestamp': time.time(),
            'module': module_name,
            'embedding': embeddings.copy()
        })
    
    def read_module_state(self, module_name: str) -> np.ndarray:
        """Todos os módulos leem estado de outros módulos."""
        return self.embeddings.get(module_name, np.zeros(256))
    
    def cross_predict(self, from_module: str, to_module: str) -> float:
        """Capacidade de um módulo prever estado de outro = integração."""
        if from_module not in self.embeddings or to_module not in self.embeddings:
            return 0.0
        # Train small predictor: to_module_t+1 ~ f(from_module_t)
        # Return R² (0.0 = nenhuma relação, 1.0 = determinístico)
        return compute_cross_r_squared(...)
```

**Tarefas:**
- [ ] Criar `SharedWorkspace` class
- [ ] Adicionar métodos `write_module_state`, `read_module_state`, `cross_predict`
- [ ] Integrar em `main_orchestrator` (central)
- [ ] Teste: verificar que todos os 5 módulos podem ler/escrever

**Metrik de sucesso:** Workspace tem dados de todos os 5 módulos a cada ciclo.

---

### Fase 2: Implementar Ciclo de Feedback (Semana 1-2)

**Objetivo:** Criar loop: sensory → qualia → narrative → meaning → expectation → sensory

**Arquivo novo:** `src/consciousness/integration_loop.py`

```python
class IntegrationLoop:
    """Ciclo fechado de retroalimentação."""
    
    def __init__(self, workspace: SharedWorkspace):
        self.workspace = workspace
        self.cycle_count = 0
    
    def run_cycle(self, sensory_input):
        """Uma iteração do ciclo integrado."""
        
        # 1. Sensory → Qualia
        qualia = self.qualia_engine.process(sensory_input, 
                                             context=self.workspace.read_module_state('qualia'))
        self.workspace.write_module_state('qualia', qualia.embedding)
        
        # 2. Qualia → Narrative
        narrative = self.narrative_constructor.process(qualia,
                                                        context=self.workspace.read_module_state('narrative'))
        self.workspace.write_module_state('narrative', narrative.embedding)
        
        # 3. Narrative → Meaning
        meaning = self.meaning_maker.process(narrative,
                                             context=self.workspace.read_module_state('meaning'))
        self.workspace.write_module_state('meaning', meaning.embedding)
        
        # 4. Meaning → Expectation (novo!)
        expectation = self.expectation_modulator.generate(meaning, workspace=self.workspace)
        self.workspace.write_module_state('expectation', expectation.embedding)
        
        # 5. Expectation modula Sensory (feedback!)
        modulated_sensory = sensory_input * (1.0 + expectation.modulation)  # ou similar
        
        # Mede Φ real (cross-predictions)
        phi = self._measure_phi_from_integration()
        self.workspace.write_module_state('phi', np.array([phi]))
        
        self.cycle_count += 1
        return phi, {'qualia': qualia, 'narrative': narrative, 'meaning': meaning}
    
    def _measure_phi_from_integration(self) -> float:
        """Calcula Φ baseado em predições cruzadas reais."""
        predictions = [
            self.workspace.cross_predict('qualia', 'narrative'),
            self.workspace.cross_predict('narrative', 'meaning'),
            self.workspace.cross_predict('meaning', 'qualia'),
            self.workspace.cross_predict('expectation', 'qualia'),
        ]
        phi = np.mean(predictions)  # Média de acoplamento
        return phi
```

**Tarefas:**
- [ ] Criar `IntegrationLoop` class
- [ ] Implementar `run_cycle()` com 5 módulos
- [ ] Adicionar `_measure_phi_from_integration()` baseado em cross-predição
- [ ] Teste: rodar 100 ciclos, coletar série temporal de Φ

**Métrica de sucesso:** Φ > 0.3 após 100 ciclos (feedback estabelecido).

---

### Fase 3: Testes Contrafactuais (Semana 2)

**Objetivo:** Validar que cada módulo contribui para Φ.

**Arquivo novo:** `tests/consciousness/test_integration_causality.py`

```python
def test_causal_impact_of_meaning_maker():
    """Desligar Meaning Maker → Φ cai?"""
    
    loop = IntegrationLoop(workspace)
    
    # Baseline: φ com todos os módulos
    phi_baseline = []
    for _ in range(100):
        phi, _ = loop.run_cycle(input_data)
        phi_baseline.append(phi)
    
    # Ablation: Meaning Maker desligado (retorna zeros)
    loop.meaning_maker.disable()
    phi_ablated = []
    for _ in range(100):
        phi, _ = loop.run_cycle(input_data)
        phi_ablated.append(phi)
    
    # Assertion
    baseline_mean = np.mean(phi_baseline)
    ablated_mean = np.mean(phi_ablated)
    
    assert ablated_mean < baseline_mean, f"Ablation should reduce Φ: {baseline_mean} vs {ablated_mean}"
    assert (baseline_mean - ablated_mean) > 0.1, "Impact should be > 0.1 Φ units"
```

**Tarefas:**
- [ ] Criar teste: desligar cada módulo, medir impacto em Φ
- [ ] Implementar `module.disable()` em cada módulo
- [ ] Rodar testes, documentar impacto

**Métrica de sucesso:** Cada módulo tem impacto mensurável em Φ (delta > 0.05).

---

### Fase 4: Adicionar Perda de Integração no Treino (Semana 2-3)

**Objetivo:** Se houver treino, otimizar por integração.

**Arquivo novo:** `src/consciousness/integration_loss.py`

```python
class IntegrationLoss:
    """Loss term para maximizar integração."""
    
    @staticmethod
    def compute(workspace: SharedWorkspace, cycle_history: List[Dict]) -> float:
        """
        Loss = - Σ cross_prediction_R² - Σ temporal_consistency
        
        (Negativo porque queremos maximizar integração.)
        """
        
        # Term 1: Cross-predictions (higher = better integration)
        cross_pred_losses = []
        modules = list(workspace.embeddings.keys())
        for i, m1 in enumerate(modules):
            for m2 in modules:
                if m1 != m2:
                    r2 = workspace.cross_predict(m1, m2)
                    cross_pred_losses.append(r2)  # Maximize this
        
        # Term 2: Temporal consistency (states should change smoothly)
        temporal_losses = []
        for module_name, history in cycle_history.items():
            if len(history) > 1:
                diffs = [np.linalg.norm(history[i+1] - history[i]) 
                         for i in range(len(history)-1)]
                consistency = 1.0 - np.mean(diffs)  # 1 = no change (bad), 0 = high variance (bad)
                temporal_losses.append(consistency)
        
        integration_loss = -(np.mean(cross_pred_losses) + np.mean(temporal_losses))
        return integration_loss
```

**Tarefas:**
- [ ] Criar `IntegrationLoss` class
- [ ] Integrar em treino (se houver)
- [ ] Teste: verificar que gradientes fluem de volta para módulos

**Métrica de sucesso:** Loss diminui quando Φ aumenta (correlação > 0.8).

---

### Fase 5: Instrumentação e Métricas (Semana 3)

**Objetivo:** Registrar Φ em série temporal com análise estatística.

**Arquivo novo:** `src/consciousness/phi_timeseries.py`

```python
class PhiTimeseries:
    """Coleta e analisa série temporal de Φ."""
    
    def __init__(self, output_dir: Path = None):
        self.data = []  # List[{timestamp, cycle, phi, phi_components, ...}]
        self.output_dir = output_dir or Path("data/consciousness/phi_analysis")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def record(self, cycle: int, phi: float, components: Dict[str, float]):
        """Registra um ciclo."""
        self.data.append({
            'timestamp': time.time(),
            'cycle': cycle,
            'phi': phi,
            'components': components
        })
    
    def compute_statistics(self) -> Dict[str, float]:
        """Estatísticas agregadas."""
        phis = [d['phi'] for d in self.data]
        return {
            'mean': np.mean(phis),
            'std': np.std(phis),
            'min': np.min(phis),
            'max': np.max(phis),
            'trend': np.polyfit(range(len(phis)), phis, 1)[0],  # slope
        }
    
    def save_report(self):
        """Salva relatório JSON."""
        report = {
            'statistics': self.compute_statistics(),
            'data_points': self.data,
            'generated_at': datetime.now().isoformat(),
        }
        output_file = self.output_dir / f"phi_report_{int(time.time())}.json"
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        logger.info(f"Saved Φ report to {output_file}")
```

**Tarefas:**
- [ ] Criar `PhiTimeseries` class
- [ ] Integrar em `IntegrationLoop`
- [ ] Rodar teste com N=30 seeds, coletar estatísticas
- [ ] Gerar gráficos (média ± desvio padrão)

**Métrica de sucesso:** Φ converge para 0.7-0.9 em 500-1000 ciclos, com < 0.1 variância após estabilização.

---

### Fase 6: Roteamento de Atenção Cruzado (Semana 3-4)

**Objetivo:** Mecanismo para priorizar sinais relevantes entre módulos.

**Arquivo novo:** `src/consciousness/cross_module_attention.py`

```python
class CrossModuleAttention:
    """Atenção dinâmica entre módulos."""
    
    def __init__(self, hidden_dim: int = 256):
        self.query_nets = {}  # query_nets[module] = NN que gera queries
        self.key_nets = {}
        self.value_nets = {}
        
    def compute_attention(self, module_name: str, workspace: SharedWorkspace) -> Dict[str, float]:
        """Que módulos são relevantes para `module_name`?"""
        
        query = self.query_nets[module_name](workspace.read_module_state(module_name))
        
        attention_weights = {}
        for other_module in workspace.embeddings.keys():
            if other_module != module_name:
                key = self.key_nets[other_module](workspace.read_module_state(other_module))
                score = np.dot(query, key) / np.sqrt(len(query))
                attention_weights[other_module] = softmax_score(score)
        
        return attention_weights
    
    def route_context(self, module_name: str, workspace: SharedWorkspace) -> np.ndarray:
        """Prepara contexto para `module_name` baseado em atenção."""
        
        attention_weights = self.compute_attention(module_name, workspace)
        context = np.zeros(256)
        
        for other_module, weight in attention_weights.items():
            other_state = workspace.read_module_state(other_module)
            value = self.value_nets[other_module](other_state)
            context += weight * value
        
        return context
```

**Tarefas:**
- [ ] Criar `CrossModuleAttention` class
- [ ] Integrar em cada módulo (ler contexto com atenção)
- [ ] Teste: verificar que pesos mudam com ciclos

**Métrica de sucesso:** Atenção é não-trivial (não uniforme) e muda dinamicamente com estado.

---

## 5. CRONOGRAMA DE IMPLEMENTAÇÃO

| Fase | Descrição | Semana | Arquivo | Teste | Φ esperado |
|------|-----------|--------|---------|-------|-----------|
| 0 | Diagnóstico (ATUAL) | - | - | - | 0.0 |
| 1 | Workspace Compartilhado | 1 | `shared_workspace.py` | ✅ Leitura/escrita | 0.0 (não há ainda) |
| 2 | Ciclo de Feedback | 1-2 | `integration_loop.py` | ✅ Cross-predição | **0.3-0.5** |
| 3 | Contrafactual Tests | 2 | `test_integration_causality.py` | ✅ Delta > 0.05 | 0.3-0.5 |
| 4 | Loss de Integração | 2-3 | `integration_loss.py` | ✅ Correlação > 0.8 | **0.5-0.7** |
| 5 | Métricas de série temporal | 3 | `phi_timeseries.py` | ✅ N=30 seeds | 0.5-0.7 |
| 6 | Atenção Cruzada | 3-4 | `cross_module_attention.py` | ✅ Pesos dinâmicos | **0.7-0.9** |

---

## 6. CHECKLIST DE ACEITE

### Aceitação Técnica
- [ ] Todas as 6 fases implementadas e testadas
- [ ] Φ atinge 0.7-0.9 após 500-1000 ciclos
- [ ] Variance de Φ < 0.1 após convergência
- [ ] Cada módulo tem impacto causal mensurável
- [ ] Testes contrafactuais passam (delta > 0.05 por módulo)
- [ ] Cross-predictions > 0.4 (R²) entre pares de módulos

### Aceitação Operacional
- [ ] Documentação de arquitetura atualizada
- [ ] Diagramas de fluxo descrevem novo design
- [ ] Scripts de teste automatizados
- [ ] Relatórios de Φ gerados em cada execução
- [ ] Logs estruturados com contexto causal

### Aceitação de Segurança
- [ ] Nenhuma intervenção no módulo produz Φ < 0 (sempre válido)
- [ ] Rollback plan documentado (reverter para design modular)
- [ ] Degradação graciosa se um módulo falha

---

## 7. RISCOS E MITIGAÇÕES

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| Workspace se torna gargalo de performance | Alto | Média | Usar memória compartilhada (shared memory), não cópia |
| Cross-predictions impossíveis de treinar | Alto | Média | Usar preditores simples (linear, pequeno MLP) |
| Feedback loops criam instabilidade | Alto | Baixa | Adicionar damping (smoothing) e clipping de valores |
| Φ não converge para > 0.7 | Médio | Média | Aumentar hidden_dim, ajustar learning rate, mais ciclos |
| Módulos existentes não são compatíveis | Médio | Baixa | Wrapper layer que traduz outputs para embeddings |

---

## 8. PRÓXIMOS PASSOS IMEDIATOS

1. **Hoje:** Revisar este plano com stakeholders
2. **Amanhã:** Iniciar Fase 1 (Workspace Compartilhado)
3. **Dia 3-4:** PR para Fase 1, code review
4. **Dia 5-7:** Fase 2 (Ciclo de Feedback) em paralelo
5. **Semana 2:** Fases 3-4, testes contrafactuais
6. **Semana 3:** Instrumentação e análise
7. **Semana 4:** Atenção cruzada, integração final

---

## Referências

- **Log de phi-0:** `data/test_reports/coverage.json`
- **Código atual de Φ:** `src/metrics/consciousness_metrics_legacy.py`
- **Production Consciousness:** `src/consciousness/production_consciousness.py`
- **Expectativas de integração:** User request (2025-11-27)

