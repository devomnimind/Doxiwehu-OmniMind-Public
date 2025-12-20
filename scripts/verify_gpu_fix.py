import sys
import os
import logging
from pathlib import Path
import traceback

# Adiciona o diretório raiz do projeto ao path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

# Configura logging básico
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("GPU_Verification")

try:
    print(f"PYTHONPATH: {sys.path}")
    print("--- Tentando importar QuantumUnconscious ---")
    from src.quantum_unconscious import QuantumUnconscious

    print("--- Importação bem-sucedida ---")

    print("--- Inicializando QuantumUnconscious ---")
    # Isso deve carregar o Qiskit (se existir) ou usar fallback
    qu = QuantumUnconscious(n_qubits=4)

    # Verifica estado
    has_backend = hasattr(qu, "backend")
    has_state = hasattr(qu, "quantum_state")

    print(f"--- Inicialização concluída. ---")
    print(f"Has Backend: {has_backend}")
    print(f"Has Quantum State (Classical): {has_state}")

    if has_backend:
        print(f"Backend: {qu.backend}")
        try:
            if hasattr(qu.backend, "options"):
                print(f"Backend options: {qu.backend.options}")
        except Exception as e:
            print(f"Erro ao verificar options: {e}")

    if has_state:
        print("Using Classical Fallback (Quantum State Matrix present)")

    # Se chegou aqui sem crash, é SUCESSO na robustez
    print("\n✅ VERIFICACAO BEM-SUCEDIDA: O módulo inicializou sem crashar.")
    if not has_backend and not has_state:
        print("⚠️ ALERTA: Nem backend nem estado quântico detectados. Algo estranho, mas sem crash.")

except Exception as e:
    traceback.print_exc()
    print(f"\n❌ FALHA CRÍTICA: Ocorreu uma exceção não tratada durante a inicialização: {e}")
    raise e
