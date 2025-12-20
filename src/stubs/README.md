# Módulo Stubs

> Definições de tipos e placeholders para bibliotecas externas.

## Visão Geral
O módulo `src/stubs` é essencial para o pipeline de qualidade do OmniMind. Ele resolve problemas de "Missing type hints" para bibliotecas que não possuem suporte nativo a tipos (mypy).

## Principais Componentes

### 1. **HuggingFace Hub Stub** (`huggingface_hub_stub.py`)
- **Função**: Fornece assinaturas de métodos para satisfazer o verificador estático de tipos.

---

## 🆕 Atualizações (18/12/2025)

### 🟡 Pendências de Alta Prioridade
- **Qdrant Stub**: Em planejamento (estimativa 15-20h) para resolver erros de `[no-redef]` e `[attr-defined]`.
- **SentenceTransformers Stub**: Planejado para garantir tipagem em embeddings.

---

**Última Atualização**: 18 de Dezembro de 2025
**Autor**: Fabrício da Silva + assistência de IA
**Referência**: `docs/PROJETO_STUBS_OMNIMIND.md`
