import subprocess
import sys
import time
import signal
import os
from pathlib import Path

# Define project_root at the top level
# Script is in scripts/science_validation/, so project root is 3 levels up
project_root = Path(__file__).resolve().parent.parent.parent


def run_training():
    # Default arguments
    args = ["--cycles", "500", "--interval", "0.1"]

    # Override with CLI args if provided
    if len(sys.argv) > 1:
        args = sys.argv[1:]

    cmd = [
        sys.executable,
        str(project_root / "scripts" / "science_validation" / "run_extended_training.py"),
    ] + args

    # Environment variables for debug
    env = os.environ.copy()
    env["PYTHONFAULTHANDLER"] = "1"  # Dump trace on segfault
    env["CUDA_LAUNCH_BLOCKING"] = "1"

    print(f"🚀 Iniciando Wrapper de Treinamento Robust (PID {os.getpid()})")

    start_time = time.time()

    # Run subprocess
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=env,
            universal_newlines=True,
            bufsize=1,
        )

        # Stream output
        with open("logs/extended_training_wrapper.log", "w") as f:
            for line in process.stdout:
                print(line, end="")  # Print to stdout for feedback
                f.write(line)
                f.flush()

        # Wait for finish
        return_code = process.wait()

        end_time = time.time()
        duration = end_time - start_time

        print(f"\n🛑 Processo terminou. Return Code: {return_code}")
        print(f"⏱️ Duração: {duration:.2f}s")

        if return_code == -11:  # SEGFAULT
            print("🚨 DETECTADO SIGSEGV (Segmentation Fault)!")
            print("Isso geralmente indica memória corrompida em C/C++ (PyTorch/Qiskit/Drivers).")
        elif return_code == -9:  # SIGKILL
            print("🚨 DETECTADO SIGKILL (OOM Killer ou Admin via kill -9)!")
        elif return_code == -6:  # SIGABRT
            print("🚨 DETECTADO SIGABRT (Abort/Assert FAILED)!")

    except KeyboardInterrupt:
        print("\n🛑 Interrompido pelo usuário.")
        process.send_signal(signal.SIGINT)
        process.wait()


if __name__ == "__main__":
    run_training()
