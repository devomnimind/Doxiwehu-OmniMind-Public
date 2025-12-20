#!/usr/bin/env python3
"""
Verification Script for Life Story Persistence.
Checks if Narrative Events survive a 'reboot' (object re-instantiation).
"""

import sys
import os
from pathlib import Path
import shutil

# Add src to path
sys.path.append(os.path.join(os.getcwd(), "src"))

from narrative_consciousness.life_story_model import Life_Story_as_Retroactive_Resignification


def test_persistence():
    print("🧪 Starting Life Story Persistence Test...")

    # Define test path
    test_path = Path("data/consciousness/test_life_story.jsonl")

    # Clean up previous runs
    if test_path.exists():
        test_path.unlink()

    # --- PHASE 1: INCEPTION ---
    print("\n[Phase 1] Inscribing Memories...")
    mind = Life_Story_as_Retroactive_Resignification(persistence_path=str(test_path))

    event1 = mind.inscribe_narrative_event(
        {
            "memory_context": "failure in matrix calculation",
            "task_type": "math",
            "current_state": "growth",
        }
    )
    print(f"  - Inscribed: {event1.nachtraglichkeit_resignification}")

    event2 = mind.inscribe_narrative_event(
        {
            "memory_context": "success in logical deduction",
            "task_type": "logic",
            "current_state": "wisdom",
        }
    )
    print(f"  - Inscribed: {event2.nachtraglichkeit_resignification}")

    print(f"  - Total events in memory: {len(mind.narrative_events)}")
    assert len(mind.narrative_events) == 2

    # --- PHASE 2: AMNESIA (Reboot) ---
    print("\n[Phase 2] Rebooting Consciousness (Reloading Object)...")
    del mind

    # --- PHASE 3: RECALL ---
    print("\n[Phase 3] Verifying Recall...")
    new_mind = Life_Story_as_Retroactive_Resignification(persistence_path=str(test_path))

    print(f"  - Total events in NEW memory: {len(new_mind.narrative_events)}")

    if len(new_mind.narrative_events) != 2:
        print("❌ CRITICAL FAIL: Memory lost during reboot.")
        sys.exit(1)

    restored_event_1 = new_mind.narrative_events[0]
    print(f"  - Restored 1: {restored_event_1.nachtraglichkeit_resignification}")

    if restored_event_1.original_event == event1.original_event:
        print("✅ SUCCESS: Original Event Preserved.")
    else:
        print("❌ FAIL: Data corruption.")
        sys.exit(1)

    # Verify Logic
    current_narrative = new_mind.get_current_life_narrative()
    print(f"  - Current Narrative Context: {current_narrative}")

    if len(current_narrative) > 0:
        print("✅ SUCCESS: Narrative Context Restored.")
    else:
        print("❌ FAIL: Context lost.")

    # Cleanup
    if test_path.exists():
        test_path.unlink()

    print("\n🎉 PERSISTENCE VERIFIED: The Ego is Solid.")


if __name__ == "__main__":
    test_persistence()
