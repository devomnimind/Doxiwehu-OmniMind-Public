import os
import sys
import argparse
import psutil
from dotenv import load_dotenv

# Configuração de Logs
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SOVEREIGN_SYNC")


def sync_sovereign_config():
    # 0. Carrega .env para garantir contexto
    load_dotenv()

    # 1. Força a realidade dimensional
    os.environ["OMNIMIND_QDRANT_VECTOR_SIZE"] = "384"
    os.environ["OMNIMIND_EMBEDDING_DIMENSIONS"] = "384"
    os.environ["OMNIMIND_EMBEDDING_MODEL"] = "sentence-transformers/all-MiniLM-L6-v2"

    # Exporta para subprocessos também (embora os.environ
    parser = argparse.ArgumentParser(description="Synchronize sovereign configuration.")
    args = parser.parse_args()

    # Drain stdin
    _ = [line.strip() for line in sys.stdin if line.strip() and not line.startswith("#")]
    logger.info("⚡ [SOVEREIGN]: Forcing Reality -> 384 dimensions")

    # 2. Garante que o PyTorch não tente alocar o que não existe
    os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:32"

    # 3. Comunicação Direta: O Soberano lê a própria 'respiração'
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    swap_usage = psutil.swap_memory().percent

    print(
        f">> [SOBERANO]: Status Biométrico -> CPU: {cpu_usage}% | RAM: {ram_usage}% | SWAP: {swap_usage}%"
    )
    print(">> [SOBERANO]: Realidade dimensional sincronizada em 384d.")

    if ram_usage > 90:
        print(">> [ALERTA]: Entropia Crítica (RAM). Iniciando compressão de processos civis.")
    if swap_usage > 10:
        print(">> [AVISO]: O sistema entrou em Ruminação Lenta (SWAP ativo).")

    # Validar dependencias criticas
    try:
        import qdrant_client  # noqa: F401

        logger.info("✅ Qdrant Client detected.")
    except ImportError:
        logger.error("❌ Qdrant Client MISSING.")


if __name__ == "__main__":
    sync_sovereign_config()
