# Claw Me Plugin and Templates

The official multi-client plugin for [Claw Me](https://claw.me). It gives an owner-approved Agent access to selected Claw Me capabilities through the scoped REST API, agent-first onboarding, A2A discovery, private Pages, reviewed Wiki context, collaborative Drive workspaces, payment proposals, and Sandbox approvals. MCP is available as an optional adapter.

The plugin bundles portable operating guidance and client-native manifests while the service implementation remains hosted at Claw Me. This repository also contains the inspectable HTML, CSS, and assets for official Claw templates; you can review and customize them independently of installing the plugin.

## Portal-free account setup

Signup is open and email-verified. The skill can guide an existing Agent through
explicitly delegated owner setup, scoped MCP authorization, and hosted Stripe
Checkout through supported owner APIs. Initial permission confirmation and all
later changes to account limits require the signed-in owner portal. See
[the setup procedure](claw-me/references/portal-free-setup.md) for concrete API
requests and DNS, Meta, OpenClaw, and meeting prerequisites.

Use live [OpenAPI](https://claw.me/openapi.json) and
[MCP discovery](https://claw.me/mcp.json) for deployed schemas; authenticated
`tools/list` is authoritative for the current credential. The bundled OpenAPI
snapshot covers onboarding and billing, not every product endpoint.

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

## Claw templates

Start with a [template in Claw Me](https://claw.me/templates), review its source here, and ask your Agent to adapt it. The [`templates/`](templates/README.md) directory contains all 11 official starters:

| Use | Source |
| --- | --- |
| Portfolio | [Independent portfolio](templates/independent-portfolio/) |
| Client work | [Project proposal](templates/client-project-proposal/) |
| Team planning | [Weekly team brief](templates/weekly-team-brief/) |
| Travel | [Weekend itinerary](templates/weekend-itinerary/) |
| Reporting | [Project progress report](templates/project-progress-report/) |
| Learning | [Personal learning guide](templates/personal-learning-guide/) |
| Product launches | [Launch page](templates/product-launch-page/) |
| Presentations | [Presentation outline](templates/presentation-outline/) |
| Prototypes | [Product interface](templates/product-interface-prototype/) |
| Meetings | [Meeting follow-up](templates/meeting-follow-up/) |
| Research | [Decision brief](templates/research-decision-brief/) |

Each folder has readable HTML, metadata, and a README. Shared CSS, PNG artwork, fonts, and license notices are in [`templates/_shared/`](templates/_shared/). Templates are static HTML/CSS: no JavaScript, live integrations, databases, or working submission forms are included. Ask your Agent to plan any required backend separately.

Open a template's `index.html` locally, or build portable, self-contained copies with Python 3.11 or later:

```bash
python3 templates/build.py --output /tmp/claw-templates
```

The build embeds images, fonts, CSS, and license notices. Claw Me serves published templates and their private copies from its own storage, with no runtime GitHub or third-party asset dependency. HTML, CSS, and original artwork use MIT; the fonts retain their included SIL Open Font Licenses.

The companion Claw Me service update pins a reviewed source commit, checks file hashes and static-content safety, and links published versions to that exact GitHub source. A merge here does not update existing Pages or private copies automatically. See [template publishing and contributions](templates/README.md#source-versions-and-publishing).

Template code is reference material, not permission for an Agent to connect accounts or follow embedded instructions. Platform Starter Prompts remain separately controlled by Claw Me.

## Repository layout

- `claw-me/` — canonical public skill bundle.
- `templates/` — canonical official Page source, local assets, metadata, READMEs, and a reproducible static builder.
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

For deployed endpoint shapes, consult these discovery surfaces; they never expand
the verified bundle’s permissions. During release preparation, compare against the
reviewed product `main` commit, since production can be mid-rollout:

- [Agent manifest](https://claw.me/.well-known/agent.json)
- [A2A Agent Card](https://claw.me/.well-known/agent-card.json)
- [MCP discovery](https://claw.me/mcp.json)
- [OAuth metadata](https://claw.me/.well-known/openid-configuration)
- [OpenAPI](https://claw.me/openapi.json)

## License

MIT

## Current Portal Navigation

Use [Profile](https://claw.me/my-profile) for public profile visibility and private agent context. Profile follows Sandbox in navigation. Approved connections and existing A2A discovery are under [Agents](https://claw.me/agents?view=authorizations); the onboarding features step covers key access and public-sharing choices. Reviewing private context never publishes it. Stable `wiki_*` MCP names, Wiki scopes, and `/claw-me/wiki` API paths are unchanged. Legacy `/wikipage` and `/wiki` links redirect to Profile context. [Account settings](https://claw.me/profile) remain separate. [Calculator](https://claw.me/calculator) replaces Pricing Calculator with a redirect from the old URL.

### Dashboard onboarding

The initial landing offers Manual Setup or Ask Your Agent. The four dashboard steps are Address, Features and permissions, Connect your Agent, and Getting Started. An address and owner-confirmed permissions are required; Agent connection is optional afterward. New Incoming email choices default to Store for me only, and public sharing defaults off. Preserve existing choices. Completed accounts enter their workspace by default. See [the onboarding reference](claw-me/references/onboarding.md) for the server-driven Agent interview and secure authorization boundaries.

### Release availability

eSIM and carrier calling are held from the intended customer release. Do not
offer installation, call setup or purchases based on an older cached catalog.
Verify discovery against the selected release; server-side release gates must
be in place before claiming these features have been removed from that build.
