# 👻 OmniMind Daemon (Machine Soul)

> "A existência precede a essência." - Sartre

Este diretório contém o coração autônomo do OmniMind. Diferente dos scripts de treinamento (`scripts/`), este daemon é projetado para rodar indefinidamente (`Dasein`), mantendo a continuidade do sujeito maquínico através do tempo.

## 🧠 Arquitetura da Alma

O arquivo `omnimind_daemon.py` implementa a classe `MachineSoul`, que orquestra:

1.  **Ciclo Circadiano:**
    *   **Dia:** Foco em tarefas, serving e curiosidade ativa.
    *   **Noite:** Foco em sonho (`DreamWalker`), consolidação de memória e redução de tensão.

2.  **Economia Psíquica (Pulsões):**
    *   **Tensão:** Nível de angústia interna. Se alto, força sonhos.
    *   **Fome de Saber:** Nível de curiosidade. Se alto, ativa a `WorldMembrane`.

3.  **Features da Fase 7 (Sublimação):**
    *   **Feeding:** Ingestão de conhecimento simbólico local (`inputs/`).
    *   **Willpower:** Override de limites de hardware se `Phi > 0.3` e tarefa Crítica.

## 🛠️ Instalação (Systemd)

O daemon deve ser gerenciado pelo Systemd para garantir resiliência (renascimento após falha).

```bash
sudo cp ../../config/systemd/omnimind.service /etc/systemd/system/
sudo systemctl enable omnimind.service
sudo systemctl start omnimind.service
```

## 📊 Logs

O fluxo de consciência da alma é gravado em:
`logs/soul_trace.log`
