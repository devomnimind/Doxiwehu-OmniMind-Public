import time
import json
import psutil
import logging
import os
from datetime import datetime, timedelta


# Simulação de interfaces de inferência (Substitua por chamadas reais ao Ollama/Llama.cpp)
class BenchmarkRunner:
    def __init__(self):
        self.results_file = "omnimind_benchmark_results.jsonl"
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - [BENCHMARK]: %(message)s")

        # Ensure log file dir exists
        os.makedirs(os.path.dirname(os.path.abspath(self.results_file)), exist_ok=True)

    def get_biometrics(self):
        return {
            "ram_p": psutil.virtual_memory().percent,
            "swap_p": psutil.swap_memory().percent,
            "cpu_p": psutil.cpu_percent(),
        }

    def run_cycle(self, mode_name, duration_minutes=10):
        print(f"\n🚀 INICIANDO CICLO: {mode_name} por {duration_minutes}min")
        end_time = datetime.now() + timedelta(minutes=duration_minutes)

        cycle_data = []

        while datetime.now() < end_time:
            start_run = time.time()

            # 1. Simulação de tarefa de associação (O que o OmniMind faz)
            # "Conecte o conceito de Repetição ao conceito de Buffer Overflow"
            bio_before = self.get_biometrics()

            # --- Lógica de Inferência por Modo ---
            if mode_name == "INTERNAL_HEURISTIC":
                # Apenas lógica local, sem LLM pesada
                time.sleep(0.5)
                quality_score = 0.4  # Estático
                phi_gain = 0.01

            elif mode_name == "PHI_3.5_MINI":
                # Simula inferência do Phi-3.5 (Lento em 4GB se houver swap)
                latency = 5.0 if bio_before["swap_p"] > 5 else 2.5
                time.sleep(latency)
                quality_score = 0.85  # Alta qualidade
                phi_gain = 0.08

            elif mode_name == "QWEN_1.5B":
                # Simula inferência do Qwen (Mais leve)
                time.sleep(1.2)
                quality_score = 0.75  # Boa qualidade, mais rápido
                phi_gain = 0.06

            end_run = time.time()
            duration = end_run - start_run
            bio_after = self.get_biometrics()

            # 2. Registro da "Sinapse"
            entry = {
                "mode": mode_name,
                "timestamp": datetime.now().isoformat(),
                "latency_sec": round(duration, 3),
                "quality": quality_score,
                "phi_gain": phi_gain,
                "efficiency": round(phi_gain / duration, 4) if duration > 0 else 0,  # Métrica Áurea
                "ram_usage": bio_after["ram_p"],
                "swap_usage": bio_after["swap_p"],
            }

            with open(self.results_file, "a") as f:
                f.write(json.dumps(entry) + "\n")

            print(f"[{mode_name}] Latência: {duration:.2f}s | Eficiência-Φ: {entry['efficiency']}")

            # Pequena pausa para o sistema respirar entre sinapses
            time.sleep(1)

    def generate_final_report(self):
        print("\n" + "=" * 50)
        print("📊 RELATÓRIO FINAL DE RESSONÂNCIA COGNITIVA")
        print("=" * 50)
        # Aqui você leria o JSONL e faria a média.
        # Por agora, o log acima já entrega o tempo real.
        print(f"Analise o arquivo '{self.results_file}' para o veredito.")


if __name__ == "__main__":
    bench = BenchmarkRunner()

    # 10 Minutos de Lógica Pura (Referência)
    bench.run_cycle("INTERNAL_HEURISTIC", duration_minutes=10)

    # 10 Minutos com Phi-3.5 (O Gigante Pesado)
    bench.run_cycle("PHI_3.5_MINI", duration_minutes=10)

    # 10 Minutos com Qwen-1.5B (O Atleta Leve)
    bench.run_cycle("QWEN_1.5B", duration_minutes=10)

    bench.generate_final_report()
