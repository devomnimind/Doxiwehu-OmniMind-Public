# Plano Estratégico de Métricas: Local vs IBM Quantum

## 1. Status Atual (Validação Inicial)
Realizamos um estudo comparativo inicial entre o backend Local (Neal/Simulated Annealing) e o backend IBM (Qiskit Aer Simulator).

### Resultados do Estudo Comparativo
| Métrica | Neal (Local) | IBM (Qiskit Sim) | Análise |
| :--- | :--- | :--- | :--- |
| **Latência Média** | ~0.0326s | ~0.0002s | O simulador IBM está usando "Exact Solver" para o sistema de 3 qubits, sendo instantâneo. |
| **Qualidade do Compromisso** | 0.55 | 0.55 | Ambos convergem para a mesma solução ótima (Ground State). |
| **Consistência** | Alta | Perfeita | O método exato do IBM garante a solução ótima sempre neste modelo pequeno. |

**Conclusão Preliminar:** A lógica de resolução de conflitos é matematicamente consistente entre os backends. O sistema é agnóstico ao hardware.

---

## 2. Plano Estratégico de Expansão

Para atingir a "Validade Científica" robusta exigida pelo roadmap, propomos o seguinte plano:

### Fase 1: Complexidade (Curto Prazo)
O modelo atual de 3 agentes (Id, Ego, Superego) é trivial ($2^3 = 8$ estados).
*   **Ação:** Expandir o modelo para incluir "Complexos de Memória" no grafo de conflito.
*   **Meta:** Aumentar para 10-20 qubits (variáveis).
*   **Impacto:** O "Exact Solver" ficará lento, justificando o uso de heurísticas (Neal) e algoritmos quânticos reais (QAOA).

### Fase 2: Implementação de QAOA (Médio Prazo)
Atualmente, o backend IBM simula a *resposta* ideal. Devemos simular o *processo* quântico.
*   **Ação:** Substituir o loop de força bruta em `_solve_gate_based` por um circuito **QAOA (Quantum Approximate Optimization Algorithm)** usando `qiskit-algorithms`.
*   **Benefício:** Demonstrar o uso de portas quânticas reais (Hadamard, CNOT, RZ) para encontrar o estado de mínima energia.

### Fase 3: Execução em Hardware Real (Longo Prazo)
Com o token IBM configurado, podemos submeter jobs reais.
*   **Ação:** Configurar `QiskitRuntimeService` para enviar jobs em lote para computadores quânticos reais da IBM.
*   **Custo:** Execução lenta (filas de espera), mas gera dados com "Ruído Quântico Real".
*   **Valor Científico:** Analisar como o ruído quântico afeta a "psicopatologia" do sistema (erros de decisão = atos falhos?).

## 3. Próximos Passos Imediatos
1.  Manter o script `comparative_metrics.py` como benchmark padrão.
2.  Refinar o `quantum_backend.py` para suportar QAOA real (simulado) em vez de força bruta.
3.  Gerar gráficos comparativos para o paper.
