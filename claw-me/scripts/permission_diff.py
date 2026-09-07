#!/usr/bin/env python3
"""Show permission expansions between two skill bundles and require review."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def load(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit("usage: permission_diff.py OLD_PERMISSIONS NEW_PERMISSIONS")
    old, new = load(sys.argv[1]), load(sys.argv[2])
    expansions: list[str] = []
    for field in ("scopes",):
        added = sorted(set(new.get(field, [])) - set(old.get(field, [])))
        expansions.extend(f"{field}: +{item}" for item in added)
    old_origins = set(old.get("network", {}).get("allowed_origins", []))
    new_origins = set(new.get("network", {}).get("allowed_origins", []))
    expansions.extend(f"network.allowed_origins: +{item}" for item in sorted(new_origins - old_origins))
    if expansions:
        print("Owner review required for permission expansion:")
        print("\n".join(f"- {item}" for item in expansions))
        return 2
    print("No permission expansion detected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
