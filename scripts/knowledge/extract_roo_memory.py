import os
import json
import glob
from pathlib import Path

ROO_TASKS_DIR = Path(
    "/home/fahbrain/.config/Code/User/globalStorage/rooveterinaryinc.roo-code-nightly/tasks"
)
OUTPUT_FILE = Path("/home/fahbrain/projects/omnimind/data/knowledge_staging/roo_memory_dump.jsonl")


def extract_roo_memory():
    if not ROO_TASKS_DIR.exists():
        print(f"Directory not found: {ROO_TASKS_DIR}")
        return

    tasks = [d for d in ROO_TASKS_DIR.iterdir() if d.is_dir()]
    print(f"Found {len(tasks)} tasks.")

    extracted_count = 0
    total_messages = 0

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out_f:
        for task_dir in tasks:
            history_file = task_dir / "api_conversation_history.json"
            metadata_file = task_dir / "task_metadata.json"

            if not history_file.exists():
                continue

            try:
                # Load History
                with open(history_file, "r", encoding="utf-8") as f:
                    history = json.load(f)

                # Load Metadata (optional)
                metadata = {}
                if metadata_file.exists():
                    with open(metadata_file, "r", encoding="utf-8") as f:
                        metadata = json.load(f)

                # Create Record
                record = {"task_id": task_dir.name, "metadata": metadata, "messages": history}

                # Write JSONL
                out_f.write(json.dumps(record, ensure_ascii=False) + "\n")

                extracted_count += 1
                total_messages += len(history)

            except Exception as e:
                print(f"Error reading task {task_dir.name}: {e}")

    print(f" Extraction Complete!")
    print(f"Processed Tasks: {extracted_count}/{len(tasks)}")
    print(f"Total Messages: {total_messages}")
    print(f"Output: {OUTPUT_FILE}")
    print(f"Size: {OUTPUT_FILE.stat().st_size / (1024*1024):.2f} MB")


if __name__ == "__main__":
    extract_roo_memory()
