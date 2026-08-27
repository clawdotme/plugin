#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Validate the public plugin package without importing executable plugin code."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT
REPOSITORY = "https://github.com/clawdotme/plugin"
MCP_URL = "https://claw.me/api/v1/mcp"
TEXT_SUFFIXES = {".md", ".json", ".py", ".sh", ".toml", ".txt", ".yml", ".yaml"}


class ValidationError(RuntimeError):
    """A stable, user-facing validation failure."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def load(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValidationError(f"invalid JSON in {path.relative_to(ROOT)}: {exc}") from exc
    require(isinstance(value, dict), f"{path.relative_to(ROOT)} must contain a JSON object")
    return value


def validate_required_files() -> None:
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
        ROOT / "tools/package.json",
        ROOT / "tools/pnpm-lock.yaml",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
    require(not missing, f"missing required files: {', '.join(missing)}")


def validate_license() -> None:
    license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
    require(license_text.startswith("MIT License\n"), "LICENSE must contain the MIT license text")
    require("Copyright (c) 2026 Claw Me" in license_text, "LICENSE copyright is missing")


def validate_secret_hygiene() -> None:
    secret_patterns = {
        "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
        "Stripe live key": re.compile(r"\b[rs]k_live_[A-Za-z0-9]{16,}\b"),
        "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
        "Slack token": re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b"),
        "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
        "Google API key": re.compile(r"\bAIza[0-9A-Za-z_-]{30,}\b"),
    }
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or "node_modules" in path.parts:
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        content = path.read_text(encoding="utf-8")
        for label, pattern in secret_patterns.items():
            require(pattern.search(content) is None, f"{label} found in {path.relative_to(ROOT)}")


def validate_manifests(compatibility: dict[str, Any]) -> None:
    version = str(compatibility.get("pluginVersion", ""))
    require(bool(re.fullmatch(r"\d+\.\d+\.\d+", version)), "compatibility pluginVersion must be semver")
    manifests = [
        load(PLUGIN / ".codex-plugin/plugin.json"),
        load(PLUGIN / ".claude-plugin/plugin.json"),
        load(PLUGIN / ".cursor-plugin/plugin.json"),
        load(PLUGIN / ".plugin/plugin.json"),
    ]
    for manifest in manifests:
        require(manifest.get("name") == "claw-me", "plugin manifest name must be claw-me")
        require(manifest.get("version") == version, "plugin manifest version drifted from compatibility.json")
        require(manifest.get("repository") == REPOSITORY, "plugin manifest repository is incorrect")
        require("[TODO:" not in json.dumps(manifest), "plugin manifest contains an unresolved TODO")

    codex_marketplace = load(ROOT / ".agents/plugins/marketplace.json")
    require(codex_marketplace.get("name") == "claw-me", "Codex marketplace name must be claw-me")
    plugins = codex_marketplace.get("plugins")
    require(isinstance(plugins, list) and len(plugins) == 1, "Codex marketplace must contain one plugin")
    entry = plugins[0]
    require(entry.get("name") == "claw-me", "Codex marketplace plugin name is incorrect")
    require(entry.get("source") == {"source": "local", "path": "./"}, "Codex marketplace source is incorrect")
    require(
        entry.get("policy") == {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
        "Codex marketplace policy is incorrect",
    )
    require(entry.get("category") == "Productivity", "Codex marketplace category is incorrect")

    claude_marketplace = load(ROOT / ".claude-plugin/marketplace.json")
    claude_plugins = claude_marketplace.get("plugins")
    require(isinstance(claude_plugins, list) and len(claude_plugins) == 1, "Claude marketplace must contain one plugin")
    require(claude_plugins[0].get("source") == "./", "Claude marketplace source is incorrect")


def validate_contracts(compatibility: dict[str, Any]) -> None:
    mcp = load(PLUGIN / ".mcp.json")
    require(mcp == {"mcpServers": {"claw-me": {"type": "http", "url": MCP_URL}}}, "MCP configuration drifted")
    service = compatibility.get("service", {})
    require(service.get("mcpUrl") == MCP_URL, "compatibility MCP URL is incorrect")
    contract_versions = compatibility.get("contracts")
    require(
        contract_versions == {
            "onboarding": "1.0.0",
            "prompts": "1.0.0",
            "mcpTools": "1.0.0",
            "openapi": "1.0.0",
        },
        "compatibility contract versions are incorrect",
    )

    prompts = load(ROOT / "contracts/prompts.v1.json")
    require(prompts.get("contractVersion") == contract_versions["prompts"], "prompt contract version drifted")
    by_surface: dict[str, list[dict[str, Any]]] = {}
    prompt_items = prompts.get("prompts")
    require(isinstance(prompt_items, list), "prompt contract must contain a prompts array")
    for prompt in prompt_items:
        require(isinstance(prompt, dict), "each prompt must be an object")
        surface = prompt.get("surface")
        require(isinstance(surface, str) and surface, "each prompt must have a surface")
        by_surface.setdefault(surface, []).append(prompt)
        require(bool(prompt.get("id") and prompt.get("title") and prompt.get("template")), "prompt fields are incomplete")
        require(prompt.get("risk") in {"read", "proposal", "approval", "authorization", "payment"}, "prompt risk is invalid")
        require(isinstance(prompt.get("scopes"), list) and len(prompt["scopes"]) <= 6, "prompt scopes are invalid")
    require(all(len(items) <= 3 for items in by_surface.values()), "a surface exposes more than three prompts")

    onboarding = load(ROOT / "contracts/onboarding.v1.schema.json")
    try:
        question = onboarding["$defs"]["question"]
        max_agent_choices = question["properties"]["choices"]["maxItems"]
        agent_question_id = question["allOf"][0]["if"]["properties"]["id"]["const"]
        max_other_choices = question["allOf"][0]["else"]["properties"]["choices"]["maxItems"]
    except (KeyError, IndexError, TypeError) as exc:
        raise ValidationError("onboarding question schema is incomplete") from exc
    require(max_agent_choices == 12, "agent connection catalog must allow up to twelve clients")
    require(agent_question_id == "agent_client", "agent connection catalog exception targets the wrong question")
    require(max_other_choices == 3, "ordinary onboarding questions must allow no more than three choices")

    mcp_tools = load(ROOT / "contracts/mcp-tools.v1.json")
    require(mcp_tools.get("contractVersion") == contract_versions["mcpTools"], "MCP tool contract version drifted")
    tools = mcp_tools.get("tools")
    require(isinstance(tools, list), "MCP tool contract must contain a tools array")
    names = [tool.get("name") for tool in tools if isinstance(tool, dict)]
    require(len(names) == len(tools) == len(set(names)), "MCP tool names must be present and unique")

    openapi = load(ROOT / "contracts/openapi.v1.json")
    require(openapi.get("openapi") == "3.1.0", "OpenAPI document must use 3.1.0")
    require(openapi.get("info", {}).get("version") == contract_versions["openapi"], "OpenAPI version drifted")


def validate_privacy_boundary() -> None:
    for private_path in (PLUGIN / "src", PLUGIN / "openclaw.plugin.json", PLUGIN / "package.json"):
        require(not private_path.exists(), f"private OpenClaw runtime material must not be public: {private_path}")


def validate_ci_pinning() -> None:
    workflow = (ROOT / ".github/workflows/validate.yml").read_text(encoding="utf-8")
    action_refs = re.findall(r"uses:\s*([^\s#]+)", workflow)
    require(bool(action_refs), "validation workflow does not use any actions")
    for action_ref in action_refs:
        _, separator, revision = action_ref.rpartition("@")
        require(separator == "@" and bool(re.fullmatch(r"[0-9a-f]{40}", revision)), f"CI action is not SHA-pinned: {action_ref}")


def main() -> None:
    validate_required_files()
    validate_license()
    validate_secret_hygiene()
    compatibility = load(ROOT / "compatibility.json")
    validate_manifests(compatibility)
    validate_contracts(compatibility)
    validate_privacy_boundary()
    validate_ci_pinning()
    print("Plugin manifests, contracts, CI pinning, secret hygiene, and privacy boundary are valid.")


if __name__ == "__main__":
    try:
        main()
    except ValidationError as exc:
        raise SystemExit(f"validation failed: {exc}") from exc
