import json
import hashlib
import shutil
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent.absolute()
LOG_FILE = PROJECT_ROOT / "logs/audit_chain.log"
REPAIRED_FILE = PROJECT_ROOT / "logs/audit_chain_repaired.log"
BACKUP_FILE = PROJECT_ROOT / "logs/audit_chain.bak"


def hash_content(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def repair_streaming():
    file_size_mb = LOG_FILE.stat().st_size / 1024 / 1024
    print(f"🔧 Starting Streaming Repair on {LOG_FILE} ({file_size_mb:.2f} MB)...")

    if not LOG_FILE.exists():
        print("❌ Log file not found.")
        return

    # Backup
    shutil.copy2(LOG_FILE, BACKUP_FILE)
    print(f"📦 Backup created at {BACKUP_FILE}")

    prev_hash = "0" * 64
    valid_count = 0
    repaired_count = 0
    dropped_count = 0

    with open(LOG_FILE, "rb") as fin, open(REPAIRED_FILE, "wb") as fout:
        for i, line in enumerate(fin, 1):
            if not line.strip():
                continue

            try:
                event = json.loads(line)
                action = event.get("action", "")

                # Logic: We treat the event content as the truth, but we MUST enforce the chain.
                # Use current prev_hash.

                # Reconstruct object for hashing (without current_hash)
                event_for_hash = {
                    "action": event.get("action"),
                    "category": event.get("category"),
                    "details": event.get("details"),
                    "timestamp": event.get("timestamp"),
                    "datetime_utc": event.get("datetime_utc"),
                    "prev_hash": prev_hash,  # Force correct linkage
                }

                # Calculate what the hash SHOULD be
                json_data = json.dumps(event_for_hash, sort_keys=True).encode("utf-8")
                calculated_hash = hash_content(json_data)

                stored_hash = event.get("current_hash")
                stored_prev = event.get("prev_hash")

                # Check 1: Is it valid as is?
                is_valid = calculated_hash == stored_hash and stored_prev == prev_hash

                # Check 2: Special handling for start of file duplicates
                # If we encounter duplicate timestamps/events, we might want to drop them?
                # Actually, rewriting with new prev_hash makes them valid but distinct.
                # But if they are logically duplicates, maybe we should drop?
                # For now, let's RECOVER everything by re-signing.

                if is_valid:
                    fout.write(line)
                    prev_hash = stored_hash
                    valid_count += 1
                else:
                    # Repair: Update hashes in the object
                    event_for_hash["current_hash"] = calculated_hash

                    # Log what happened
                    if i < 10:
                        print(
                            f"   ⚠️ Line {i} Repaired: {action} "
                            f"(Prev: {stored_prev[:8]}->{prev_hash[:8]})"
                        )

                    # Write repaired line
                    repaired_line = json.dumps(event_for_hash, sort_keys=True).encode("utf-8")
                    fout.write(repaired_line + b"\n")

                    prev_hash = calculated_hash
                    repaired_count += 1

            except json.JSONDecodeError:
                print(f"   ❌ Line {i} Dropped: Invalid JSON")
                dropped_count += 1

    print("\n✅ Streaming Repair Complete.")
    print(f"Valid: {valid_count}")
    print(f"Repaired: {repaired_count}")
    print(f"Dropped: {dropped_count}")

    # Swap
    if repaired_count > 0 or dropped_count > 0:
        print("🔄 Swapping files...")
        shutil.move(REPAIRED_FILE, LOG_FILE)
        print("✅ Log file updated.")
    else:
        print("nothing changed.")
        REPAIRED_FILE.unlink()


if __name__ == "__main__":
    repair_streaming()
