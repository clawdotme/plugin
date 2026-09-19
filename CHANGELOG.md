## 0.7.8 — 2026-09-19

- Remove the paused hosted-Agent offer and onboarding example from current setup guidance.
- Sync skill 1.4.0, including explicit owner approval for public/private account changes; no additional plugin permissions are requested.

## 0.7.7 — 2026-09-16

- Clarify signup and email verification before account authorization.
- Explain that users publish through their own account without domain ownership.
- Keep anonymous 24-hour previews independent of signup and pairing.
- Check email delivery status before telling users to wait for an approval email.
- Sync skill 1.3.7; no additional permissions are requested.

## 0.7.6 — 2026-09-16

- Replace the retired Clawhouse plugin logo with the orange Claw Me mark.
- Align the Codex brand color with the Claw Me icon.

## 0.7.5 — 2026-09-15

- Sync skill 1.3.5 from product main.
- Honor explicit anonymous publishing even when an account key exists.
- Keep claim responses private and return completed URLs without blocking on browser setup.

## 0.7.4 — 2026-09-14

- Sync skill 1.3.4 with account approval guidance and delegated account setup instructions.
- Explain remote MCP OAuth setup alongside plugin installation and portal setup.
- Clarify that approving Agent access and signing in to the dashboard are separate actions.

## 0.7.3 — 2026-09-14

- Provide executable Claude Code plugin installation commands alongside interactive slash commands.
- Make the connection prompt a read-only setup check with a concrete scope and verification tool.
- Shorten the sample setup request and keep account authorization separate from optional data access.

## 0.7.2 — 2026-09-12

- Sync skill 1.3.2 so an explicit anonymous preview request takes precedence over existing account credentials.
- Document anonymous mode in the OpenClaw publishing tool and the Python helper fallback for older installations.
- Preserve the 24-hour expiry and existing storage limits; clarify disposable-preview date handling.

## 0.7.1 — 2026-09-11

- Explain Free with optional usage billing; signup still needs no credit card.
- Preserve the Free allowance when billing is enabled and distinguish card setup from wallet spending authorization.
- Update guidance for quota notices and the Rules and Approvals tabs. Existing billing MCP names remain compatible.

## 0.7.0 — 2026-09-11

- Sync skill 1.3.0 with permanent account-owned Pages, including Free, within existing quotas; anonymous previews retain their 24-hour expiry.
- Add a portable folder publisher with preflight, exact hashes, private recovery state, explicit sharing, and event-lifetime guards.
- Require account authorization before publishing future-event deliverables that outlive an anonymous preview.

## 0.6.0 — 2026-09-11

- Make website and event-page publishing discoverable in plugin descriptions and the shared skill.
- Separate Pages device authorization from optional Gateway relay setup, and point installation guidance to `/plugins`.
- Document version-bound sharing links, supported map embeds, and event-lifetime checks.
- Update OpenClaw install guidance to review and accept declared capabilities before restarting.

## 0.5.5 — 2026-09-10

- Sync skill 1.1.6 with signup and terms before setup, Agent prompt/dashboard choice, and saved final billing choice.
- Document completed legacy setup, Always release and Block sender behavior, owner-only outbound email, and provider-drafts availability checks. Email release never starts an Agent turn or approves external actions.
- Clarify Managed hosting availability, the bounded $5/30-day bootstrap allowance, durable provider setup, and separately configured channels.
- Point OpenClaw installation at the connector archive shipped by Claw Me. Keep plugin permissions and immutable templates-v3.0.0 assets unchanged.

## 0.5.4 — 2026-09-10

- Sync skill 1.1.4 for explicit Free, PAYG, Basic, or Plus selection as the last onboarding step. Free completes without a card.
- Document hosted card setup, separate wallet funding, the 72-hour warning, persisted purchase keys, and verified PAYG completion.
- Add billing choice, PAYG setup, and access-status tools to the discovery contracts without expanding plugin permissions.
- Clarify that managed hosting requires a Basic or Plus subscription and has a separate monthly charge.

# 0.5.2

- Sync skill 1.1.2 with the four-step onboarding guide, Profile visibility, private Agent context, Connections, and Calculator.
- Preserve existing Wiki MCP tool names, scopes, and API contracts.

# Changelog

## 0.5.3

- Keep Profile focused on public profile editing and private context. Direct connection management to Agents and remove Profile connection links from onboarding.

## 0.5.0 (unreleased)

- Document explicitly delegated, email-verified owner setup without the customer portal.
- Add concrete billing inputs, safe retries, account activation checks, and feature API routes.
- Sync the pinned skill bundle and permission manifest; owner-session access is an explicit permission change.
- Requires the portal-free API rollout; detect older servers and report the mismatch.


## 0.4.0 — 2026-09-01

- Let owners approve a least-privilege subset of the permissions an Agent requests instead of accepting an all-or-nothing bundle.
- Treat account products as optional capabilities and prevent Agents from assuming Wiki, Email, Pages, Drive, or other access is configured.
- Add capability discovery and structured access-reporting guidance, plus the complete optional onboarding, approvals, payments, recovery, Wiki refresh, publishing, and workspace references.
- Align anonymous preview guidance with the branded expiry banner, live countdown, and paid-plan handoff.

## 0.3.5 — 2026-08-27

- Add account-free “claw me that” publishing for unindexed static previews that expire within 24 hours.
- Align Agent guidance with `/address`, `/agents`, Drive Workspaces, Mailroom quarantine, Sandbox review, and customer-owned WhatsApp credentials.
- Document the anonymous create, presigned upload, finalize, footer, expiry, and safety contract.

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
