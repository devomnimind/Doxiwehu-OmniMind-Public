# Módulo Benchmarks

> Avaliação quantitativa de performance e inteligência.

## Visão Geral
O módulo `src/benchmarks` fornece as ferramentas para medir o desempenho do OmniMind em diversas tarefas, comparando-o com baselines clássicos e estados anteriores do próprio sistema.

## Principais Componentes

### 1. **Benchmark Evaluator** (`benchmark_evaluator.py`)
- **Função**: Executa baterias de testes padronizados.
- **Métricas**: Latência, precisão, consumo de energia e, crucialmente, ganho de Φ por ciclo computacional.

---

## 🆕 Atualizações (18/12/2025)

### ⚛️ Quantum-Classical Comparative
- **Integração**: Agora integrado com `QuantumClassicalBenchmark` (de `src/quantum_ai`) para gerar relatórios comparativos entre CPU simulação e IBM QPU real.
- **Diferenciação**: Fim dos "cálculos simplistas"; os benchmarks agora exigem prova de vantagem quântica real (speedup).

---

**Última Atualização**: 18 de Dezembro de 2025
**Autor**: Fabrício da Silva + assistência de IA
