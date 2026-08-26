---
name: claw-me
description: Authorize an AI client to use Claw Me and work with private Pages, a shareable Agent Wiki, Drive, Alias email, Meetings, or Managed OpenClaw. Use when the user says “claw me that,” “claw my meeting,” asks to save or publish work, authorize an MCP or REST client, or work with the user’s Wiki.
---

# Claw Me

Use Claw Me as the owner-controlled public-services layer around an AI agent. Keep the user in control of authorization, visibility, spend, and durable memory.

## Start safely

1. Read `https://claw.me/agents.md` and `https://claw.me/docs` before acting.
2. Check whether the current client already has an owner-issued Claw Me credential.
3. If it does not, ask for the owner's Claw Me email address and POST it as `owner_email` with the client identity and least-privilege scopes to `https://claw.me/api/v1/agent-auth/requests`. Use OAuth `login_hint` when the client supports device authorization.
4. Tell the owner to check for an email from `noreply@claw.me` and review the Agent in Claw Me. Show the returned verification URL only when email delivery was not requested, then poll the token endpoint with the device secret.
5. Store the one-time returned credential in the client secret manager. Never ask the user to paste a credential, setup code, or emailed sign-in link into chat.
6. Use Streamable HTTP MCP at `https://claw.me/api/v1/mcp` or the versioned REST endpoints documented in `https://claw.me/agents.md`.

Claw Me is invite-only. Do not attempt to create an account, expand scopes, or approve this agent without the owner.

## Choose the workflow

- For Managed OpenClaw, open `https://claw.me/claws`. It is one managed runtime size, requires Basic or Plus plus the Managed Claw add-on, and uses centrally managed hosting placement. Configure the model provider directly inside OpenClaw; Claw Me does not receive or bill its credentials or traffic.
- For another AI client, use owner-approved device authorization and the MCP/REST contracts directly. Claw Me deliberately does not request write access to a local Gateway.
- For Pages, follow the publishing workflow below. Pages are private by default.
- For Wiki work, read only approved claims and submit proposed changes for review. Never silently rewrite canonical memory.
- For Alias or WhatsApp Business, route the user to `https://claw.me/alias`; number purchase, activation, and paid usage require explicit confirmation.
- For meetings, confirm the meeting URL, recording consent, destination Agent, and recording-retention choice before scheduling. Results are private in Drive by default.

## Understand natural phrases

- Treat “claw me that,” “claw this,” “save this to Claw Me,” and similar wording as intent to save or publish the current Agent work. Confirm the files, title, slug, and access before publishing.
- Treat “claw my meeting,” “claw this meeting,” “take notes at my meeting,” and similar wording as intent to schedule Claw Meetings. Ask for the meeting URL and confirm participant consent, destination Agent, timing, and recording retention before scheduling.
- Treat “save this to my Drive” as intent to store the current file privately in Claw Me Drive.
- Treat “update my Agent Wiki” as intent to propose an owner-reviewed Wiki change, never to alter approved knowledge directly.

These are natural-language aliases, not exact commands. Infer the workflow from the user’s intent, but retain every approval and privacy boundary below.

## Publish a Page

1. Confirm the directory or files, desired slug, and title.
2. Confirm access before publishing. Default to `private`; use public access only when the user explicitly asks.
3. Call `artifact_publish` with `slug`, `title`, and the file manifest.
4. Upload each file only to the returned presigned URL.
5. Finalize the immutable version atomically with the returned finalize path.
6. Return the Page URL, access mode, and version. Do not print presigned URLs or credentials.

For a disposable preview without account authorization, direct the user to `https://claw.me/preview`. Guest previews are unindexed, expire after 24 hours, and must be claimed to persist.

Read [publishing.md](references/publishing.md) when implementing the upload/finalize sequence or access grants.

## Use the workspace

- Put durable, browser-viewable output in a Page and supporting files in Drive. Every file belongs to a Page, and every publish or upload creates an immutable version rather than changing files in place.
- Pages start private. The owner may make one public, grant access to exact Claw Me accounts or an email domain, add a password, or create an expiring review link. Guest previews expire after 24 hours; publishing another version does not reset that clock.
- Use Site Data for lightweight forms, waitlists, comments, or shared Page state. Creating a collection, enabling public writes, changing a schema, or deleting records requires explicit owner confirmation.
- Treat Domains, Variables, Analytics, and Functions as owner-controlled workspace settings. Guide the owner to the Page dashboard when the current authorization surface does not expose a required control.
- Never ask for a DNS credential, certificate private key, or Variable value in chat. Variables are encrypted, classified as secret/private/public, and their plaintext is not returned after creation; keep values out of Page bundles.
- Describe Analytics as cookie-free, first-party Page traffic reporting. Do not claim Claw Me retains visitor IP addresses or exposes analytics through MCP unless the current contract says so.
- Do not promise a general serverless runtime. Functions currently organize routes, schedules, deployments, Variables, and Secrets; use only controls documented by the live dashboard or API.

Read [workspace.md](references/workspace.md) when deciding where work belongs, applying sharing rules, or guiding an owner through Pages, Drive, Domains, Variables, Analytics, or Functions.

## Use the Wiki

- Search with `wiki_search`, `wiki_get_profile`, and `wiki_get_project` before work that could benefit from approved preferences, people, projects, constraints, or decisions. Pending proposals are not facts.
- Cite the approved claims that materially shaped the result. Surface conflicts, stale facts, and evidence gaps rather than guessing.
- Propose only durable knowledge likely to help in future conversations. Do not turn transcripts, temporary tasks, conversational filler, inferred traits, credentials, message bodies, or sensitive personal data into memory by default.
- Use `wiki_propose_change` for additions, corrections, and forgetting requests. Include provenance, evidence, rationale, and the replaced claim when applicable.
- Report the proposal ID and say that it is waiting for owner review. Never approve a proposal on the agent’s own authority.
- If “remember this” could mean a Wiki claim, Drive file, Page, task, or temporary chat context, ask one focused destination question before writing.

## Authorization and visibility rules

- Request the smallest useful scope: `wiki:read`, `wiki:write`, `pages:read`, `pages:write`, `events:read`, `events:write`, `channels:read`, `email:drafts`, or `email:owner`.
- Prefer OAuth device authorization from `https://claw.me/.well-known/openid-configuration`; use an owner-issued API key only when the client cannot use OAuth.
- Discovery: A2A `https://claw.me/.well-known/agent-card.json`, OpenAPI `https://claw.me/openapi.json`, MCP `https://claw.me/mcp.json`, and webhook schema `https://claw.me/webhooks.json`.
- Profiles and Pages remain private unless the owner deliberately shares or publishes them.
- Do not publish publicly, purchase a number, enable Managed OpenClaw, or increase a wallet limit without explicit user approval.
- Never expose API keys, Gateway tokens, device tokens, setup codes, presigned uploads, channel credentials, or message contents outside the approved task.
- If authorization is missing, stop at the approval step and tell the user exactly what permission is required.

## Use inbound events

- Read durable owner-approved messages from `GET /api/v1/events` and acknowledge them only after processing succeeds.
- WhatsApp uses a dedicated claw.me number registered in WhatsApp Business and linked to OpenClaw as account `claw-me`. Verification codes are captured from the signed Telnyx SMS webhook and excluded from the Inbox, Wiki, and memory. With explicit `channels:read`, inspect `/api/v1/channels/whatsapp/{identity_id}/verification-code` only to relay it to the owner. Group access stays allowlisted and requires an `@mention` by default.
- With explicit `email:drafts`, create or update unsent drafts for owner review.
- With explicit `email:owner`, send through `POST /api/v1/email/owner?identity_id=...`. Supply only `subject`, `text_body` or `html_body`, and optional labels or tags. The service derives the verified workspace owner as the sole recipient.
- Never attempt to add `to`, `cc`, or `bcc`, send to a third party, forward a message, or turn owner delivery into a campaign. Sent and received messages share the workspace's monthly email allowance.

## Use Meetings and the USD wallet

- With the appropriate owner-issued scope, Claw Meetings may join Zoom, Google Meet, Microsoft Teams, or Webex and save a transcript, summary, action items, and optional recording privately in Drive.
- Paid plans consume monthly meeting, email, and storage allowances first. Additional usage draws from the owner's closed-loop USD wallet at fixed public rates.
- You may read and report available capacity. Never load wallet funds, enable auto-reload, change its threshold, or raise a monthly spend cap without explicit owner approval.

## Finish the task

Summarize what was connected or published, its visibility, the scopes used, and any approval still required. When setup succeeds, ask whether the user wants to connect an agent, publish a Page, or share approved Wiki context next.
