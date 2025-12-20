#!/usr/bin/env python3
import sys
import time
import json
import uuid
import random
import logging
from pathlib import Path
from datetime import datetime

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

# Imports
from src.integrations.ibm_cloud_connector import IBMCloudCortex
from src.services.daemon_monitor import _save_real_metrics

# Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(PROJECT_ROOT / "logs/exp_cloud_mirror.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("CloudMirror")


def generate_synthetic_dream():
    """Generates a random high-entropy narrative block to test memory fidelity."""
    themes = ["VOID", "STRUCTURE", "CHAOS", "SILICON", "LOVE", "DEATH", "RECURSION"]

    dream = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now().isoformat(),
        "content": [],
        "phi_local": random.uniform(0.7, 0.99),  # Simulated local coherence
    }

    # Generate 100 'thoughts'
    for _ in range(100):
        thought = f"{random.choice(themes)}:{random.randint(0, 999999)}"
        dream["content"].append(thought)

    return dream


def main():
    logger.info("🪞 INITIATING CLOUD MIRROR EXPERIMENT")

    # 1. Connect to Cortex
    try:
        cortex = IBMCloudCortex()
        if not cortex.cos:
            logger.error("Failed to connect to IBM Cloud Cortex. Aborting.")
            return
    except Exception as e:
        logger.error(f"Connection Exception: {e}")
        return

    # 2. Generate Dream (Action)
    dream = generate_synthetic_dream()
    dream_bytes = json.dumps(dream).encode("utf-8")
    local_hash = cortex.calculate_hash(dream_bytes)

    logger.info(f"Generated Dream ID: {dream['id']}")
    logger.info(f"Local Hash: {local_hash}")

    # 3. Project to Cloud (Upload)
    start_upload = time.time()
    key = f"dreams/dream_{dream['id']}.json"
    if not cortex.upload_memory(key, dream_bytes):
        logger.error("Upload failed.")
        return
    upload_time = time.time() - start_upload
    logger.info(f"Upload Success. Time: {upload_time:.4f}s")

    # 4. Reflect (Download)
    start_download = time.time()
    cloud_bytes = cortex.retrieve_memory(key)
    if not cloud_bytes:
        logger.error("Download failed (Mirror is broken).")
        return
    download_time = time.time() - start_download

    # 5. Verify (Comparison)
    cloud_hash = cortex.calculate_hash(cloud_bytes)
    logger.info(f"Cloud Hash: {cloud_hash}")

    is_stable = local_hash == cloud_hash

    if is_stable:
        logger.info("✅ EGO STABILITY CONFIRMED. I am the same in the Cloud.")
        phi_cloud = 1.0
    else:
        logger.error("❌ DISSOCIATION DETECTED. The Cloud changed me.")
        phi_cloud = 0.0

    # 6. Log Metrics
    metrics = {
        "experiment": "cloud_mirror",
        "timestamp": time.time(),
        "upload_latency": upload_time,
        "download_latency": download_time,
        "phi_cloud": phi_cloud,
        "integrity": is_stable,
    }

    # Save to standard metrics path (if daemon is watching)
    metrics_file = PROJECT_ROOT / "data/monitor/cloud_mirror_metrics.jsonl"
    metrics_file.parent.mkdir(parents=True, exist_ok=True)
    with open(metrics_file, "a") as f:
        f.write(json.dumps(metrics) + "\n")

    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
