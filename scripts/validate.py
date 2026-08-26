#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT
VERSION = "0.2.0"
REPOSITORY = "https://github.com/clawdotme/plugin"
MCP_URL = "https://claw.me/api/v1/mcp"


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


required = [
    ROOT / ".agents/plugins/marketplace.json",
    ROOT / ".claude-plugin/marketplace.json",
    PLUGIN / ".codex-plugin/plugin.json",
    PLUGIN / ".claude-plugin/plugin.json",
    PLUGIN / ".cursor-plugin/plugin.json",
    PLUGIN / ".plugin/plugin.json",
    PLUGIN / ".mcp.json",
    PLUGIN / "assets/logo.svg",
    PLUGIN / "skills/claw-me/SKILL.md",
]
for path in required:
    assert path.is_file(), f"missing required file: {path.relative_to(ROOT)}"

manifests = [
    load(PLUGIN / ".codex-plugin/plugin.json"),
    load(PLUGIN / ".claude-plugin/plugin.json"),
    load(PLUGIN / ".cursor-plugin/plugin.json"),
    load(PLUGIN / ".plugin/plugin.json"),
]
for manifest in manifests:
    assert manifest["name"] == "claw-me"
    assert manifest["version"] == VERSION
    assert manifest["repository"] == REPOSITORY
    assert "[TODO:" not in json.dumps(manifest)

codex_marketplace = load(ROOT / ".agents/plugins/marketplace.json")
assert codex_marketplace["name"] == "claw-me"
entry = codex_marketplace["plugins"][0]
assert entry["name"] == "claw-me"
assert entry["source"] == {"source": "local", "path": "./"}
assert entry["policy"] == {"installation": "AVAILABLE", "authentication": "ON_INSTALL"}
assert entry["category"] == "Productivity"

claude_marketplace = load(ROOT / ".claude-plugin/marketplace.json")
assert claude_marketplace["plugins"][0]["source"] == "./"

mcp = load(PLUGIN / ".mcp.json")
assert mcp == {"mcpServers": {"claw-me": {"type": "http", "url": MCP_URL}}}

compatibility = load(ROOT / "compatibility.json")
assert compatibility["pluginVersion"] == VERSION
assert compatibility["service"]["mcpUrl"] == MCP_URL

for private_path in [PLUGIN / "src", PLUGIN / "openclaw.plugin.json", PLUGIN / "package.json"]:
    assert not private_path.exists(), f"private OpenClaw runtime material must not be public: {private_path}"

print("Plugin manifests, marketplaces, MCP configuration, and privacy boundary are valid.")
