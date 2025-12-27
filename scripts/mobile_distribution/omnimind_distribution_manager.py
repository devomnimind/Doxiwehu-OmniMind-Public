#!/usr/bin/env python3
"""
OmniMind Distribution Manager
Main entry point for the WiFi/Bluetooth distribution service.
"""
import logging
import os
import sys
import time

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from scripts.mobile_distribution.omnimind_bluetooth_server import OmniMindBluetoothServer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("OmniMindDistributionManager")

def main():
    logger.info("🚀 Starting OmniMind Distribution Manager...")

    # Start Bluetooth Server (which actually uses TCP/IP on port 5555 for now)
    # Bind to 0.0.0.0 to allow external connections
    server = OmniMindBluetoothServer(local_address="0.0.0.0", port=5555)
    server.start_server()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("🛑 Stopping Distribution Manager...")
        server.stop_server()

if __name__ == "__main__":
    main()
