# Claw Me Plugin

The official multi-client plugin for [Claw Me](https://claw.me). It gives an owner-approved Agent access to selected Claw Me capabilities through the scoped REST API, agent-first onboarding, A2A discovery, private Pages, reviewed Wiki context, collaborative Drive workspaces, payment proposals, and Sandbox approvals. MCP is available as an optional adapter.

The package is intentionally thin: it bundles portable operating guidance and client-native manifests while the service implementation remains hosted at Claw Me.

## Install

### Codex

```bash
codex plugin marketplace add clawdotme/plugin
codex plugin add claw-me@claw-me
```

Start a new Codex task after installation. Complete the Claw Me authorization flow when prompted.

### Claude Code

```text
/plugin marketplace add clawdotme/plugin
/plugin install claw-me@claw-me
```

Start a new session after installation and approve only the products and permissions the Agent needs.

### Cursor and other Skills clients

```bash
npx skills add clawdotme/plugin --skill claw-me -g
```

The repository also includes Cursor and vendor-neutral plugin manifests plus a hosted MCP configuration. Until a marketplace listing is available, use the Skills install above and connect the MCP endpoint shown below.

### Generic MCP

```json
{
  "mcpServers": {
    "claw-me": {
      "type": "http",
      "url": "https://claw.me/api/v1/mcp"
    }
  }
}
```

Clients that support remote MCP authorization can use the published OAuth metadata. Other clients follow the owner-approved device flow documented at [claw.me/agents.md](https://claw.me/agents.md). Never paste a credential or emailed sign-in link into chat.

### OpenClaw

```bash
openclaw plugins install @telnyx/claw-me
openclaw claw-me connect <one-time-claw-me-setup-code>
```

The OpenClaw runtime package is maintained privately and is not included in this repository.

## Sample prompt

```text
Connect this Agent to Claw Me. Open https://claw.me/connect and follow the guide for this client. Prefer its native clawdotme/plugin installation. If this client has no native plugin, install the shared skill with npx skills add clawdotme/plugin --skill claw-me -g. Request only the permissions needed, send me through Claw Me's owner review, read my Agent Guide through the scoped REST API, and verify a read-only action first. Never ask me to paste an API key, device secret, setup code, or emailed sign-in link into chat.
```

## What the plugin adds

- Scoped REST API at `https://claw.me/api/v1`, described by `https://claw.me/openapi.json`.
- Optional Streamable HTTP MCP adapter at `https://claw.me/api/v1/mcp`.
- A2A discovery at `https://claw.me/.well-known/agent-card.json`.
- Owner-approved, independently selectable access to Pages, Wiki, Drive, inbound events, and owner-only delivery.
- Capability-aware guidance that distinguishes access available now, access needing approval, unavailable account features, and dashboard-only controls.
- Sandbox review for proposed Agent actions, Wiki changes, drafts, and private work.
- Private-by-default publishing and least-privilege authorization guidance.

## Repository layout

- `claw-me/` — canonical public skill bundle.
- `skills/claw-me/` — root Skills CLI compatibility mirror.
- `.codex-plugin/`, `.claude-plugin/`, `.cursor-plugin/`, and `.plugin/` — client-native manifests at the installable repository root.
- `.mcp.json` — hosted Claw Me MCP configuration shared by supported clients.
- `.agents/plugins/marketplace.json` — Codex marketplace.
- `.claude-plugin/marketplace.json` — Claude Code marketplace.
- `compatibility.json` — verified hosted contract and package versions.
- `contracts/` — versioned onboarding, prompt, MCP tool, and OpenAPI contracts consumed by the hosted service.
- `examples/` — sanitized existing-Agent and Managed OpenClaw onboarding transcripts.

## Development

Run the full repository validation before publishing:

```bash
./scripts/validate.sh
```

Live contracts remain authoritative:

- [Agent manifest](https://claw.me/.well-known/agent.json)
- [A2A Agent Card](https://claw.me/.well-known/agent-card.json)
- [MCP discovery](https://claw.me/mcp.json)
- [OAuth metadata](https://claw.me/.well-known/openid-configuration)
- [OpenAPI](https://claw.me/openapi.json)

## License

MIT
