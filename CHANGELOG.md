# Changelog

## 0.3.4 — 2026-08-27

- Make plugin validation reproducible with a locked Skills CLI toolchain.
- Pin every GitHub Action by immutable commit and disable persisted checkout credentials.
- Replace assertion-only checks with explicit contract, secret-hygiene, CI, and privacy-boundary validation.
- Add a canonical skill sync command so the compatibility mirror cannot be edited independently.

## 0.3.3 — 2026-08-27

- Establish the scoped REST API and OpenAPI contract as the primary Agent integration.
- Add a lightweight ETag-based Wiki revision check and a human prompt for one daily, deduplicated Agent refresh job.
- Keep MCP available as an optional compatibility adapter.

## 0.3.2 — 2026-08-27

- Mirror all six supported connection paths in the onboarding client catalog.
- Keep the three-choice interview limit while allowing the connection catalog to show every supported client.

## 0.3.1 — 2026-08-27

- Add contextual Agent prompts for Page analytics, Meetings, and Functions.
- Keep channel prompts aligned with the Address and communications control surface.

## 0.3.0 — 2026-08-27

- Publish the agent-first onboarding, contextual prompt, MCP tool, and OpenAPI contracts.
- Add existing-Agent and paid Managed OpenClaw onboarding guidance and examples.
- Document owner-only approvals, payment boundaries, bootstrap inference limits, and recovery.
- Add security, contribution, and third-party notice documents while retaining MIT licensing.

## 0.2.0 — 2026-08-26

- Rename the public distribution repository to `clawdotme/plugin`.
- Add repository marketplaces for Codex and Claude Code.
- Add Codex, Claude Code, Cursor, and vendor-neutral plugin manifests.
- Bundle the hosted Claw Me MCP connection and current public skill.
- Document A2A discovery, collaborative Drive workspaces, and Sandbox review.
- Keep the private OpenClaw runtime outside this public repository.

## 0.1.0

- Publish the initial Claw Me Agent Skill.
