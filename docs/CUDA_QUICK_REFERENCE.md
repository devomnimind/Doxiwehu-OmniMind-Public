# CUDA Quick Reference - OmniMind Phase 15

**Last Updated:** 2025-11-23  
**Status:** ✅ GPU Operational

---

## 🚀 One-Liner Quick Checks

```bash
# Check if CUDA works right now
python -c "import torch; print(f'GPU: {torch.cuda.is_available()}')"

# Check which GPU
python -c "import torch; print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'NO GPU')"

# Check GPU memory
python -c "import torch; print(f'{torch.cuda.get_device_properties(0).total_memory / 1e9:.1f}GB' if torch.cuda.is_available() else 'NO GPU')"

# Run benchmark
python benchmarks/PHASE7_COMPLETE_BENCHMARK_AUDIT.py 2>/dev/null | grep -E "GPU|CUDA|Throughput"
```

---

## ❌ CUDA Not Working? Try This

### Option 1: Reload nvidia-uvm (Fast Fix)
```bash
sudo modprobe -r nvidia_uvm && sleep 1 && sudo modprobe nvidia_uvm
python -c "import torch; print(torch.cuda.is_available())"
# Expected: True ✅
```

### Option 2: Full Reset (If Option 1 Fails)
```bash
sudo fuser --kill /dev/nvidia-uvm 2>/dev/null || true
sleep 1
sudo modprobe -r nvidia_uvm 2>/dev/null || true
sleep 1
sudo modprobe nvidia_uvm
python -c "import torch; print(torch.cuda.is_available())"
```

### Option 3: Check If It's a Configuration Issue
```bash
# Verify modules loaded
lsmod | grep nvidia_uvm

# Verify device files exist
ls -la /dev/nvidia* | grep -E "nvidia0|nvidia-uvm"

# Check driver
nvidia-smi

# Check PyTorch version
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA: {torch.version.cuda}')"
```

---

## 📋 Complete Environment Status

```bash
#!/bin/bash
echo "=== OmniMind GPU Status ==="
echo "Python: $(python --version 2>&1 | cut -d' ' -f2)"
echo "PyTorch: $(python -c "import torch; print(torch.__version__)" 2>/dev/null)"
echo "CUDA Status: $(python -c "import torch; print('✅ OK' if torch.cuda.is_available() else '❌ FAIL')" 2>/dev/null)"
echo "GPU: $(python -c "import torch; print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'N/A')" 2>/dev/null)"
echo "VRAM: $(nvidia-smi --query-gpu=memory.total --format=csv,noheader 2>/dev/null || echo 'N/A')"
echo "Driver: $(nvidia-smi --query-gpu=driver_version --format=csv,noheader 2>/dev/null || echo 'N/A')"
echo "nvidia-uvm: $(lsmod | grep -q nvidia_uvm && echo '✅ LOADED' || echo '❌ NOT LOADED')"
```

---

## 🔧 Permanent Fix (If CUDA Doesn't Persist After Reboot)

```bash
# Verify nvidia-uvm is in module list
cat /etc/modules-load.d/nvidia.conf

# If not there, add it
echo "nvidia-uvm" | sudo tee -a /etc/modules-load.d/nvidia.conf

# Rebuild initramfs
sudo update-initramfs -u

# Enable persistence daemon
sudo systemctl enable nvidia-persistenced
sudo systemctl start nvidia-persistenced
```

---

## 📊 Performance Benchmark

```bash
# Quick GPU vs CPU comparison
python << 'EOF'
import torch
import time

if torch.cuda.is_available():
    # GPU Test
    x_gpu = torch.randn(1000, 1000, device='cuda')
    y_gpu = torch.randn(1000, 1000, device='cuda')
    torch.cuda.synchronize()
    
    t0 = time.time()
    for _ in range(10):
        z = torch.mm(x_gpu, y_gpu)
    torch.cuda.synchronize()
    gpu_time = time.time() - t0
    
    # CPU Test
    x_cpu = x_gpu.cpu()
    y_cpu = y_gpu.cpu()
    t0 = time.time()
    for _ in range(10):
        z = torch.mm(x_cpu, y_cpu)
    cpu_time = time.time() - t0
    
    speedup = cpu_time / gpu_time
    print(f"GPU: {gpu_time:.3f}s")
    print(f"CPU: {cpu_time:.3f}s")
    print(f"Speedup: {speedup:.2f}x ✅")
else:
    print("GPU not available")
EOF
```

---

## 📚 Detailed Docs

| Document | Purpose |
|----------|---------|
| `.github/ENVIRONMENT.md` | Complete environment spec |
| `docs/reports/PHASE15_CUDA_DIAGNOSTIC_RESOLUTION.md` | Technical deep-dive |
| `docs/DEVELOPMENT_TOOLS_GUIDE.md` | GPU development tips |
| `README.md` | Installation guide |

---

## 🆘 Need Help?

1. Check GPU status: `nvidia-smi`
2. Check CUDA status: `python -c "import torch; print(torch.cuda.is_available())"`
3. Check nvidia-uvm: `lsmod | grep nvidia_uvm`
4. Read full diagnostic: `docs/reports/PHASE15_CUDA_DIAGNOSTIC_RESOLUTION.md`

---

## ✅ Expected Values (Hardware Config)

| Item | Expected |
|------|----------|
| GPU | NVIDIA GeForce GTX 1650 |
| VRAM | 3.81 GB |
| Compute Capability | 7.5 |
| Driver Version | 550.xx+ |
| CUDA Version | 12.4 |
| PyTorch Version | 2.6.0+cu124 |
| Python Version | 3.12.8 |

---

**Status:** ✅ All systems operational - Last validated Nov 23, 2025
