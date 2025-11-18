# Hugging Face Resource Validation — 18 Nov 2025

## 1. Autenticação & Permissões
- `hf auth whoami` → usuário ativo `fabricioslv`, conta PRO com token rotulado **OmniDev** (`role: write`).
- Acesso Git confirmado pela API (`whoami.auth.accessToken.role = write`), portanto push/pull privados habilitados.
- Nenhum workspace dedicado (novo recurso “Workspaces”) aparece na API pública; somente Spaces estão associados à conta.

## 2. Spaces / Workspaces Validados
| Space | Priv / Status | Hardware solicitado | GPU? | Conteúdo relevante | Observações |
| --- | --- | --- | --- | --- | --- |
| `fabricioslv/dev_brain` | Privado · `SLEEPING` | `cpu-basic` | ❌ | `app.py`, `requirements.txt` | UI simples, sem scripts de fine-tuning. |
| `fabricioslv/devbrain-training` | Privado · `SLEEPING` | `cpu-basic` | ❌ | `train_hf_zerogpu.py`, `training_dataset.jsonl` | Estrutura mais próxima do fine-tuning, porém limitado a CPU “Zero GPU”. |
| `fabricioslv/devbrain-docs` | Público · `SLEEPING` | `cpu-basic` | ❌ | Documentação/app estático | Sem utilidade direta para treino. |
| `fabricioslv/devbrain-inference` | Público · `RUNTIME_ERROR` | `cpu-basic` | ❌ | `app.py`, `requirements.txt` | Stopped com erro; não preparado para treino. |

**Conclusões:**
- Nenhum Space atual solicita GPU (apenas `cpu-basic`).
- `devbrain-training` já contém script e dataset exemplificativo, portanto é o melhor candidato para upgrade de hardware (ex.: `gpu-zero`, `t4-medium`, `a10g-small`).
- Sem “Workspaces” com GPUs provisionados; qualquer execução remota exigirá alterar o hardware de um Space existente ou criar outro com GPU.

## 3. Datasets Disponíveis
| Dataset | Privacidade | Formato / Arquivos | Indicadores | Compatibilidade |
| --- | --- | --- | --- | --- |
| `fabricioslv/devbrain-training-data` | Privado | `data/train-00000-of-00001.parquet`, README | Tags: `size_categories:n<1K`, `format:parquet` | Útil para smoke tests pequenos; insuficiente para Fase 10. |
| `fabricioslv/devbrain-complete-consolidated` | Privado | `data.jsonl` (~1,489 amostras, médio porte) | Tags: `size_categories:1K<n<10K`, `format:json` | **Melhor candidato** ao fine-tuning atual (equivale ao dataset usado localmente). |
| `fabricioslv/academic-writer-training` | Privado | `data.jsonl`, `devbrain_consolidated.jsonl` | Conteúdo temático diferente | Reaproveitável apenas se precisarmos de estilo acadêmico. |

**Observações adicionais:**
- Nenhum dataset público/privado contém arquivo chamado `personal_corpus.jsonl`; se for requisito explícito, será necessário upload do arquivo local (`DEVBRAIN_V23/kernel/finetuning/datasets/personal_corpus.jsonl`).
- O dataset `devbrain-complete-consolidated` já foi espelhado localmente em `hf_datasets/devbrain_complete/data.jsonl` (1,489 exemplos, ~1.18k caracteres médios). Pode ser sincronizado novamente para garantir paridade.

## 4. Decisão & Planejamento
1. **Reutilizar `fabricioslv/devbrain-training`**
   - Motivo: já contém scripts (`train_hf_zerogpu.py`) e assets. Necessário apenas trocar o hardware para GPU e atualizar dependências.
2. **Dataset**
   - Preferir `devbrain-complete-consolidated`. Se o cliente exigir `personal_corpus.jsonl`, subir esse arquivo para o mesmo dataset ou criar `fabricioslv/personal-corpus-phase10`.
3. **Ações faltantes antes do treino**
   - Solicitar GPU (`gpu-zero`, `t4-medium` ou `a10g-small`) para o Space escolhido.
   - Sincronizar código atualizado (`finetune_mistral.py`, novas configs) com o Space.
   - Confirmar armazenamento suficiente (>= 15 GB) para checkpoints no Space.

## 5. Comandos Propostos (executar apenas após aprovação)
```bash
# 1. Solicitar hardware GPU para o Space de treino
huggingface-cli space hardware fabricioslv/devbrain-training --hardware a10g-small

# 2. Atualizar conteúdo do Space com o pipeline local
cd /home/fahbrain/projects/omnimind/DEVBRAIN_V23/kernel/finetuning
huggingface-cli upload . space fabricioslv/devbrain-training --include "finetune_mistral.py" "requirements.txt"

# 3. (Opcional) Publicar dataset personal_corpus.jsonl
huggingface-cli upload ./datasets/personal_corpus.jsonl \
  datasets/fabricioslv/devbrain-complete-consolidated/personal_corpus_phase10.jsonl
```
> Observação: confirme o comando `huggingface-cli space hardware` disponível na versão atual da CLI; em alternativa, ajuste o hardware pela UI dos Spaces.

## 6. Aprovação Requerida
- **Treinamento remoto não será iniciado** até recebermos autorização explícita para: (a) upgrade de hardware do Space, (b) upload/sincronização de datasets, (c) execução do pipeline `finetune_mistral.py` em ambiente GPU.
- Após aprovação, forneceremos playbook detalhado (deploy do Space, monitoramento, coleta de métricas de loss/perplexity).
