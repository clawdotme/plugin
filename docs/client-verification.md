# Verify a Claw Me client installation

A native plugin bundles the skill and MCP configuration. A Skills CLI installation supplies instructions; it does not itself establish a connection or authorize an account. REST clients can use the documented device flow independently of MCP.

## First successful session

1. Follow the installation instructions in the root README for the selected client. Start a new task/session so the client discovers the installed skill.
2. Check the client exposes `claw-me` and, for an MCP installation, the configured server URL is `https://claw.me/api/v1/mcp`. Do not register a second connection just because the first needs authorization.
3. Complete the owner authorization workflow from the bundled skill. Reuse an existing appropriate credential; never paste secrets into the conversation.
4. Inspect authenticated tools and granted scopes. Ask: “Show which Claw Me capabilities this Agent can access.” A successful read establishes connectivity; an install success message does not.
5. If `wiki:read` is granted and `wiki_get_agent_guide` is present, read the guide. Otherwise choose an available read operation relevant to the user's task.
6. Report the client, plugin version, successful operation, and remaining access limitation. Redact tokens, email contents, and private context from any shared diagnostic report.

## Troubleshooting

| Symptom | Next check |
| --- | --- |
| Skill missing | Confirm the installation scope and start a new session. For source validation run `./scripts/validate.sh`. |
| Skill present, MCP absent | A skill-only install needs a separately configured MCP connection if that adapter is desired. Use the README configuration; REST remains supported. |
| Authorization expired or rejected | Use the client's supported reconnect flow and owner review. Do not guess tokens or repeatedly create authorizations. |
| Read works, requested tool absent | Compare the granted scope and product availability. Ask only for access needed for the task; account features are not implied by installation. |
| Email missing | Only released mail is Agent-visible. Opening mail in the owner UI does not release it. |
| Send/reply unavailable | Third-party delivery and replies are disabled at launch. Do not substitute another provider or ask for its credentials. |
| Write timed out | Follow the bundled recovery reference; inspect operation state before retrying a mutation. |
| Manifest verification fails | Stop using that bundle; obtain an intact reviewed release and verify it. Do not edit hashes to bypass verification. |

## Release evidence

Repository validation checks packaging and discovery, not authenticated behavior in every client. Before claiming a client is tested, record its version, operating system, plugin source commit, installation method, skill discovery result, authorization result, and one successful scoped read. Use a test account and retain sanitized evidence. A manifest-supported client without such evidence should be described as manifest-supported.

## Hermes Agent

### Hermes Agent

Hermes Agent from Nous Research learns from repeated work. Connect it to Claw Me to keep finished Pages and approved project context alongside the Agent you already use.

[Official documentation](https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp) · [Claw Me guide](https://claw.me/plugins/hermes)

```bash
hermes mcp add claw-me --url https://claw.me/api/v1/mcp --auth oauth
```

Use Hermes’s documented remote MCP setup. Complete owner authorization in Claw Me; a live Claw Me session has not yet been verified.

Starter prompt:

```text
I use Hermes Agent. Follow the verified claw-me skill and https://claw.me/plugins/hermes. Check supported tools before installing anything. Reuse an authorized connection or complete owner authorization for only the permissions needed. Never request secrets in chat. Turn our completed research into a private project brief on Claw Me. Include sources, decisions, and next steps. Verify the result and explain any unsupported capability.
```

## Meta Agents

### Muse

Muse is Meta’s personal agent, running in a dedicated virtual environment. Prepare useful project summaries and use Claw Me as a private destination when Muse exposes an approved connection.

[Official documentation](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/) · [Claw Me guide](https://claw.me/plugins/muse)

Check your Muse account’s supported integrations and tools. Review https://github.com/clawdotme/plugin/tree/main/claw-me before connecting.

Muse is separate from the Muse Code terminal agent. No native Claw Me plugin or live connection is verified. Do not assume shell access or install terminal software into the personal agent. If custom connections are unavailable, prepare the output for another supported client.

Starter prompt:

```text
I use Muse. Follow the verified claw-me skill and https://claw.me/plugins/muse. Check available tools before configuring a connection. Reuse authorized access or complete owner authorization for only the required permissions. Never request secrets in chat. Turn our project conversation into a private brief with decisions, open questions, and next steps. Save privately only through an available authorized tool; otherwise prepare the files and explain the missing capability.
```

### Muse Code

Muse Code is Meta’s terminal coding agent. Use Claw Me to keep project briefs, release summaries, and finished static pages alongside the repository work.

[Official documentation](https://dev.meta.ai/docs/muse-code) · [Claw Me guide](https://claw.me/plugins/muse-code)

Review the shared skill at https://github.com/clawdotme/plugin/tree/main/claw-me. Follow https://dev.meta.ai/docs/muse-code for the installed client’s supported skill and connection configuration.

Meta confirms Muse Code as a terminal coding agent. Its developer documentation requires login, so no native Claw Me installation command or live connection is verified. Use the shared skill only through supported file access and HTTPS or MCP tools.

Starter prompt:

```text
I use Muse Code. Follow the verified claw-me skill and https://claw.me/plugins/muse-code. Check available tools before configuring a connection. Reuse authorized access or complete owner authorization for only the required permissions. Never request secrets in chat. Create a private release handoff from the current repository changes, including validation results and remaining limitations. Save privately only through an available authorized tool; otherwise prepare the files and explain the missing capability.
```

## Claws

OpenClaw, AutoClaw, NemoClaw, ZeroClaw, NanoClaw, PicoClaw, Kimi Claw, and TrustClaw are grouped here for discovery. A shared name does not imply binary or plugin compatibility. The root README contains the existing OpenClaw package instructions.

### ZeroClaw

ZeroClaw runs as a Rust binary on your own machine. Use Claw Me for private project output without adding a local storage service to your Agent.

[Official documentation](https://github.com/zeroclaw-labs/zeroclaw) · [Claw Me guide](https://claw.me/plugins/zeroclaw)

```text
Review the shared claw-me skill at https://github.com/clawdotme/plugin/tree/main/claw-me. Configure a supported HTTP tool or remote MCP connection for your installed ZeroClaw version.
```

Compatibility guide; no native ZeroClaw package or live connection is verified. Keep network allowlists and deny-by-default policies in place.

Starter prompt:

```text
I use ZeroClaw. Follow the verified claw-me skill and https://claw.me/plugins/zeroclaw. Check supported tools before installing anything. Reuse an authorized connection or complete owner authorization for only the permissions needed. Never request secrets in chat. Prepare a private status page from the approved project files. Use only explicitly allowed network destinations and report any blocked operation. Verify the result and explain any unsupported capability.
```

### NanoClaw

NanoClaw uses Anthropic’s Agent SDK with agents running in containers. Keep that isolation while saving approved output to Claw Me. Containers reduce exposure; they do not guarantee protection from prompt injection.

[Official documentation](https://github.com/nanocoai/nanoclaw) · [Claw Me guide](https://claw.me/plugins/nanoclaw)

```text
Review the shared claw-me skill at https://github.com/clawdotme/plugin/tree/main/claw-me. Make it available only to the intended NanoClaw agent using your deployment’s supported configuration.
```

Compatibility guide; no native NanoClaw package or live connection is verified. The agent container needs an approved HTTP or MCP path and secure credential injection. Do not mount the host home directory to make setup work.

Starter prompt:

```text
I use NanoClaw. Follow the verified claw-me skill and https://claw.me/plugins/nanoclaw. Check supported tools before installing anything. Reuse an authorized connection or complete owner authorization for only the permissions needed. Never request secrets in chat. Create a private handoff page from this agent’s approved workspace. Exclude other agents’ files and keep the container boundary intact. Verify the result and explain any unsupported capability.
```

### PicoClaw

PicoClaw is a Go-based assistant designed for lightweight and edge deployments. Send a concise report to Claw Me while keeping device control in your existing setup.

[Official documentation](https://github.com/sipeed/picoclaw) · [Claw Me guide](https://claw.me/plugins/picoclaw)

```text
Review the shared claw-me skill at https://github.com/clawdotme/plugin/tree/main/claw-me. Use a supported HTTPS tool or MCP transport available in your PicoClaw build.
```

Compatibility guide; no native PicoClaw package or live connection is verified. Check your build’s transport support and available memory. An edge device does not need Node.js just to read the shared instructions.

Starter prompt:

```text
I use PicoClaw. Follow the verified claw-me skill and https://claw.me/plugins/picoclaw. Check supported tools before installing anything. Reuse an authorized connection or complete owner authorization for only the permissions needed. Never request secrets in chat. Prepare a private weekly summary from the device readings I provide. Highlight missing readings and unusual values without changing device settings. Verify the result and explain any unsupported capability.
```

### Kimi Claw

Kimi Claw brings OpenClaw conversations into Kimi. Prepare project briefs and finished pages in that workflow, then use Claw Me when your environment exposes an approved connection.

[Official documentation](https://www.kimi.com/en/help/kimi-claw/overview) · [Claw Me guide](https://claw.me/plugins/kimi-claw)

```text
Check whether your Kimi Claw environment supports custom skills and outbound HTTPS or remote MCP. Read https://github.com/clawdotme/plugin/tree/main/claw-me before configuring a connection.
```

Compatibility guide; hosted Kimi Claw access does not imply shell access or permission to install an OpenClaw package. No live Claw Me connection is verified. If custom tools are unavailable, prepare the output and use another supported client to upload it.

Starter prompt:

```text
I use Kimi Claw. Follow the verified claw-me skill and https://claw.me/plugins/kimi-claw. Check supported tools before installing anything. Reuse an authorized connection or complete owner authorization for only the permissions needed. Never request secrets in chat. Turn this conversation into a project handoff with decisions, open questions, and next steps. Save privately to Claw Me if authorized tools are available; otherwise prepare the files and explain the missing connection. Verify the result and explain any unsupported capability.
```

### TrustClaw

TrustClaw combines Composio-managed integrations with sandboxed execution. Use Claw Me as a destination for reviewed project output when your deployment supports a custom connection.

[Official documentation](https://github.com/ComposioHQ/trustclaw) · [Claw Me guide](https://claw.me/plugins/trustclaw)

```text
Ask your deployment administrator to configure an approved Claw Me HTTPS or MCP tool using https://github.com/clawdotme/plugin/tree/main/claw-me.
```

Compatibility guide; no native TrustClaw package, Composio catalog listing, or live Claw Me connection is verified. Existing OAuth connections to other services do not authorize Claw Me. Keep credentials in the deployment’s managed secret storage.

Starter prompt:

```text
I use TrustClaw. Follow the verified claw-me skill and https://claw.me/plugins/trustclaw. Check supported tools before installing anything. Reuse an authorized connection or complete owner authorization for only the permissions needed. Never request secrets in chat. Draft a private weekly operations brief using only my connected, approved sources. Identify source gaps and save to Claw Me only if the deployment exposes an authorized tool. Verify the result and explain any unsupported capability.
```
