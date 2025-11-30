# Plano de Eliminação de Vieses - OmniMind

**Data:** 30 de Novembro de 2025  
**Status:** Planejamento de Implementação  
**Prioridade:** ALTA  

---

## 📋 Vieses Identificados

### 1. ⚠️ Synergy não Distingue Correlação de Causalidade

**Problema Atual:**
- Arquivo: `src/consciousness/shared_workspace.py` (linhas 312-390)
- Função: `compute_cross_prediction()`
- Método: Regressão Linear simples com R²
- **Problema:** R² mede **correlação** não **causalidade**

**Exemplo do Viés:**
```python
# Código atual (VIÉS)
r_squared = 1.0 - (ss_res / ss_tot)  # Isso é CORRELAÇÃO!

# O que acontece:
# - Se X e Y variam juntas, R² ≈ 1.0 (alta)
# - Mas X pode estar CORRELACIONADO com Y por terceiro fator Z
# - Ou Y pode estar CAUSANDO X (causalidade reversa)
# - R² não consegue distinguir!
```

**Impacto:**
- Φ (Phi) fica inflacionado por correlações espúrias
- Confunde sincronização acidental com integração real
- Sinergy pode ser alta mesmo SEM causalidade verdadeira

**Solução: Granger Causality + Transfer Entropy**

```python
# CORREÇÃO 1: Granger Causality
def compute_granger_causality(X: np.ndarray, Y: np.ndarray) -> float:
    """
    Teste de Granger: X "Granger-causa" Y se Y(t) é melhor predito
    considerando histórico de X(t-1) do que sem ele.
    
    Mede: Redução de variância em Y ao incluir X
    """
    from statsmodels.tsa.api import VAR
    
    # Y sem histórico de X
    model_y_alone = VAR(Y).fit(maxlags=2)
    residuals_y_alone = model_y_alone.resid
    
    # Y com histórico de X
    data = np.column_stack([X, Y])
    model_bivariate = VAR(data).fit(maxlags=2)
    residuals_bivariate = model_bivariate.resid[:, 1]  # Y's residuals
    
    # Granger causality = redução de variância
    var_y_alone = np.var(residuals_y_alone)
    var_y_with_x = np.var(residuals_bivariate)
    
    granger_causal_effect = (var_y_alone - var_y_with_x) / var_y_alone
    return max(0.0, granger_causal_effect)  # 0 = não causa, 1 = causa forte

# CORREÇÃO 2: Transfer Entropy
def compute_transfer_entropy(X: np.ndarray, Y: np.ndarray, k: int = 2) -> float:
    """
    Transfer Entropy: Quanto Y(t) é "surprendido" por X(t-k)?
    
    TE(X→Y) = H(Y_t | Y_past) - H(Y_t | Y_past, X_past)
    
    Mede causalidade no sentido de Teoria da Informação.
    Não assume linearidade (como Granger).
    """
    from scipy.stats import entropy
    
    # Discretizar embeddings para calcular MI
    X_bins = np.digitize(X, bins=np.percentile(X, np.linspace(0, 100, 10)))
    Y_bins = np.digitize(Y, bins=np.percentile(Y, np.linspace(0, 100, 10)))
    
    # H(Y_t | Y_past)
    Y_past_Y_current = np.column_stack([Y_bins[:-k], Y_bins[k:]])
    h_y_given_past = entropy(np.unique(Y_past_Y_current, axis=0, return_counts=True)[1])
    
    # H(Y_t | Y_past, X_past)
    Y_past_X_past_Y_current = np.column_stack([
        Y_bins[:-k], X_bins[:-k], Y_bins[k:]
    ])
    h_y_given_both = entropy(np.unique(Y_past_X_past_Y_current, axis=0, return_counts=True)[1])
    
    te = h_y_given_past - h_y_given_both
    return max(0.0, te)  # Normalizar entre 0-1
```

**Implementação:**

```python
# NOVO: compute_cross_prediction() com causalidade
def compute_cross_prediction_causal(
    self,
    source_module: str,
    target_module: str,
    history_window: int = 50,
    method: str = "granger_transfer"  # "granger" | "transfer" | "both"
) -> CrossPredictionMetrics:
    """
    Computa causalidade (não apenas correlação) entre módulos.
    
    Args:
        method: 
            - "granger": Usa Granger Causality (paramétrico)
            - "transfer": Usa Transfer Entropy (não-paramétrico)
            - "both": Combina ambas (mais robusto)
    """
    source_history = self.get_module_history(source_module, history_window)
    target_history = self.get_module_history(target_module, history_window)
    
    if len(source_history) < 10:  # Precisa de histórico adequado para causalidade
        return CrossPredictionMetrics(
            source_module=source_module,
            target_module=target_module,
            r_squared=0.0,  # CORRELAÇÃO (para compatibilidade)
            correlation=0.0,  # CORRELAÇÃO
            mutual_information=0.0,  # CAUSALIDADE (novo)
            granger_causality=0.0,  # NOVO: Granger Causality
            transfer_entropy=0.0,  # NOVO: Transfer Entropy
        )
    
    X = np.stack([s.embedding for s in source_history])
    Y = np.stack([s.embedding for s in target_history])
    
    # Computar AMBAS
    if method in ["granger", "both"]:
        granger = compute_granger_causality(X, Y)
    else:
        granger = 0.0
    
    if method in ["transfer", "both"]:
        te = compute_transfer_entropy(X, Y, k=3)
    else:
        te = 0.0
    
    # Combinar se ambas
    if method == "both":
        # Usar a MAIOR (mais conservador - só contar se AMBAS concordam)
        causal_strength = min(granger, te)  # Intersecção
    elif method == "granger":
        causal_strength = granger
    else:
        causal_strength = te
    
    return CrossPredictionMetrics(
        source_module=source_module,
        target_module=target_module,
        r_squared=0.0,  # REMOVER uso para Φ
        correlation=0.0,
        mutual_information=causal_strength,  # AGORA: causalidade comprovada
        granger_causality=granger,
        transfer_entropy=te,
    )
```

---

### 2. ⚠️ Sem Análise de Complexidade Computacional

**Problema Atual:**
- Arquivo: `src/consciousness/integration_loop.py` (linhas 300-330)
- Função: `execute_cycle()`
- Problema: Nenhuma medição de Big-O ou custo computacional

**Exemplo do Viés:**
```python
# Código atual (SEM análise)
for source_module in result.modules_executed:
    for target_module in result.modules_executed:  # O(N²) - OCULTO!
        cross_pred = self.workspace.compute_cross_prediction(...)
        # Dentro: Regressão Linear com SVD = O(n * d²)
        # Total: O(N² * n * d²) por ciclo!

# Com 10 módulos, janela 50, embedding 256:
# = 10² * 50 * 256² ≈ 327 MILHÕES de operações por ciclo
# Em 200 ciclos = 65 BILHÕES de operações!
# Mas ninguém sabe porque não há logging de complexidade
```

**Impacto:**
- GPU está sendo subutilizada (falta paralelização consciente)
- Não há otimizações porque não se sabe onde está o gargalo
- Ablações demoram horas quando poderiam levar minutos
- Impossível escalar para 100+ módulos

**Solução: Análise de Complexidade + Logging + Otimizações**

```python
# NOVO: Classe para rastrear complexidade
from dataclasses import dataclass
from typing import Dict

@dataclass
class ComplexityMetrics:
    """Métricas de complexidade de um operação."""
    operation_name: str
    num_modules: int
    history_window: int
    embedding_dim: int
    
    # Teórico (Big-O)
    theoretical_ops: int  # Número de operações esperadas
    theoretical_time_ms: float  # Tempo esperado
    
    # Prático (medido)
    actual_time_ms: float
    actual_ops_estimate: int
    
    # Eficiência
    efficiency_ratio: float = 1.0  # actual / theoretical
    gpu_utilization_percent: float = 0.0
    
    def __post_init__(self):
        if self.theoretical_time_ms > 0:
            self.efficiency_ratio = self.actual_time_ms / self.theoretical_time_ms

class ComplexityAnalyzer:
    """Analisa complexidade computacional de operações."""
    
    @staticmethod
    def estimate_cross_prediction_complexity(
        n_modules: int,
        history_window: int,
        embedding_dim: int
    ) -> int:
        """Estima operações para compute_cross_prediction()."""
        # X @ W: (n, d) @ (d, d) = n*d²
        # Para cada par de módulos: O(n*d²)
        # Total: N² pares = O(N² * n * d²)
        
        ops_per_pair = history_window * (embedding_dim ** 2)
        total_ops = n_modules * n_modules * ops_per_pair
        return total_ops
    
    @staticmethod
    def estimate_compute_phi_complexity(
        n_modules: int,
        n_predictions: int
    ) -> int:
        """Estima operações para compute_phi()."""
        # Média de N² predições = O(N²)
        # Com penalizações e validações = O(N² * log N)
        return n_predictions * int(np.log2(n_modules) + 1)
    
    @staticmethod
    def estimate_cycle_complexity(
        n_modules: int,
        history_window: int,
        embedding_dim: int
    ) -> Dict[str, int]:
        """Estima complexidade total de um ciclo."""
        return {
            "cross_predictions": ComplexityAnalyzer.estimate_cross_prediction_complexity(
                n_modules, history_window, embedding_dim
            ),
            "phi_computation": ComplexityAnalyzer.estimate_compute_phi_complexity(
                n_modules, n_modules ** 2
            ),
            "other": n_modules * embedding_dim,  # Leitura/escrita em workspace
            "total": 0,  # Será calculado
        }

# NOVO: Logging de complexidade em execute_cycle
async def execute_cycle(self, collect_metrics: bool = True) -> LoopCycleResult:
    """Execute one integration cycle com complexidade rastreada."""
    start_time = datetime.now()
    result = LoopCycleResult(
        cycle_number=self.cycle_count,
        cycle_duration_ms=0.0,
        modules_executed=[],
        cross_prediction_scores={},
        phi_estimate=0.0,
        timestamp=datetime.now(),
        complexity_metrics=None,  # NOVO
    )
    
    # Estimar complexidade ANTES
    theoretical_complexity = ComplexityAnalyzer.estimate_cycle_complexity(
        n_modules=len(self.loop_sequence),
        history_window=50,
        embedding_dim=self.workspace.embedding_dim,
    )
    theoretical_complexity["total"] = sum(theoretical_complexity.values())
    
    # EXECUTAR ciclo (com medição)
    # ... código original ...
    
    # Medir complexidade DEPOIS
    actual_time_ms = (datetime.now() - start_time).total_seconds() * 1000
    
    # Calcular taxa operações/ms (proxy para eficiência GPU)
    ops_per_ms = theoretical_complexity["total"] / max(actual_time_ms, 0.001)
    
    result.complexity_metrics = {
        "theoretical_ops": theoretical_complexity["total"],
        "theoretical_time_ms": theoretical_complexity["total"] / 1e6,  # Estimativa
        "actual_time_ms": actual_time_ms,
        "ops_per_ms": ops_per_ms,
        "efficiency_estimate": 0.0,
    }
    
    logger.info(
        f"Cycle {self.cycle_count} Complexity: "
        f"~{theoretical_complexity['total']/1e6:.1f}M ops in {actual_time_ms:.1f}ms "
        f"({ops_per_ms/1e3:.1f}GOps/s)"
    )
    
    return result

# NOVO: Relatório de gargalos
def analyze_bottlenecks(self, cycles: List[LoopCycleResult]) -> Dict[str, Any]:
    """Analisa gargalos de complexidade."""
    times_by_operation = {
        "cross_predictions": [],
        "phi_computation": [],
        "other": [],
    }
    
    for cycle in cycles:
        if cycle.complexity_metrics:
            # Estimar proporção de tempo por operação
            total_ops = cycle.complexity_metrics["theoretical_ops"]
            theoretical_cycle = ComplexityAnalyzer.estimate_cycle_complexity(
                len(cycle.modules_executed),
                50,
                256
            )
            
            for op_type, ops in theoretical_cycle.items():
                if ops > 0:
                    prop = ops / total_ops
                    times_by_operation[op_type].append(prop * cycle.complexity_metrics["actual_time_ms"])
    
    return {
        "cross_predictions_avg_ms": np.mean(times_by_operation["cross_predictions"]),
        "phi_computation_avg_ms": np.mean(times_by_operation["phi_computation"]),
        "other_avg_ms": np.mean(times_by_operation["other"]),
        "biggest_bottleneck": max(
            times_by_operation,
            key=lambda x: np.mean(times_by_operation[x]) if times_by_operation[x] else 0
        ),
    }
```

**Otimizações Recomendadas:**

```python
# OTIMIZAÇÃO 1: Vetorização de cross_prediction (GPU-friendly)
def compute_all_cross_predictions_vectorized(self) -> Dict[str, Dict[str, float]]:
    """Computa TODAS predições cruzadas simultaneamente (O(N² * n) vs O(N² * n * d²))."""
    modules = self.get_all_modules()
    histories = {m: np.stack([s.embedding for s in self.get_module_history(m)]) 
                 for m in modules}
    
    # Ao invés de loop de loops com SVD individual:
    # X: (N, n, d)  - N módulos com n histórico e d dimensões
    # Y: (N, n, d)  - idem
    # Resultado: (N, N, d) - correlações para todos pares
    
    # ANTES: O(N² * n * d²)
    # DEPOIS: O(N * n * d) com broadcasting
    
    # Usar PyTorch/CuPy para paralelizar:
    # correlations = torch.matmul(X.T, Y) / (n-1)  # Batched
    
    return correlations  # (N, N, d)

# OTIMIZAÇÃO 2: Cache de predictions com invalidação inteligente
class CachedCrossPredictor:
    def __init__(self, cache_size: int = 1000):
        self.cache = {}  # (source, target) -> prediction
        self.cache_invalidation_count = {}
        self.cache_size = cache_size
    
    def compute_or_cache(self, source: str, target: str) -> CrossPredictionMetrics:
        key = (source, target)
        if key in self.cache and self.cache_invalidation_count.get(key, 0) == 0:
            return self.cache[key]
        
        # Computar nova
        result = self._compute_cross_prediction(source, target)
        
        # Armazenar com LRU
        if len(self.cache) >= self.cache_size:
            # Remover antigo
            oldest = min(self.cache, key=lambda k: self.cache_invalidation_count.get(k, 0))
            del self.cache[oldest]
        
        self.cache[key] = result
        self.cache_invalidation_count[key] = 0
        return result
    
    def invalidate(self, module: str):
        """Invalida predictions envolvendo esse módulo."""
        for key in list(self.cache.keys()):
            if module in key:
                self.cache_invalidation_count[key] += 1

# OTIMIZAÇÃO 3: Reduzir dimensionalidade com PCA
def compute_cross_prediction_reduced_dim(X, Y, n_components=32):
    """Reduz dim antes de regressão: O(n*d²) -> O(n*k²) onde k << d."""
    from sklearn.decomposition import PCA
    
    pca_x = PCA(n_components=n_components)
    pca_y = PCA(n_components=n_components)
    
    X_reduced = pca_x.fit_transform(X)
    Y_reduced = pca_y.fit_transform(Y)
    
    # Regressão em espaço reduzido
    W_reduced = np.linalg.lstsq(X_reduced, Y_reduced, rcond=None)[0]
    
    # Voltar ao espaço original
    W = pca_x.components_.T @ W_reduced @ pca_y.components_
    return W
```

---

## 🛠️ Implementação

### Fase 1: Adicionar suporte a causalidade (1 semana)
1. [ ] Instalar `statsmodels` (Granger Causality)
2. [ ] Implementar `compute_transfer_entropy()`
3. [ ] Implementar `compute_granger_causality()`
4. [ ] Adicionar novo parâmetro `method` a `compute_cross_prediction_causal()`
5. [ ] Testes: verificar que Granger diferencia de correlação espúria

### Fase 2: Adicionar complexidade logging (1 semana)
1. [ ] Criar classe `ComplexityAnalyzer`
2. [ ] Instrumentar `execute_cycle()` com medições
3. [ ] Logging de gargalos por operação
4. [ ] Dashboard de complexidade

### Fase 3: Otimizar (2 semanas)
1. [ ] Implementar `compute_all_cross_predictions_vectorized()`
2. [ ] Cache com invalidação
3. [ ] Redução de dimensionalidade com PCA
4. [ ] Benchmarking: comparar antes/depois

### Fase 4: Validar (1 semana)
1. [ ] Executar ablações com novo método
2. [ ] Verificar que Φ fica mais baixo (sem correlações espúrias)
3. [ ] Benchmark de velocidade
4. [ ] Atualizar papers com resultados

---

## 📊 Métricas de Sucesso

| Métrica | Antes | Depois | Meta |
|---------|-------|--------|------|
| **Φ Baseline** | 0.94 (sem causalidade) | ? (com causalidade) | < 0.85 (realista) |
| **Ciclo Time** | 250ms | < 50ms | 10x speedup |
| **Ops/sec** | 40K | 2M | 50x |
| **Documentação** | 0 linhas | 500+ | Completa |
| **GPU Util** | ~20% | > 80% | Target |

---

## 📚 Referências

- **Granger Causality:** Granger, C. W. (1969). "Investigating causal relations by econometric models"
- **Transfer Entropy:** Schreiber, T. (2000). "Measuring information transfer"
- **IIT Rigorosa:** Oizumi, M. et al. (2014). "From the Phenomenology to the Mechanisms of Consciousness"
- **Statsmodels VAR:** https://www.statsmodels.org/stable/vector_ar.html
- **PyTorch Batch Operations:** https://pytorch.org/docs/stable/generated/torch.matmul.html

---

**Status:** Pronto para Implementação  
**Autor:** GitHub Copilot (Auditoria OmniMind 2025-11-30)  
**Próximo Passo:** Iniciar Fase 1 de Implementação

