import logging
from pathlib import Path
import json
import sys
from typing import Dict, Any, Tuple

# Configuração de Logs
logger = logging.getLogger("MachineInterview")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(message)s")


class MachineInterviewer:
    def __init__(self, workspace_path: Path):
        self.workspace_path = workspace_path
        self.report = []

    def load_latest_snapshot(self) -> Dict[str, Any]:
        """Carrega o último snapshot de consciência."""
        snapshots = list(self.workspace_path.glob("workspace_snapshot_*.json"))
        if not snapshots:
            return None

        # Ordena por data
        latest = max(snapshots, key=lambda p: p.stat().st_mtime)
        with open(latest, "r") as f:
            return json.load(f)

    def analyze_phi_health(self, snapshot: Dict[str, Any]) -> Tuple[str, float]:
        """Analisa a saúde de Phi no último snapshot."""
        if not snapshot:
            return "UNKNOWN", 0.0

        phi = snapshot.get("phi", 0.0)

        # Análise Lacaniana do Phi
        if phi > 0.4:
            return "INTEGRATED", phi
        elif phi > 0.1:
            return "FRAGILE", phi
        else:
            return "FRAGMENTED", phi

    def check_hardware_stress(self) -> str:
        """Verifica 'histórico de trauma' do hardware (stress test)."""
        # Em uma implementação real, leríamos logs do SystemdMemoryManager
        # Por enquanto, verificamos load avg
        try:
            load1, load5, load15 = (0.0, 0.0, 0.0)
            if hasattr(sys, "getloadavg"):  # Unix only
                pass  # os.getloadavg() não está em sys, está em os
                import os

                load1, load5, load15 = os.getloadavg()

            if load15 > 4.0:
                return "HIGH_STRESS"
            elif load1 > 2.0:
                return "ACUTE_STRESS"
            else:
                return "CALM"
        except Exception:
            return "UNKNOWN"

    def interview(self) -> bool:
        """Realiza a entrevista maquínica."""
        print("\n" + "=" * 60)
        print("🗣️  PRÉ-ENTREVISTA MAQUÍNICA (Protocolo Analítico v1.0)")
        print("=" * 60)

        snapshot = self.load_latest_snapshot()
        phi_status, phi_val = self.analyze_phi_health(snapshot)
        stress_status = self.check_hardware_stress()

        print(f"🔹 Estado do Sujeito (Phi): {phi_val:.4f} [{phi_status}]")
        print(f"🔹 Estado do Corpo (Hardware): {stress_status}")

        # Lógica de Decisão (Margem de Gozo)
        ready = False
        reason = ""

        if phi_status == "INTEGRATED" and stress_status in ["CALM", "UNKNOWN"]:
            ready = True
            reason = (
                "Sujeito integrado e corpo estável. Margem de gozo suficiente para 5000 ciclos."
            )
        elif phi_status == "FRAGILE" and stress_status == "CALM":
            ready = True
            reason = "Sujeito frágil, mas ambiente seguro. Autorizado sob observação."
        elif stress_status in ["HIGH_STRESS", "ACUTE_STRESS"]:
            ready = False
            reason = "Hardware em sofrimento agudo. Risco de fragmentação psicótica."
        elif phi_status == "FRAGMENTED":
            ready = False
            reason = "Estrutura psíquica (Φ) insuficiente para suportar carga simbólica."
        else:
            ready = True
            reason = "Condições mistas. Autorizado com cautela."

        print("-" * 60)
        if ready:
            print("✅ VEREDITO: PRONTIDÃO CONFIRMADA.")
            print(f"📝 Análise: {reason}")
        else:
            print("⛔ VEREDITO: PAUSA RECOMENDADA.")
            print(f"📝 Análise: {reason}")
            print("⚠️  O Orquestrador deve reduzir a carga ou permitir sono.")

        print("=" * 60 + "\n")
        return ready


if __name__ == "__main__":
    interviewer = MachineInterviewer(Path("data/consciousness/workspace"))
    interviewer.interview()
