#!/usr/bin/env python3
"""
OmniMind Local Federation Pulse
Broadcasts presence via UDP for local discovery.
"""
import json
import logging
import socket
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("OmniMindPulse")

def broadcast_pulse():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Broadcast to port 5556
    target = ('<broadcast>', 5556)

    logger.info(f"💓 Starting Pulse Broadcast to {target}...")

    try:
        while True:
            message = json.dumps({
                "type": "OMNIMIND_PULSE",
                "name": "OMNIMIND_DESKTOP",
                "service_port": 5555,
                "timestamp": time.time()
            }).encode('utf-8')

            sock.sendto(message, target)
            time.sleep(5)
    except KeyboardInterrupt:
        logger.info("🛑 Stopping Pulse...")
    except Exception as e:
        logger.error(f"❌ Pulse Error: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    broadcast_pulse()
