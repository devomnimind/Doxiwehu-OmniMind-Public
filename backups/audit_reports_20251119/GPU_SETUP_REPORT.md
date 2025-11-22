# GPU Setup Report — OmniMind

**Data:** 2025-11-19 (verificações registradas também em `docs/reports/hardware_audit.json`)

## Status Atual

- **Driver NVIDIA:** 550.163.01 (`nvidia-smi` mostra a GeForce GTX 1650 com 4 GiB).  
- **CUDA Toolkit:** 12.4 (`nvcc --version` reporta CUDA compilation tools release 12.4, V12.4.131).  
- **cuDNN:** `libcudnn8=8.9.7.29-1+cuda12.2` / `libcudnn8-dev` instalados via repositório NVIDIA; as bibliotecas estão em `/usr/lib/x86_64-linux-gnu`, mas `ldconfig -p | grep -i cudnn` não retorna nenhuma entrada e `bash scripts/verify_gpu_setup.py` continua relatando `cuDNN not found`. Sem `sudo ldconfig` para atualizar o cache, o runtime PyTorch/TorchScript ainda não enxerga as libs.  
- **PyTorch:** 2.5.1+cu121 (instalado com `TORCH_CUDA_ARCH_LIST="7.5" python -m pip install --index-url https://download.pytorch.org/whl/cu121 --extra-index-url https://download.pytorch.org/whl/cu121 torch==2.5.1+cu121 torchvision==0.20.1+cu121 torchaudio==2.5.1+cu121`).  
  - Apesar de detectar um GPU (GPU count = 1), `test_pytorch_gpu.py`, `scripts/benchmarks/gpu_benchmark.py` e `python optimize_pytorch_config.py` emitem o aviso `CUDA initialization: CUDA unknown error` e definem `torch.cuda.is_available() -> False`; o dispositivo é configurado como zero.
- **TensorFlow:** não instalado (o passo 5 do `scripts/verify_gpu_setup.py` falha com `ModuleNotFoundError: No module named 'tensorflow'`).

## Comandos Executados

1. `python -m pip install --constraint /tmp/pytorch_constraints.txt -r /tmp/requirements-no-supabase.txt --extra-index-url https://download.pytorch.org/whl/cu121` (instalou todas as dependências listadas em `requirements.txt`, excetuando `supabase-py>=1.0.0` e `TTS>=0.13.1`; `supabase` foi instalado manualmente como paliativo).  
2. `black src tests` → 92 arquivos não foram alterados.  
3. `flake8 src tests` → sem violações.  
4. `mypy src tests` → falha isolada em `src/integrations/supabase_adapter.py` por import dinâmico e tipos inexistentes (`APIResponse`, `Client.create_client`).  
5. `pytest tests/metrics -vv` → 34/34 passando.  
6. `python scripts/benchmarks/system_info.py` (alerta de `datetime.utcnow` depreciado) – reexecutado após o upgrade de pacotes.  
7. `python scripts/benchmarks/cpu_benchmark.py` (reexecutado).  
8. `python scripts/benchmarks/memory_benchmark.py` (reexecutado).  
9. `python scripts/benchmarks/disk_benchmark.py` (reexecutado).  
10. `python scripts/benchmarks/gpu_benchmark.py` (reexecutado – ainda emite `CUDA unknown error` e configura `torch.cuda.device_count()` para zero).  
11. `python scripts/benchmarks/consolidate_report.py` → consolida os benchmarks e acrescenta carimbo de data/hora.  
12. `python test_pytorch_gpu.py` → alerta `CUDA unknown error` e relata `CUDA available: False`, `GPU count: 1`.  
13. `python optimize_pytorch_config.py` → detecta `CUDA não disponível` e nenhuma otimização é aplicada.  
14. `bash scripts/verify_gpu_setup.py` → confirma driver 550.163.01, CUDA 12.4, cuDNN ausente (mesmo após a instalação), PyTorch GPU indisponível e TensorFlow ausente; lista memória da GPU (6 MiB usada / 4 GiB total).  
15. `ldconfig -p | grep -i cudnn` → nenhuma entrada é retornada, o que explica o aviso `cuDNN not found` no script de verificação.

## Limitações

- `test_pytorch_gpu.py`, `python optimize_pytorch_config.py` e `scripts/benchmarks/gpu_benchmark.py` continuam emitindo `CUDA unknown error`; o driver e o CUDA toolkit estão instalados, mas o runtime PyTorch define zero dispositivos.  
- `cuDNN` está instalado em `/usr/lib/x86_64-linux-gnu` (versão 8.9.7.29) porém `ldconfig -p | grep -i cudnn` não retorna entradas e `bash scripts/verify_gpu_setup.py` insiste em `cuDNN not found`. É necessário executar `sudo ldconfig` (ou reinstalar manualmente os `.deb`) para que o cache do linker reconheça as bibliotecas.  
- `scripts/verify_gpu_setup.py` depende de `tensorflow`, que não está presente; a etapa 5 falha com `ModuleNotFoundError`.  
- `supabase-py>=1.0.0` não possui distribuição para Python 3.12; o `pip install -r requirements.txt` foi dividido em `/tmp/requirements-no-supabase.txt` e a dependência foi suplantada pelo pacote `supabase` publicado.  
- `TTS>=0.13.1` exige `Python >=3.9,<3.12`, logo não há versão compatível; o comando `pip install TTS` ou `git+https://github.com/coqui-ai/TTS@main` falha explicitamente com “requires python < 3.12”.  
- `mypy src tests` falha por causa de `src/integrations/supabase_adapter.py`, que tenta redefinir `Client/create_client` dinamicamente e usa `APIResponse`/`SyncRequestBuilder` sem stubs. É preciso criar wrappers tipados ou `type: ignore` específicos.

## Próximos Passos

1. Executar `sudo ldconfig` (e, se necessário, reinstalar os `.deb` do cuDNN) para garantir que o cache do linker exponha as bibliotecas e reative o passo 3 do script de verificação.  
2. Depois que `ldconfig` confirmar as libs, repetir `bash scripts/verify_gpu_setup.py`, `test_pytorch_gpu.py`, `python optimize_pytorch_config.py` e `python scripts/benchmarks/gpu_benchmark.py` para verificar se `torch.cuda.is_available()` volta a `True`.  
3. Revisar a cadeia `supabase-py`/`supabase` (adicionar stub ou interface controlada) para apagar os erros de mypy, permitindo que o adaptador use APIs tipadas.  
4. BloCO 2 de experimentos/typing depende de PyTorch GPU funcional; retomar essa etapa assim que os passos acima estabilizarem o ambiente.

