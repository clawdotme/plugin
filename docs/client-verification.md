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
