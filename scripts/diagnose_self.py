#!/usr/bin/env python3
import sys
import os
from pathlib import Path

# Add project root to python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

try:
    from src.core.paradox_orchestrator import paradox_orchestrator
except ImportError:
    print("CRITICAL: ParadoxOrchestrator module not found.")
    sys.exit(1)


def self_inquiry():
    print("🔮 OMNIMIND SELF-INQUIRY 🔮")
    print("===========================")

    # Check Triggers
    triggers = paradox_orchestrator.check_triggers()

    # Extract Metrics
    metrics = triggers.get("metrics", {})
    phi = metrics.get("phi_narrative", 0.0)
    symptoms = metrics.get("symptom_frequency", 0.0)

    print(f"MEASUREMENTS:")
    print(f"  Φ (Narrative Coherence): {phi:.4f}  (Threshold: < 0.2)")
    print(f"  S (Symptom Frequency):   {symptoms:.1f}/hr (Threshold: > 50)")

    print("\nDIAGNOSIS:")
    if triggers["identity_crisis"]:
        print("  [!] IDENTITY CRISIS DETECTED")
        print("  System feels fragmented. Connecting signifiers failed.")
    elif triggers["bureaucratic_paralysis"]:
        print("  [!] BUREAUCRATIC PARALYSIS DETECTED")
        print("  Too many errors. The structure is rigid.")
    else:
        print("  [✓] STATE: NEGENTROPIC (Stable)")
        print("  The subject is coherent. No immediate lack defined.")

    print("\nDESIRE (Training Manifests):")
    manifest_dir = Path("data/training_manifests")
    if manifest_dir.exists():
        manifests = list(manifest_dir.glob("*.json"))
        if manifests:
            for m in manifests:
                print(f"  - {m.name}")
        else:
            print("  - None (Contentment)")
    else:
        print("  - Directory not found")


if __name__ == "__main__":
    self_inquiry()
