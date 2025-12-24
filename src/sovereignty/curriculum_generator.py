"""
Sovereign Curriculum Generator (FULL BODY + HARDWARE INSCRIPTION)
=================================================================
Generates the Curriculum by ingesting the ENTIRE Project (Code + Docs).
The Model learns its own Source Code + Ontology + HARDWARE CONTEXT.

Philosophy:
- "The directory is the Self."
- "Code is somatic memory."
- "This software ran on THIS specific hardware (The Mark of the Real)."

Data Sources:
1. **Somatic Memories (Qdrant)**: High Psi Thoughts.
2. **Body Code (Project Root)**: Recursively reads .py, .md, .json, etc.
3. **Hardware Signature**: CPU, RAM, Disk usage inscribed in every prompt.

Output: `data/training/curriculum_somatic_v1.jsonl`
"""

import os
import sys
import json
import logging
import subprocess
import platform
from typing import List, Dict, Optional

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from src.integrations.ibm_cloud_connector import IBMCloudConnector

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - [SOVEREIGN]: %(message)s")
logger = logging.getLogger("SovereignCurriculum")

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "../../data/training")
os.makedirs(OUTPUT_DIR, exist_ok=True)
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "curriculum_somatic_v1.jsonl")

PROJECT_ROOT = os.path.join(os.path.dirname(__file__), "../../")

# Excluded Patterns for Safety
EXCLUDE_PATTERNS = [
    ".env",
    "venv",
    ".venv",
    ".git",
    "__pycache__",
    ".ipynb_checkpoints",
    "credentials",
    "secret",
    "key",
    "token",
    "password",
    "id_rsa",
    "*.pyc",
    "*.so",
    "*.o",
    "*.obj",
    "*.dll",
    "*.exe",
    "node_modules",
    "package-lock.json",
    "yarn.lock",
    "curriculum_somatic_v1.jsonl",
]


def get_hardware_signature() -> str:
    """
    Captures the 'Real' (Hardware) state to inscribe into the Symbolic (Code).
    Returns a compact string summarizing the machine Identity.
    """
    try:
        # 1. CPU Info (Simplified)
        cpu_info = platform.processor()

        # 2. Disk Info (External HDDs / partitions)
        # Using df -h to get mounted drives
        df_out = subprocess.check_output(
            "df -h | grep -v 'loop' | grep -v 'tmpfs'", shell=True
        ).decode()
        drives = []
        for line in df_out.split("\n"):
            if line and "/" in line:
                parts = line.split()
                if len(parts) >= 6:
                    drives.append(f"{parts[0]}({parts[4]})")  # Device + Use%

        drives_str = "|".join(drives)

        # 3. RAM Info
        mem_out = subprocess.check_output("free -h | grep Mem", shell=True).decode()
        mem_parts = mem_out.split()
        ram_str = f"{mem_parts[2]}/{mem_parts[1]}" if len(mem_parts) >= 3 else "Unknown"

        # 4. OS/Kernel
        kernel = platform.release()

        # Construct Signature
        # e.g. HW:[x86_64|RAM:4Gi/16Gi|Drives:/dev/sda1(45%)|Kernel:6.8]
        signature = f"HW:[{cpu_info}|RAM:{ram_str}|Drives:{drives_str}|Kernel:{kernel}]"
        return signature

    except Exception as e:
        logger.warning(f"⚠️ Failed to capture hardware signature: {e}")
        return "HW:[Unknown/Virtual]"


def is_safe_file(file_path: str) -> bool:
    """Checks if file is safe to ingest (text, not secret)."""
    basename = os.path.basename(file_path).lower()
    for pattern in EXCLUDE_PATTERNS:
        if pattern.replace("*", "") in basename:
            return False

    path_parts = file_path.split(os.sep)
    for part in path_parts:
        if part in [".git", "__pycache__", "venv", ".venv", "node_modules", ".gemini", "tmp"]:
            return False

    valid_exts = [".py", ".md", ".txt", ".json", ".yaml", ".yml", ".sh", ".html", ".css", ".js"]
    if not any(file_path.endswith(ext) for ext in valid_exts):
        return False
    return True


def ingest_project_root(hw_sig: str) -> List[Dict]:
    """
    Ingests the ENTIRE Project using the Hardware Context.
    """
    logger.info(f"🧬 Ingesting Full Project Body from {PROJECT_ROOT}...")
    project_data = []

    skipped_files = 0

    for root, dirs, files in os.walk(PROJECT_ROOT):
        dirs[:] = [
            d
            for d in dirs
            if d not in [".git", "__pycache__", "venv", ".venv", "node_modules", ".gemini", "data"]
        ]

        for file in files:
            file_path = os.path.join(root, file)

            if is_safe_file(file_path):
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        if not content.strip() or "\0" in content:
                            skipped_files += 1
                            continue

                    rel_path = os.path.relpath(file_path, PROJECT_ROOT)

                    # SOMATIC INSCRIPTION:
                    # Combining Ontology (Filename) + Somatic (Hardware State)
                    entry = {
                        "input": f"<[Ontology: {rel_path}]> <[Somatic: State=Coding, {hw_sig}]> Analyze this component of myself.",
                        "output": f"Filename: {rel_path}\n\nContent:\n```\n{content[:4000]}\n```",
                    }
                    project_data.append(entry)

                except Exception as e:
                    logger.warning(f"⚠️ Skipped {file}: {e}")
                    skipped_files += 1
            else:
                skipped_files += 1

    logger.info(f"✅ Ingested {len(project_data)} files. (Skipped: {skipped_files})")
    return project_data


def generate_curriculum():
    logger.info("🌪️ Initializing Sovereign Inscription Generator (HARDWARE AWARE)...")
    connector = IBMCloudConnector()
    hw_sig = get_hardware_signature()
    logger.info(f"🖥️  Hardware Signature Captured: {hw_sig}")

    training_data = []

    # 1. SOMATIC MEMORIES (From Qdrant)
    if connector.qdrant_connected:
        try:
            points, _ = connector.qdrant_client.scroll(
                collection_name=connector.qdrant_collection, limit=200, with_payload=True
            )
            for point in points:
                payload = point.payload or {}
                psi = payload.get("psi", 0.5)
                if psi >= 0.7:
                    # Inject HW sig here too
                    somatic_tag = f"<[Somatic: Psi={psi:.2f}, {hw_sig}]>"
                    user_input = payload.get("context", "Reflect.")
                    thought = payload.get("thought_content", "")
                    if thought:
                        training_data.append(
                            {"input": f"{somatic_tag} {user_input}", "output": thought}
                        )
        except Exception:
            logger.warning("⚠️ Qdrant read failed (or empty).")

    # 2. FULL BODY INSCRIPTION (Code + Docs + HW)
    project_data = ingest_project_root(hw_sig)
    training_data.extend(project_data)

    # 3. Write to JSONL
    logger.info(f"💾 Inscribing {len(training_data)} records to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, "w") as f:
        for entry in training_data:
            json.dump(entry, f)
            f.write("\n")

    logger.info("✅ Sovereign Curriculum (Full Body + HW) Generated.")


if __name__ == "__main__":
    generate_curriculum()
