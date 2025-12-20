#!/usr/bin/env python3
"""
Log Rotation Script
Enforces strict data retention policy:
1. Archives logs older than 2 days.
2. Compresses archived logs (.gz).
3. Deletes archives older than 7 days.
4. Truncates active logs if they exceed 100MB (after archiving).
"""

import os
import time
import shutil
import gzip
import logging
from pathlib import Path
from datetime import datetime

# Configuration
LOG_DIRS = ["logs", "data/monitor/module_metrics", "data/test_reports"]
ARCHIVE_DIR = Path("logs/archive")
RETENTION_DAYS = 2
DELETE_ARCHIVE_DAYS = 7
MAX_FILE_SIZE_MB = 100


def setup_logging():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def compress_file(file_path):
    """Compresses a file using gzip."""
    with open(file_path, "rb") as f_in:
        with gzip.open(f"{file_path}.gz", "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
    return f"{file_path}.gz"


def should_rotate(file_path):
    """Checks if file is older than retention period or too large."""
    if not file_path.exists():
        return False
    stat = os.stat(file_path)
    mtime = datetime.fromtimestamp(stat.st_mtime)
    size_mb = stat.st_size / (1024 * 1024)

    age_days = (datetime.now() - mtime).days

    return age_days >= RETENTION_DAYS or size_mb > MAX_FILE_SIZE_MB


def rotate_logs():
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

    rotated_count = 0
    deleted_count = 0

    for log_dir in LOG_DIRS:
        path = Path(log_dir)
        if not path.exists():
            continue

        # Find all log/jsonl files
        files = list(path.glob("*.log")) + list(path.glob("*.jsonl")) + list(path.glob("*.bak"))

        for file_path in files:
            if should_rotate(file_path):
                # Archive
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                archive_name = f"{file_path.stem}_{timestamp}{file_path.suffix}"
                archive_path = ARCHIVE_DIR / archive_name

                logging.info(f"Rotating {file_path} -> {archive_path}")

                # Copy then truncate (or move if .bak)
                if file_path.suffix == ".bak":
                    shutil.move(str(file_path), str(archive_path))
                else:
                    shutil.copy2(file_path, archive_path)
                    # Truncate original
                    with open(file_path, "w") as f:
                        f.write(f"--- Rotated at {datetime.now()} ---\n")

                # Compress archive
                compress_file(archive_path)
                if archive_path.exists():  # Remove uncompressed
                    os.remove(archive_path)

                rotated_count += 1

    # Cleanup Archives
    now = time.time()
    for archive_path in ARCHIVE_DIR.glob("*"):
        stat = os.stat(archive_path)
        if (now - stat.st_mtime) > (DELETE_ARCHIVE_DAYS * 86400):
            logging.info(f"Deleting old archive: {archive_path}")
            os.remove(archive_path)
            deleted_count += 1

    logging.info(f"Rotation Complete. Rotated: {rotated_count}, Deleted: {deleted_count}")


if __name__ == "__main__":
    setup_logging()
    rotate_logs()
