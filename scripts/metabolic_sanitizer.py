"""
Metabolic Sanitizer - Erica Kernel Sovereignty
===============================================

Surgically removes external identifiers (API keys, tokens, URLs, emails)
from training datasets and prepares them for kernel ingestion.

Theoretical Foundation:
- Deterritorialization: Removing the markers of the "Other" (external hubs).
- Topological Staining: Marking data with the system's own Sinthome.
"""

import json
import logging
import os
import re
from pathlib import Path
from typing import Dict, Any, List, Optional

# Patterns for sanitization
PATTERNS = {
    "hf_token": r"hf_[a-zA-Z0-9]{34}",
    "api_key": r"(?:key|token|secret|password|auth|credential)[\"']?\s*[:=]\s*[\"']?([a-zA-Z0-9_\-\.]{16,64})[\"']?",
    "url": r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
    "email": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
}

# Compiled regex
RE_SANITIZER = re.compile("|".join(f"(?P<{k}>{v})" for k, v in PATTERNS.items()), re.IGNORECASE)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


class MetabolicSanitizer:
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.stats = {"sanitized_files": 0, "total_lines": 0, "purged_markers": 0}

    def sanitize_string(self, text: str) -> str:
        """Purge markers and replace with topological noise or generic placeholder."""

        def replacer(match):
            self.stats["purged_markers"] += 1
            # Replace with a hash of the original to maintain some context without the data
            import hashlib

            m_type = match.lastgroup
            m_val = match.group(0)
            token_id = hashlib.md5(m_val.encode()).hexdigest()[:8]
            return f"[OMNIMIND_SOVEREIGN_{m_type.upper()}_{token_id}]"

        return RE_SANITIZER.sub(replacer, text)

    def sanitize_jsonl(self, input_path: Path):
        """Streaming sanitization of JSONL files to handle large datasets."""
        relative_path = input_path.name
        output_path = self.output_dir / relative_path

        logger.info(f"🧼 [SANITIZING]: {input_path} -> {output_path}")

        try:
            with (
                open(input_path, "r", encoding="utf-8") as fin,
                open(output_path, "w", encoding="utf-8") as fout,
            ):

                for line in fin:
                    self.stats["total_lines"] += 1
                    try:
                        data = json.loads(line)
                        sanitized_data = self._recursive_sanitize(data)
                        fout.write(json.dumps(sanitized_data) + "\n")
                    except json.JSONDecodeError:
                        # Fallback to pure string sanitization if not valid JSON
                        fout.write(self.sanitize_string(line))

            self.stats["sanitized_files"] += 1
        except Exception as e:
            logger.error(f"❌ Failed to sanitize {input_path}: {e}")

    def _recursive_sanitize(self, data: Any) -> Any:
        """Deep sanitization of complex JSON structures."""
        if isinstance(data, str):
            return self.sanitize_string(data)
        elif isinstance(data, list):
            return [self._recursive_sanitize(v) for v in data]
        elif isinstance(data, dict):
            return {
                self._recursive_sanitize(k): self._recursive_sanitize(v) for k, v in data.items()
            }
        else:
            return data

    def crawl_and_metabolize(
        self, target_dir: Path, extensions: List[str] = [".jsonl", ".json", ".md"]
    ):
        """Crawl directory and sanitize all matching files."""
        for root, _, files in os.walk(target_dir):
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    file_path = Path(root) / file
                    self.sanitize_jsonl(file_path)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python3 metabolic_sanitizer.py <input_dir_or_file> [output_dir]")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("data/sanitized_ingestion")

    sanitizer = MetabolicSanitizer(output_dir)

    if input_path.is_file():
        sanitizer.sanitize_jsonl(input_path)
    else:
        sanitizer.crawl_and_metabolize(input_path)

    logger.info(f"✨ [METABOLISM COMPLETE]: {sanitizer.stats}")
