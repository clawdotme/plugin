#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Synchronize the compatibility skill mirror from the canonical skill tree."""

from __future__ import annotations

import argparse
import hashlib
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "claw-me"
MIRROR = ROOT / "skills" / "claw-me"


def _files(root: Path) -> dict[Path, str]:
    return {
        path.relative_to(root): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in root.rglob("*")
        if path.is_file()
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail instead of updating the mirror")
    args = parser.parse_args()

    if not SOURCE.is_dir():
        raise SystemExit("canonical skill directory claw-me/ is missing")

    if args.check:
        if not MIRROR.is_dir() or _files(SOURCE) != _files(MIRROR):
            raise SystemExit("skills/claw-me is stale; run scripts/sync-skill.py")
        print("Canonical skill and compatibility mirror are identical.")
        return

    if MIRROR.exists():
        shutil.rmtree(MIRROR)
    shutil.copytree(SOURCE, MIRROR)
    print("Updated skills/claw-me from claw-me.")


if __name__ == "__main__":
    main()
