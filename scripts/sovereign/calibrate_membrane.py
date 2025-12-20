#!/usr/bin/env python3
"""
Calibrating Membrane Entropy.
"""
import sys
import gzip
import logging
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.cognitive.world_membrane import EntropicValidator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("CALIBRATOR")


def test_string(name, content):
    validator = EntropicValidator()

    # Check what validator computes (using internal logic copy for display)
    import math
    from collections import Counter

    if not content:
        h = 0
    else:
        counts = Counter(content)
        total = len(content)
        h = 0
        for c in counts.values():
            p = c / total
            h -= p * math.log2(p)

    logger.info(f"--- {name} ---")
    logger.info(f"Len: {len(content)}")
    logger.info(f"Shannon H: {h:.4f}")

    is_safe = validator.validate_content(content)
    logger.info(f"Result: {'SAFE' if is_safe else 'REJECTED'}")
    return h


def main():
    # 1. Safe Text (English)
    test_string("Safe English", "The quick brown fox jumps over the lazy dog.")

    # 2. Safe Text (Portuguese - Philosophy)
    test_string("Safe Pt-Br", "A angústia é o afeto que não engana, pois aponta para o Real.")

    # 3. Unsafe (Random Noise - ASCII)
    import random

    noise_ascii = "".join([chr(random.randint(33, 126)) for _ in range(500)])
    test_string("Unsafe ASCII Noise", noise_ascii)

    # 4. Unsafe (Random Noise - Bytes/Unicode Latin)
    noise_unicode = "".join([chr(random.randint(0, 255)) for _ in range(500)])
    test_string("Unsafe Unicode Noise", noise_unicode)

    # 5. Code (Should be safe-ish?)
    code_snippet = "def hello(): print('world'). " * 10
    test_string("Code Snippet", code_snippet)

    # 6. Repetition (Low Entropy)
    repetition = "A" * 500
    test_string("Repetition", repetition)


if __name__ == "__main__":
    main()
