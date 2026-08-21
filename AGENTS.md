# Claw Me Public Skill Repository

Use this file as the operating guide for agents working in the public `clawdotme/skill` repository.

## Contents

- `claw-me/` is the canonical skill bundle for `npx skills add clawdotme/skill --skill claw-me`.
- `skills/claw-me/` is a generated compatibility mirror for Codex and Cursor discovery.
- `.codex-plugin/` and `.cursor-plugin/` contain plugin manifests.
- `assets/` contains public brand assets.

## Source of truth

The public skill is synced from the private Claw Me product repository.

- Agent documentation: https://claw.me/agents.md
- Product documentation: https://claw.me/docs
- MCP discovery: https://claw.me/mcp.json
- OpenAPI discovery: https://claw.me/openapi.json

If local skill text and the live product interfaces disagree, prefer the live interface for current behavior and update this repository promptly.

## Editing rules

- Edit `claw-me/` first, then regenerate `skills/claw-me/` as an exact mirror.
- Keep the skill concise and move implementation detail into `references/`.
- Never commit credentials, setup codes, API keys, device secrets, presigned upload URLs, or private Page and Wiki content.
- Do not claim capabilities that are not present in the live discovery documents.
- Preserve the install command and skill name unless a migration plan is published first.

## Verification

Run:

```bash
./scripts/validate.sh
```
