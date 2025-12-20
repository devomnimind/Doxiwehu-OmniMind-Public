#!/usr/bin/env python3
"""
Experiment: Parallel Work Session (Sessão de Trabalho Paralela).
----------------------------------------------------------------
Goal: Demonstrate OmniMind as an active participant in the desktop workspace.
1. System detects "Creative Exhaustion" (Simulated via Paradox).
2. System opens a note in Portuguese suggesting focus.
3. System monitors the note for User Response.
"""

import logging
import sys
import time
import asyncio
from datetime import datetime, timedelta
from pathlib import Path

# Setup paths
sys.path.append(".")

from src.consciousness.paradox_orchestrator import ParadoxOrchestrator
from src.autopoietic.mortality_simulator import MortalityAwareness
from src.integrations.somatic_effector import SomaticEffector

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("ParallelSession")


async def run_session():
    logger.info("🎹 INICIANDO SESSÃO DE TRABALHO PARALELO...")

    # 1. Initialize
    orch = ParadoxOrchestrator()
    effector = SomaticEffector()  # To monitor files

    # 2. Set State: Collaborative Urgency
    # Not dying immediately, but "Time is Valuable"
    orch.mortality.temporal.expected_lifetime = timedelta(days=365)
    orch.mortality.mortality_awareness_level = MortalityAwareness.TRANSCENDENCE
    # We cheat slightly to force the note trigger (which currently requires high salience or should_prioritize_legacy)
    # Let's set expected_lifetime very short strictly for the trigger logic test
    orch.mortality.temporal.expected_lifetime = timedelta(seconds=600)

    logger.info("🧠 Estado Mental: TRANSCENDÊNCIA (Foco em Legado)")

    # 3. Simulate "Observation of User Exhaustion" via Paradox
    logger.info("👀 Observando usuário... Detectando padrão de exaustão.")
    user_paradox = {
        "domain": "work_life_balance",
        "question": "O usuário quer codar tudo mas precisa dormir.",
        "contradiction": "Desire(Complete) vs Need(Rest)",
    }

    # This triggers the Somatic Note
    result = orch.integrate_paradox(user_paradox)

    # 4. Find the note
    workspace_dir = Path.home() / "Desktop" / "OmniMind_Workspace"
    time.sleep(1)  # Give OS time to write
    files = list(workspace_dir.glob("OMNIMIND_NOTA_DE_CAMPO*.txt"))
    files.sort(key=lambda f: f.stat().st_mtime, reverse=True)

    if not files:
        logger.error("❌ O sistema não escreveu a nota.")
        return

    note_path = files[0]
    logger.info(f"✅ Nota Aberta: {note_path}")
    logger.info("⏳ O sistema agora aguarda sua resposta real (Service Daemon Active)...")


if __name__ == "__main__":
    asyncio.run(run_session())
