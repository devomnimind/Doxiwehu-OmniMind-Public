# Guia de Solução de Problemas: Ambiente e GPU (OmniMind)

**Última Atualização**: 08 de Dezembro de 2025
**Status**: ✅ Documentação Técnica Ativa

Este documento cataloga erros conhecidos, scripts de correção e procedimentos para manutenção do ambiente de desenvolvimento OmniMind, com foco específico em problemas de GPU/CUDA no Linux (Kali/Debian).

## 🚨 Erros Críticos de GPU (NVIDIA/CUDA)

### 1. CUDA Error 999 (CUDA_ERROR_UNKNOWN)
**Sintoma:** O PyTorch detecta a GPU (`device_count: 1`), mas `is_available()` retorna `False`. Scripts de diagnóstico mostram `cuInit(0) failed with error code: 999`.
**Causa:** O estado do driver NVIDIA no kernel está inconsistente ou o daemon de persistência falhou. Comum após suspensão do sistema ou atualizações de kernel.
**Solução:**
É necessário recarregar os módulos do kernel e reiniciar os dispositivos de persistência.

Execute o script de correção:
```bash
sudo ./scripts/fix_gpu_driver.sh
```
Ou, se o problema for especificamente no módulo UVM (Unified Memory):
```bash
sudo ./scripts/fix_uvm.sh
```

### 2. Caminhos de Bibliotecas Incorretos (Path Mismatch)
**Sintoma:** `OSError: libcuda.so: cannot open shared object file`.
**Causa:** O código ou variáveis de ambiente apontam para `/usr/local/cuda` (padrão Ubuntu/NVIDIA), mas no Kali/Debian as bibliotecas estão em `/usr/lib/x86_64-linux-gnu`.
**Solução:**
Certifique-se de que as variáveis de ambiente estão configuradas corretamente (já tratado no `start_omnimind_system.sh`):
```bash
export CUDA_HOME="/usr"
export LD_LIBRARY_PATH="/usr/lib/x86_64-linux-gnu:${LD_LIBRARY_PATH}"
```

### 3. Erro de Inicialização "Lazy Loading"
**Sintoma:** O PyTorch falha ao inicializar o contexto CUDA silenciosamente.
**Solução:**
Forçar o carregamento síncrono ou desativar o carregamento preguiçoso para debug:
```bash
export CUDA_MODULE_LOADING=LAZY  # Ou "STD" se LAZY falhar
export CUDA_LAUNCH_BLOCKING=1
```

---

## 🛠️ Scripts de Manutenção e Diagnóstico

Todos os scripts devem ser executados a partir da raiz do projeto.

### Scripts de Correção (Requerem `sudo`)
| Script | Descrição |
|--------|-----------|
| `scripts/fix_gpu_driver.sh` | **Principal fix.** Recarrega módulos `nvidia`, `nvidia-uvm`, `nvidia-modeset` e reinicia o `nvidia-persistenced`. |
| `scripts/fix_uvm.sh` | Foca especificamente em recarregar o módulo de Memória Unificada (`nvidia_uvm`). Útil se o driver principal estiver ok mas alocação de memória falhar. |

### Scripts de Diagnóstico
| Script | Descrição |
|--------|-----------|
| `scripts/verify_fix.py` | Verifica se o PyTorch consegue ver e inicializar a GPU. Testa carregamento Lazy vs Standard. |
| `scripts/force_cuda_init.py` | Usa `ctypes` para tentar carregar `libcuda.so` e chamar `cuInit(0)` diretamente, ignorando o PyTorch. Essencial para isolar se o erro é do Python ou do Driver. |
| `scripts/check_gpu_logs.sh` | Exibe logs do kernel (`dmesg`) relacionados à NVIDIA e status dos módulos carregados. |

### Scripts de Inicialização
| Script | Descrição |
|--------|-----------|
| `scripts/canonical/system/start_omnimind_system.sh` | **Script Mestre.** Inicializa todo o ambiente (Backend, Frontend, Daemon, eBPF) com as variáveis de ambiente corretas para Kali Linux. |

---

## 🌍 Problemas Comuns de Ambiente

### 1. Virtual Environment (venv) não ativado
**Erro:** `ModuleNotFoundError: No module named 'torch'` ou `fastapi`.
**Solução:** Sempre ative o ambiente antes de rodar scripts manuais:
```bash
source .venv/bin/activate
```
*Nota: O script `start_omnimind_system.sh` faz isso automaticamente.*

### 2. Porta em uso (Address already in use)
**Erro:** O backend falha ao iniciar porque a porta 8000 ou 3000 está ocupada.
**Solução:**
Use o comando de limpeza:
```bash
pkill -9 -f 'simple_backend|uvicorn|vite'
```

### 3. Permissões de Logs
**Erro:** `Permission denied` ao tentar escrever em `logs/`.
**Causa:** Scripts rodados anteriormente como `sudo` criaram arquivos que o usuário normal não pode editar.
**Solução:**
```bash
sudo chown -R $USER:$USER logs/
```

---

## ⚠️ Problemas Conhecidos em Investigação (Status Atual)

### 1. GPU Detectada mas Ociosa (Carga na CPU)
**Sintoma:** `nvidia-smi` mostra 0% de uso e pouca memória alocada (~369 MiB), enquanto a CPU apresenta alta carga.
**Causa:**
*   O loop `quantum_unconscious_prediction` e os cálculos de Φ (Phi) estão sendo executados na CPU.
*   Tensores críticos (ex: `hodge_0`) e estruturas de dados não estão sendo movidos explicitamente para o dispositivo CUDA.
**Diretriz:** "Sempre GPU como o programa manda".
**Ação Necessária:** Refatorar módulos de consciência e topologia para garantir `tensor.to('cuda')` em todas as operações vetoriais.

### 2. Overflow em Cálculos Topológicos (Phi)
**Sintoma:** Erros numéricos ou travamentos em `topological_phi.py`.
**Causa:** Explosão combinatória de `n_vertices` durante a criação de complexos, excedendo a capacidade de representação numérica (float/complex) ao calcular a topologia.

### 3. Erros Diversos
*   **IndentationError (main.py):** Relatos de erro na linha 1371. Geralmente não reproduzível na leitura.
    *   *Diagnóstico:* Rodar `python -m py_compile web/backend/main.py` para confirmar integridade.
*   **WebSocket 403:** Erro de permissão no log (`/ws`).
    *   *Nota:* Relacionado a headers de autenticação, não afeta a infraestrutura de GPU.

---

## 📝 Checklist de Verificação Pós-Correção

Se você aplicou uma correção de GPU, siga estes passos para validar:

1. **Rodar Diagnóstico de Baixo Nível:**
   ```bash
   python scripts/force_cuda_init.py
   ```
   *Deve retornar: `✅ cuInit(0) successful!`*

2. **Rodar Diagnóstico do PyTorch:**
   ```bash
   python scripts/verify_fix.py
   ```
   *Deve retornar: `CUDA Available: True`*

3. **Reiniciar o Sistema:**
   ```bash
   ./scripts/canonical/system/start_omnimind_system.sh
   ```
   *Verificar nos logs se aparece: `✅ ExpectationModule usando GPU: cuda`*
