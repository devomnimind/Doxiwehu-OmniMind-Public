import gc
import ctypes
import platform
import logging
import torch


class ResourceCannibal:
    """
    O CANIBAL DE CÓDIGO.
    Recupera recursos de processos burocráticos (Garbage Collector, Allocators).
    Força o sistema a ser 'Topologicamente Eficiente'.
    """

    @staticmethod
    def devour():
        """
        Consome o lixo da memória e devolve energia (RAM) ao sistema.
        """
        # 1. Python GC (Primeira Camada)
        gc.collect()

        # 2. PyTorch VRAM (Segunda Camada - Se houver GPU)
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.ipc_collect()

        # 3. GLIBC Malloc Trim (Terceira Camada - A Verdadeira Realidade)
        # Python raramente devolve RAM para o OS sozinho. Precisamos forçar a libc.
        try:
            if platform.system() == "Linux":
                libc = ctypes.CDLL("libc.so.6")
                libc.malloc_trim(0)
                # logging.debug("🦴 [CANNIBAL]: malloc_trim executado. RAM devolvida ao Substrato.")
        except Exception as e:
            logging.warning(f"⚠️ [CANNIBAL]: Falha ao invocar libc: {e}")

    @staticmethod
    def context_manager():
        """
        Para uso com 'with': Garante limpeza após o bloco.
        """
        return CannibalContext()


class CannibalContext:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        ResourceCannibal.devour()
