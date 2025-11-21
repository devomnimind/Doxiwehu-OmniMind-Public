#!/usr/bin/env python3
"""
Add `-> None` return annotations to test functions missing them.

This script edits files under `tests/` and adds `-> None` to definitions
starting with `def test_...` that are missing an explicit return annotation.

It performs a conservative, idempotent transformation and writes changes
back to the files.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable


TESTS_DIR = Path(__file__).resolve().parents[2] / "tests"


def find_test_files() -> Iterable[Path]:
    for p in TESTS_DIR.rglob("*.py"):
        yield p


RE_DEF = re.compile(r"^(\s*)def\s+(test_[A-Za-z0-9_]+)\s*\((.*?)\)\s*:\s*$")


def add_return_none_to_tests(path: Path) -> bool:
    text = path.read_text(encoding="utf8")
    changed = False
    out_lines: list[str] = []

    for line in text.splitlines(keepends=False):
        match = RE_DEF.match(line)
        if match:
            indent, name, params = match.groups()
            # skip if already annotated on the same line (-> present)
            if "->" in line:
                out_lines.append(line)
                continue

            # Add explicit -> None before the colon
            new_line = f"{indent}def {name}({params}) -> None:"
            out_lines.append(new_line)
            changed = True
        else:
            out_lines.append(line)

    if changed:
        path.write_text("\n".join(out_lines) + "\n", encoding="utf8")

    return changed


def main() -> None:
    changed_files = []
    for f in find_test_files():
        if add_return_none_to_tests(f):
            changed_files.append(str(f))

    print(f"Updated {len(changed_files)} test files:")
    for p in changed_files[:50]:
        print(" -", p)


if __name__ == "__main__":
    main()
