# Claw Me

The public agent skill for [Claw Me](https://claw.me): connect user-owned agents to private Pages, shared Wiki context, inbound events, web tools, and local or hosted OpenClaw Gateways.

## Install

```bash
npx skills add clawdotme/skill --skill claw-me -g
```

To install only for the current project, omit `-g`.

Or install the hosted skill without npm:

```bash
curl -fsSL https://claw.me/install.sh | bash
```

After installation, ask your agent to use `$claw-me`.

## What the skill does

- Connects Codex, Claude, Gemini, OpenClaw, CI jobs, and custom agents through owner-approved MCP or REST authorization.
- Publishes private-by-default Pages using immutable upload and finalize workflows.
- Reads approved Wiki context and proposes durable changes for owner review.
- Handles inbound events and prepaid web tools within user-controlled scopes and spend limits.
- Connects a private local OpenClaw Gateway or provisions an optional hosted Clawhouse Gateway.

Current agent documentation is available at [claw.me/agents.md](https://claw.me/agents.md).

## Repository layout

- `claw-me/` — canonical skill bundle used by `npx skills add`.
- `skills/claw-me/` — generated compatibility mirror for Codex and Cursor plugin discovery.
- `.codex-plugin/` and `.cursor-plugin/` — plugin metadata.

## License

MIT
