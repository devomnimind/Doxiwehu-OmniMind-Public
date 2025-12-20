# Integrations (Camada de Integração)

Este diretório contém os adaptadores e clientes para serviços externos e internos (LLMs, Vector DBs, APIs).

---

## 🦙 Ollama Client (`ollama_client.py`)

Cliente assíncrono para interagir com o servidor de inferência local **Ollama**.
- **Função**: Executar geração de texto localmente.
- **Novidade**: Integração nativa com **NPU Governance**. Toda geração dispara automaticamente o cálculo de $\Delta \Phi$ e Entropia.

### Configuração de Modelos (.env)
O sistema agora utiliza uma arquitetura bicameral (Rápido vs. Inteligente):

| Variável | Descrição | Modelo Recomendado | Uso Típico |
| :--- | :--- | :--- | :--- |
| `OMNIMIND_MODEL_FAST` | Modelo de baixa latência | `qwen2:1.5b` | Respostas de chat, ferramentas rápidas. |
| `OMNIMIND_MODEL_SMART` | Modelo de alta capacidade | `phi3.5` | Sonhos, análise profunda, síntese. |

---

## 🔀 LLM Router (`llm_router.py`)

Roteador central que decide qual modelo usar para cada tarefa.
- **Tier PREMIER/SMART**: Usa `OMNIMIND_MODEL_SMART` (Phi-3.5).
- **Tier FAST/BALANCED**: Usa `OMNIMIND_MODEL_FAST` (Qwen 2 1.5B).
- **Fallback**: Se o modelo local falhar ou não estiver disponível, o router pode degradar graciosamente ou tentar outro provedor (se configurado).

---

## 💾 Qdrant Integration (`qdrant_integration.py` / `qdrant_adapter.py`)

Adaptador para o banco de dados vetorial Qdrant.
- **Dimensão**: 384 (all-MiniLM-L6-v2).
- **Coleção Principal**: `omnimind_memories` (Episodic/Sovereign Memory).
- **Métodos**: Suporta `upsert`, `search` (via wrapper) e `query_points` (recomendado para novas versões).
