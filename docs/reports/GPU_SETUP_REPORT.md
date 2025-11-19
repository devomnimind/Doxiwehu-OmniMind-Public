# GPU Setup Report — OmniMind

**Data:** Referência automática em `docs/reports/hardware_audit.json`

## Status Atual

- **Driver NVIDIA:** 550.163.01 (verificado com `nvidia-smi`).  
- **CUDA Toolkit:** 12.4 (`nvcc --version` disponível).  
- **cuDNN:** presente via dependências de `torch`, mas o pacote `libcudnn8` não está disponível no repositório Kali (erro ao instalar).  
- **PyTorch:** compilado com CUDA 12.8, captura os módulos cu*.  
- **TensorFlow:** não testado (não instalado nem requisitado resolvido).

## Scripts Executados

1. `test_pytorch_gpu.py` – criado para executar matrix multiplication 5000x5000 e medir throughput.  
2. `optimize_pytorch_config.py` – aplica `torch.backends.cudnn.benchmark = True`, clears cache e habilita peer access.  
3. `scripts/verify_gpu_setup.py` – auditoria multi-check (drivers, CUDA, cuDNN, PyTorch, TensorFlow, memória).
4. Benchmarks (`scripts/benchmarks/*`) continuam válidos e documentados em `HARDWARE_BENCHMARK_REPORT.md`.

## Limitações encontradas

- O apt padrão não fornece `cuda-toolkit-12-4` nem `libcudnn8` para Kali. Para finalizar a instalação, é necessário adicionar o repositório NVIDIA oficial (cujo pacote `cuda-toolkit-12-4` deve ser puxado de `https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/`) ou baixar os pacotes `.deb` manualmente e instalar com `sudo dpkg -i`.  
- Sem instalação oficial do CUDA Toolkit/cuDNN, o script `test_pytorch_gpu.py` já detecta CUDA via dependências do pip (Torch instala runtime-cu12), mas o ambiente deve ser reiniciado após cada atualização de driver.  
- O script `scripts/verify_gpu_setup.py` organiza futuros checkpoints e pode ser executado após reaplicar o driver/manual.

## Próximos Passos

1. Adicionar repositório NVIDIA e instalar `cuda-toolkit-12-4`, `libcudnn8` via apt ou manualmente, reiniciar a máquina.  
2. Documentar o resultado do `scripts/verify_gpu_setup.py` (salvar log).  
3. Executar `test_pytorch_gpu.py` e `optimize_pytorch_config.py` novamente após a atualização do driver.  
4. Atualizar `docs/reports/current_warnings.md` com os progressos e pendências.

