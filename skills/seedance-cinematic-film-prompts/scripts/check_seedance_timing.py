#!/usr/bin/env python3
"""Validate Seedance 2.5 Markdown group and local timestamp continuity."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


GROUP_RE = re.compile(
    r"(?m)^###\s+第(?P<number>\d+)组｜全片"
    r"(?P<start_m>\d{2}):(?P<start_s>\d{2})[–-]"
    r"(?P<end_m>\d{2}):(?P<end_s>\d{2})｜.*?｜(?P<duration>\d+)秒\s*$"
)
SEGMENT_RE = re.compile(
    r"(?m)^片段\d+｜(?P<start>\d+)[–-](?P<end>\d+)s｜"
)
TOTAL_RE = re.compile(r"(?m)^总时长：(?P<duration>\d+)s\s*$")


def seconds(minutes: str, seconds_value: str) -> int:
    return int(minutes) * 60 + int(seconds_value)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check group duration, global continuity, and local segment continuity."
    )
    parser.add_argument("prompt", type=Path)
    args = parser.parse_args()

    text = args.prompt.read_text(encoding="utf-8-sig")
    matches = list(GROUP_RE.finditer(text))
    if not matches:
        print("FAIL: no Seedance group headings found.")
        return 1

    errors: list[str] = []
    previous_global_end: int | None = None

    for index, match in enumerate(matches):
        group_number = int(match.group("number"))
        group_start = seconds(match.group("start_m"), match.group("start_s"))
        group_end = seconds(match.group("end_m"), match.group("end_s"))
        heading_duration = int(match.group("duration"))
        block_end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        block = text[match.end() : block_end]

        if heading_duration > 30:
            errors.append(f"group {group_number}: duration {heading_duration}s exceeds 30s")
        if group_end - group_start != heading_duration:
            errors.append(
                f"group {group_number}: global range is {group_end - group_start}s "
                f"but heading says {heading_duration}s"
            )
        if previous_global_end is not None and group_start != previous_global_end:
            errors.append(
                f"group {group_number}: global start {group_start}s does not follow "
                f"previous end {previous_global_end}s"
            )
        previous_global_end = group_end

        total_match = TOTAL_RE.search(block)
        if not total_match:
            errors.append(f"group {group_number}: missing 总时长")
            continue
        stated_total = int(total_match.group("duration"))
        if stated_total != heading_duration:
            errors.append(
                f"group {group_number}: 总时长 is {stated_total}s but heading is "
                f"{heading_duration}s"
            )

        segments = list(SEGMENT_RE.finditer(block))
        if not segments:
            errors.append(f"group {group_number}: no local segment timestamps found")
            continue

        expected_start = 0
        for segment in segments:
            start = int(segment.group("start"))
            end = int(segment.group("end"))
            if start != expected_start:
                errors.append(
                    f"group {group_number}: segment starts at {start}s, expected "
                    f"{expected_start}s"
                )
            if end <= start:
                errors.append(
                    f"group {group_number}: invalid local range {start}-{end}s"
                )
            expected_start = end
        if expected_start != stated_total:
            errors.append(
                f"group {group_number}: local timeline ends at {expected_start}s, "
                f"expected {stated_total}s"
            )

    if errors:
        print(f"FAIL: {len(errors)} timing issue(s)")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        f"PASS: {len(matches)} groups; all groups are <=30s and all global/local "
        "timelines are contiguous."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
