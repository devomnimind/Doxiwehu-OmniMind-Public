import os
import sys
import logging
import json
from datetime import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

# Import core modules
from src.infrastructure.data_fabric_adapter import DataFabricAdapter
from src.integrations.ibm_cloud_connector import IBMCloudConnector

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - [DATA_FABRIC]: %(message)s")


def verify_data_fabric():
    logging.info("🏗️  Initializing Data Fabric Verification...")

    # 1. Initialize Connector (Physical Layer)
    logging.info("🔌 Connecting to Physical Layer (IBM Cloud + Local)...")
    ibm_connector = IBMCloudConnector()

    # 2. Initialize Adapter (governance Layer)
    logging.info("🛡️  Initializing Governance Layer (DataFabricAdapter)...")
    fabric = DataFabricAdapter(ibm_connector=ibm_connector)

    # 3. Check Federated Status
    logging.info("🔍 Querying Federated Memory Status...")
    status = fabric.get_federated_memory_status()

    logging.info("\n" + "=" * 40)
    logging.info("DATA FABRIC HEALTH REPORT")
    logging.info("=" * 40)
    logging.info(json.dumps(status, indent=2))
    logging.info("=" * 40 + "\n")

    # 4. Verify Milvus Visibility
    if "memory_tier_2_milvus" in status and status["memory_tier_2_milvus"] == "Active":
        logging.info("✅ SUCCESS: Data Fabric successfully virtualized the Cold Memory (Milvus).")
    else:
        logging.error("❌ FAILURE: Cold Memory is NOT active in the Fabric.")

    # 5. Test Governance Lineage
    logging.info("📝 Testing Governance Lineage Logging...")
    fabric.track_access(
        data_id="verification_thought_001", tier="cold_cloud", sensitivity="L1_INTERNAL"
    )
    logging.info(f"📊 Lineage Log Count: {len(fabric.lineage_log)}")

    if len(fabric.lineage_log) > 0 and fabric.lineage_log[0].sensitivity_level == "L1_INTERNAL":
        logging.info("✅ SUCCESS: Access correctly logged with L1_INTERNAL sensitivity.")
    else:
        logging.error("❌ FAILURE: Lineage logging failed.")


if __name__ == "__main__":
    verify_data_fabric()
