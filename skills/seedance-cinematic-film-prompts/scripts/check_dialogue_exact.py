#!/usr/bin/env python3
"""Compare source and prompt dialogue TSV files exactly."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


def read_tsv(path: Path) -> list[tuple[str, str, str]]:
    rows: list[tuple[str, str, str]] = []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle, delimiter="\t")
        for line_number, row in enumerate(reader, start=1):
            if not row or all(cell == "" for cell in row):
                continue
            if row == ["shot_id", "speaker", "dialogue"]:
                continue
            if len(row) != 3:
                raise ValueError(
                    f"{path}:{line_number}: expected 3 tab-separated fields "
                    f"(shot_id, speaker, dialogue), got {len(row)}"
                )
            rows.append((row[0], row[1], row[2]))
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify that source and prompt dialogue TSV rows match exactly."
    )
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--prompt", required=True, type=Path)
    args = parser.parse_args()

    source = read_tsv(args.source)
    prompt = read_tsv(args.prompt)
    ok = True

    if len(source) != len(prompt):
        print(f"FAIL: row count differs: source={len(source)} prompt={len(prompt)}")
        ok = False

    for index, (source_row, prompt_row) in enumerate(zip(source, prompt), start=1):
        if source_row != prompt_row:
            ok = False
            print(f"FAIL: row {index} differs")
            print(f"  source: {source_row!r}")
            print(f"  prompt: {prompt_row!r}")

    if ok:
        print(f"PASS: {len(source)} dialogue rows match exactly.")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
