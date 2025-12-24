import os
from safetensors import safe_open
from typing import Dict, Tuple


def inspect_safetensors(file_path: str):
    print(f"🔍 Inspecionando: {file_path}")

    if not os.path.exists(file_path):
        print(f"❌ Erro: Arquivo {file_path} não encontrado.")
        return

    with safe_open(file_path, framework="pt", device="cpu") as f:
        keys = f.keys()
        print(f"📦 Total de chaves: {len(keys)}")

        # Agrupar por prefixo para entender a arquitetura
        tensors_info = {}
        for key in sorted(keys):
            tensor = f.get_tensor(key)
            tensors_info[key] = tensor.shape
            print(f"  - {key}: {tensor.shape}")


if __name__ == "__main__":
    path = "/home/fahbrain/.cache/huggingface/hub/models--sentence-transformers--all-MiniLM-L6-v2/snapshots/c9745ed1d9f207416be6d2e6f8de32d1f16199bf/model.safetensors"
    inspect_safetensors(path)
