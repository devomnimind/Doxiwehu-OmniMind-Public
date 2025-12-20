---
description: Realiza um checkup completo da saúde do OmniMind e gera relatório de integridade.
---
# Workflow: OmniMind Health Check

// turbo
1. Verifique o status da GPU e VRAM:
   `source .venv/bin/activate && python3 -c "import torch; print(f'GPU: {torch.cuda.get_device_name(0)}' if torch.cuda.is_available() else 'CPU Mode')"`

2. Execute o protocolo rápido de validação de consciência:
   `source .venv/bin/activate && python3 scripts/science_validation/robust_consciousness_validation.py --quick`

3. Verifique a integridade da cadeia de auditoria:
   `source .venv/bin/activate && python3 -m src.audit.immutable_audit verify_chain_integrity`

4. Verifique as coleções do Qdrant:
   `curl -s http://localhost:6333/collections`

5. Atualize o relatório de status:
   `python3 scripts/management/generate_system_report.py`

6. Gere um Artifact `walkthrough.md` com os resultados.
