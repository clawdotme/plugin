# Claw Me workspace

Use this reference to decide where Claw work belongs and to explain workspace controls without overstating the current agent API.

## Placement guide

| Need | Use | Operating rule |
| --- | --- | --- |
| A durable site, document, app, deck, or report | Page | Private by default; publish a new immutable version for each update. |
| A private upload or Agent output | Drive Files | Available on every plan; use it without creating a collaborative Workspace. |
| Files edited by people and multiple Agents | Drive Workspace | Basic or Plus; stage changes from an explicit revision and wait for owner acceptance. |
| Reviewed facts shared across authorized Agents | Wiki | Read approved claims; propose changes for owner review. |
| Forms, waitlists, comments, or small shared state | Site Data | Use same-origin `/.claw/data/{collection}` calls. |
| A custom web address | Domains | The owner connects DNS to a selected Page from the dashboard. |
| Values needed by approved Agents or Page proxy routes | Variables | Store encrypted values in the dashboard, never in chat or Page files. |
| Page audience and traffic reporting | Analytics | Use first-party, cookie-free reports without retained visitor IP addresses. |
| Routes, schedules, deployment guidance, Variables, and Secrets | Functions | Use only the controls that the current dashboard or API explicitly exposes. |

## Pages, Drive Files, Workspaces, and versions

- Page files belong to an immutable Page version. Standalone Drive Files do not need a Page.
- Drive opens on Files for every account. Collaborative Workspaces require Basic or Plus.
- Before editing a Workspace, use `drive_list_workspaces` and `drive_open_workspace`, then read the current revision, instructions, manifest, and review state.
- Begin edits with `drive_begin_change`, write through `drive_write_file`, preview with `drive_preview_change`, and submit with `drive_submit_change`.
- Submission never applies a change. The owner accepts or rejects it in Drive, and an Agent cannot accept its own proposal.
- Accepted changes and restores create immutable revisions. Same-file stale changes require a fresh change set from the latest revision; never hide or overwrite a conflict.
- A Page begins private. The owner may deliberately make it public, grant access to exact Claw Me accounts, grant an email domain with `@domain`, add password access, or issue an expiring private review link.
- Public Pages appear on the public profile only when the owner chooses to list them.
- Guest and Free previews expire after 24 hours unless claimed onto an eligible plan. Publishing another version does not extend the expiry.
- Use `artifact_list` and `artifact_publish` for Pages. The `pages:read` and `pages:write` scope names map to artifact read/write access.
- Use `drive:read` for Workspace inspection and `drive:propose` only when staged edits are required.

## Site Data

- Published Page code calls `/.claw/data/{collection}` on the same origin. Never embed Manager URLs, API keys, or database credentials in a Page bundle.
- Site Data is appropriate for lightweight forms, waitlists, comments, and shared state, not arbitrary backend execution.
- Get explicit owner confirmation before creating a collection, allowing public writes, changing a schema, or deleting records.

## Domains

- The owner selects a Page, proves DNS control, and points the hostname to `pages.claw.me` with a CNAME. Root domains need ALIAS or ANAME flattening from the DNS provider.
- Domain limits are plan entitlements: Basic supports one and Plus supports five.
- The live dashboard may require certificate material for TLS configuration. Never ask the owner to paste a certificate private key or DNS credential into chat; send them to the dashboard.
- Do not claim direct MCP control over Domains.

## Variables and Secrets

- Variables are encrypted values used by approved Agents or Page proxy routes and are classified as `secret`, `private`, or `public`.
- Plaintext is not returned after creation. The owner creates, rotates, and deletes values in the dashboard.
- Never ask the owner to paste a Variable or Secret value into chat. Never place one in published HTML, JavaScript, logs, screenshots, or a Page manifest.
- Do not claim direct MCP control over Variables or Secrets.

## Analytics

- Analytics reports first-party Page activity over a 30-day view: views, visitors, paths, referrers, countries, versions, and active grants.
- Reporting is cookie-free. Visitor uniqueness uses a daily one-way hash at the edge, and Claw Me does not retain visitor IP addresses.
- Treat Analytics as read/report functionality within the allowed owner scope. Do not claim MCP access unless a current contract exposes it.

## Functions

- The workspace Functions area groups Routes, Cron jobs, Deployments, Variables, and Secrets. Some surfaces are guidance or staged controls.
- Do not promise a general-purpose serverless runtime, arbitrary code execution, or direct MCP management.
- For secret-backed Page operations, use documented proxy routes and dashboard-managed Variables. For simple shared state, prefer Site Data.

## Capability boundary

The current MCP workspace surface includes Page tools (`artifact_list`, `artifact_publish`) and Drive Workspace tools (`drive_list_workspaces`, `drive_open_workspace`, `drive_begin_change`, `drive_write_file`, `drive_preview_change`, `drive_submit_change`). If a user asks an Agent to manage Domains, Variables, Analytics, Functions, or another control not exposed by the live contract, explain the steps and direct the owner to the dashboard. Never improvise an endpoint or claim the change was made.
