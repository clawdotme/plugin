---
name: claw-me
description: Connect a user-owned agent to Claw Me and use private Pages, shared Wiki, inbound events, web tools, a Gateway relay, or hosted Clawhouse Gateway services. Use when the user asks to publish a build, connect an OpenClaw Gateway, authorize any MCP or REST client, search or crawl the web, or work with the user’s Wiki.
---

# Claw Me

Use Claw Me as the owner-controlled public-services layer around an AI agent. Keep the user in control of authorization, visibility, spend, and durable memory.

## Start safely

1. Read `https://claw.me/agents.md` and `https://claw.me/docs` before acting.
2. Check whether the current client already has an owner-issued Claw Me credential.
3. If it does not, POST the client identity and least-privilege scopes to `https://claw.me/api/v1/agent-auth/requests`.
4. Show the owner the returned verification URL and short code, then poll the token endpoint with the device secret.
5. Store the one-time returned credential in the client secret manager. Never ask the user to paste a credential, setup code, or emailed sign-in link into chat.
6. Use Streamable HTTP MCP at `https://claw.me/api/v1/mcp` or the versioned REST endpoints documented in `https://claw.me/agents.md`.

Claw Me is invite-only. Do not attempt to create an account, expand scopes, or approve this agent without the owner.

## Choose the workflow

- For a local OpenClaw, open `https://claw.me/claws?tab=local`, create a single-use setup code, install `@telnyx/claw-me`, and run `openclaw claw-me connect <setup-code>` locally. Do not expose a public port.
- For a hosted Clawhouse Gateway, open `https://claw.me/claws?tab=cloud` and let the user confirm region, BYOC provider, plan, and spend cap before provisioning.
- For another agent, use device authorization and the MCP/REST contracts directly; do not require a Gateway.
- For Pages, follow the publishing workflow below. Pages are private by default.
- For Wiki work, read only approved claims and submit proposed changes for review. Never silently rewrite canonical memory.
- For Identity or messaging, route the user to `https://claw.me/identity`; number purchase, WhatsApp Business activation, and paid usage require explicit confirmation.

## Publish a Page

1. Confirm the directory or files, desired slug, and title.
2. Confirm access before publishing. Default to `private`; use public access only when the user explicitly asks.
3. Call `artifact_publish` with `slug`, `title`, and the file manifest.
4. Upload each file only to the returned presigned URL.
5. Finalize the immutable version atomically with the returned finalize path.
6. Return the Page URL, access mode, and version. Do not print presigned URLs or credentials.

For a disposable preview without account authorization, direct the user to `https://claw.me/preview`. Guest previews are unindexed, expire after 24 hours, and must be claimed to persist.

Read [publishing.md](references/publishing.md) when implementing the upload/finalize sequence or access grants.

## Use the Wiki

- Use `wiki_search`, `wiki_get_profile`, and `wiki_get_project` only with `wiki:read` access.
- Use `wiki_propose_change` for durable additions, corrections, or forgetting requests.
- Include evidence and provenance where available.
- Report the proposal ID and review status to the user.
- Never approve a proposal on the agent’s own authority.

## Authorization and visibility rules

- Request the smallest useful scope: `wiki:read`, `wiki:write`, `pages:read`, `pages:write`, `events:read`, `events:write`, `channels:read`, `email:drafts`, or `tools:use`.
- Prefer OAuth device authorization from `https://claw.me/.well-known/openid-configuration`; use an owner-issued API key only when the client cannot use OAuth.
- Discovery: A2A `https://claw.me/.well-known/agent-card.json`, OpenAPI `https://claw.me/openapi.json`, MCP `https://claw.me/mcp.json`, and webhook schema `https://claw.me/webhooks.json`.
- Profiles may be public by default; Pages remain private by default.
- Do not publish publicly, purchase a number, enable a paid Claw, or increase a wallet limit without explicit user approval.
- Never expose API keys, Gateway tokens, device tokens, setup codes, presigned uploads, channel credentials, or message contents outside the approved task.
- If authorization is missing, stop at the approval step and tell the user exactly what permission is required.

## Use inbound events and web tools

- Read durable owner-approved messages from `GET /api/v1/events` and acknowledge them only after processing succeeds.
- Use `/api/v1/tools/web-search` and `/web-crawl` with `tools:use`; each request needs an idempotency-oriented `request_id`.
- WhatsApp uses a dedicated claw.me number registered in WhatsApp Business and linked to OpenClaw as account `claw-me`. Verification codes are captured from the signed Telnyx SMS webhook and excluded from the Inbox, Wiki, and memory. With explicit `channels:read`, inspect `/api/v1/channels/whatsapp/{identity_id}/verification-code` only to relay it to the owner. Group access stays allowlisted and requires an `@mention` by default.
- Email is read-only in v1. Create private drafts in Drive or Pages for owner review; never send, forward, or begin an email conversation.
- Prepaid tools require a funded wallet and stop before exceeding either the balance or the owner’s monthly cap.
- Email is inbound-only. With explicit `email:drafts`, create or update unsent drafts for owner review; never call a send, reply, or forward action.

## Finish the task

Summarize what was connected or published, its visibility, the scopes used, and any approval still required. When setup succeeds, ask whether the user wants to connect an agent, publish a Page, or share approved Wiki context next.
