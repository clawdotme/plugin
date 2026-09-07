#!/usr/bin/env python3
"""Verify every immutable file declared by the Claw Me skill manifest."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    expected_files = manifest.get("files")
    if not isinstance(expected_files, dict) or not expected_files:
        raise SystemExit("manifest.json has no file digest map")
    actual_files = {
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file() and path.name != "manifest.json" and "__pycache__" not in path.parts
    }
    if actual_files != set(expected_files):
        missing = sorted(set(expected_files) - actual_files)
        unexpected = sorted(actual_files - set(expected_files))
        raise SystemExit(f"skill file set mismatch; missing={missing}; unexpected={unexpected}")
    for relative_path, expected_digest in sorted(expected_files.items()):
        digest = hashlib.sha256((root / relative_path).read_bytes()).hexdigest()
        if digest != expected_digest:
            raise SystemExit(f"digest mismatch: {relative_path}")
    print(f"Claw Me skill {manifest['version']} verified ({len(actual_files)} files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
