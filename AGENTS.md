# Claw Me Public Plugin Repository

Use this file as the operating guide for agents working in the public `clawdotme/plugin` repository.

## Contents

- `claw-me/` is the canonical public skill bundle for `npx skills add clawdotme/plugin --skill claw-me`.
- `skills/claw-me/` is the root Skills CLI compatibility mirror.
- The repository root is the installable multi-client plugin package.
- `.agents/plugins/marketplace.json` and `.claude-plugin/marketplace.json` are the repository marketplaces.
- `assets/` contains public brand assets.
- `templates/` is the canonical source of official static Claw templates; follow its README and run its builder before submitting changes.

## Public repository scope

Only publish material needed to install, use, understand, or maintain the Claw Me skill/plugin: skill instructions and references, client manifests, public API contracts, sanitized usage examples, public Page templates and their assets, licenses, and validation tooling.

Competitive research, distribution strategy, internal audits, incident reports, deployment runbooks, customer information, and product planning belong in the internal product repository. Do not put them in public files, issues, PR descriptions, comments, or release notes. Public templates must use synthetic examples, not internal working documents.

`docs/` contains only explicitly approved user guides listed by `validate_public_scope` in `scripts/validate.py`. Adding a guide requires reviewing its purpose and updating that allowlist in the same change. Passing the path check does not replace reviewing the contents for public suitability.

## Source of truth

The public skill is synced from the private Claw Me product repository.

- Agent documentation: https://claw.me/agents.md
- Product documentation: https://claw.me/docs
- MCP discovery: https://claw.me/mcp.json
- OpenAPI discovery: https://claw.me/openapi.json

Use the reviewed product `main` commit as the source for release preparation; production may be on an older or mixed revision during rollout. Record both repository SHAs. For a deployed client, authenticated discovery describes the tools actually available, but it never expands the verified skill bundle’s permissions, destinations, approval rules, or secret policy. Resolve discrepancies before claiming compatibility.

## Editing rules

- Sync `claw-me/` from the private product repository, then regenerate `skills/claw-me/` exactly.
- Keep all plugin manifests on the version declared in `compatibility.json`.
- Keep the skill concise and move implementation detail into `references/`.
- Never commit credentials, setup codes, API keys, device secrets, presigned upload URLs, or private Page and Wiki content.
- Never copy the private OpenClaw runtime package or source into this repository.
- Do not claim capabilities that are not present in the live discovery documents.
- Preserve the `claw-me` plugin and marketplace names unless a migration plan is published first.

## Verification

Run:

```bash
./scripts/validate.sh
```
