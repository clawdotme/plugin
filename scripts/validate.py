#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT
VERSION = "0.3.3"
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
    PLUGIN / "claw-me/references/wiki-sync.md",
    ROOT / "contracts/onboarding.v1.schema.json",
    ROOT / "contracts/prompts.v1.json",
    ROOT / "contracts/mcp-tools.v1.json",
    ROOT / "contracts/openapi.v1.json",
    ROOT / "SECURITY.md",
    ROOT / "CONTRIBUTING.md",
    ROOT / "THIRD_PARTY_NOTICES.md",
]
for path in required:
    assert path.is_file(), f"missing required file: {path.relative_to(ROOT)}"

license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
assert license_text.startswith("MIT License\n")
assert "Copyright (c) 2026 Claw Me" in license_text

secret_patterns = [
    re.compile(r"sk_live_[A-Za-z0-9]{16,}"),
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
]
for path in ROOT.rglob("*"):
    if not path.is_file() or ".git" in path.parts:
        continue
    if path.suffix.lower() not in {".md", ".json", ".py", ".yml", ".yaml"}:
        continue
    content = path.read_text(encoding="utf-8")
    assert not any(pattern.search(content) for pattern in secret_patterns), f"secret-like value found in {path}"

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
assert compatibility["contracts"] == {
    "onboarding": "1.0.0",
    "prompts": "1.0.0",
    "mcpTools": "1.0.0",
    "openapi": "1.0.0",
}

prompts = load(ROOT / "contracts/prompts.v1.json")
assert prompts["contractVersion"] == compatibility["contracts"]["prompts"]
by_surface: dict[str, list[dict]] = {}
for prompt in prompts["prompts"]:
    by_surface.setdefault(prompt["surface"], []).append(prompt)
    assert prompt["id"] and prompt["title"] and prompt["template"]
    assert prompt["risk"] in {"read", "proposal", "approval", "authorization", "payment"}
    assert len(prompt["scopes"]) <= 6
assert all(len(items) <= 3 for items in by_surface.values())

onboarding = load(ROOT / "contracts/onboarding.v1.schema.json")
question = onboarding["$defs"]["question"]
assert question["properties"]["choices"]["maxItems"] == 12
assert question["allOf"][0]["if"]["properties"]["id"]["const"] == "agent_client"
assert question["allOf"][0]["else"]["properties"]["choices"]["maxItems"] == 3

mcp_tools = load(ROOT / "contracts/mcp-tools.v1.json")
assert mcp_tools["contractVersion"] == compatibility["contracts"]["mcpTools"]
assert len({tool["name"] for tool in mcp_tools["tools"]}) == len(mcp_tools["tools"])

openapi = load(ROOT / "contracts/openapi.v1.json")
assert openapi["openapi"] == "3.1.0"
assert openapi["info"]["version"] == compatibility["contracts"]["openapi"]

for private_path in [PLUGIN / "src", PLUGIN / "openclaw.plugin.json", PLUGIN / "package.json"]:
    assert not private_path.exists(), f"private OpenClaw runtime material must not be public: {private_path}"

print("Plugin manifests, marketplaces, MCP configuration, and privacy boundary are valid.")
