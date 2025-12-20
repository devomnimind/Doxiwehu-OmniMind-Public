#!/usr/bin/env python3
"""
System State Snapshot & Ghost Hunter
------------------------------------
Captures current system state (memory, cpu, processes) and identifies
potential interfering 'ghost' services before intense training runs.
"""

import psutil
import datetime
import json
import os
import sys


def snapshot_system(label="baseline"):
    snapshot = {
        "timestamp": datetime.datetime.now().isoformat(),
        "label": label,
        "memory": dict(psutil.virtual_memory()._asdict()),
        "swap": dict(psutil.swap_memory()._asdict()),
        "load_avg": os.getloadavg(),
        "omnimind_processes": [],
        "ghost_candidates": [],
    }

    print(f"📸 Taking System Snapshot: {label}")
    print(f"   Memory Used: {snapshot['memory']['percent']}%")
    print(f"   Swap Used: {snapshot['swap']['percent']}%")

    # Scan processes
    for proc in psutil.process_iter(["pid", "name", "cmdline", "memory_percent"]):
        try:
            pinfo = proc.info
            cmdline = " ".join(pinfo["cmdline"] or [])

            # Identify OmniMind processes
            if "omnimind" in cmdline or "python" in pinfo["name"]:
                snapshot["omnimind_processes"].append(
                    {"pid": pinfo["pid"], "cmd": cmdline[:100], "mem": pinfo["memory_percent"]}
                )

            # Identify potential heavy 'ghosts' (high memory not related to us)
            elif pinfo["memory_percent"] > 1.0:
                snapshot["ghost_candidates"].append(
                    {"pid": pinfo["pid"], "name": pinfo["name"], "mem": pinfo["memory_percent"]}
                )

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    print(f"   OmniMind Processes: {len(snapshot['omnimind_processes'])}")
    print(f"   Heavy External Processes: {len(snapshot['ghost_candidates'])}")

    # Save snapshot
    os.makedirs("data/snapshots", exist_ok=True)
    filename = (
        f"data/snapshots/system_state_{label}_{int(datetime.datetime.now().timestamp())}.json"
    )
    with open(filename, "w") as f:
        json.dump(snapshot, f, indent=2)

    print(f"💾 Snapshot saved to {filename}")


if __name__ == "__main__":
    label = sys.argv[1] if len(sys.argv) > 1 else "manual"
    snapshot_system(label)
