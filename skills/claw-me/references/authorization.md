<!-- SPDX-License-Identifier: MIT -->

# Authorize account access

This approves scoped access to the owner's Claw Me account, not to their computer. Installation, account approval, and account feature permissions are separate. Reuse credentials only when they cover the requested work; preserve other task credentials.

## Choose a connection path first

Reuse an existing scoped connection. An explicitly requested disposable static Page can instead use anonymous publishing for 24 hours without an account or plugin, subject to the limits in [publishing.md](publishing.md). For account access, choose the plugin at https://claw.me/plugins or direct MCP at https://claw.me/api/v1/mcp. If this Agent cannot install or configure either, give the owner https://claw.me/getting-started and resume after they connect. Verify a permitted read before claiming success. A website `CLAUDE.md` is not automatically loaded by the client.

## Choose scopes before creating one request

- Connect and verify only: `onboarding:read`, then `account_get_permissions`.
- Finish onboarding: `onboarding:read`, `onboarding:write`, `setup:read`, `setup:propose`, `billing:read`, `billing:propose`. Resume the server interview, preview proposals, and ask for the owner's plan choice. Billing scopes do not authorize payment.
- Other work: request only that task's scopes. Wiki, Drive, Pages, and email access are not prerequisites for connection or onboarding. Read Profile context only when requested, enabled, and covered by `wiki:read`.

## Installed helper

When the client already manages OAuth, use that connection. Otherwise run the bundled helper from the installed skill directory. Ask for the owner's Claw Me email if it was not supplied; do not infer it from another service's login.

```bash
python3 scripts/authorize.py start --email OWNER_EMAIL --client-name "My Agent" --client-type generic --scope onboarding:read --state ~/.claw-me/setup-authorization.json
```

Replace `OWNER_EMAIL` with the supplied address. For full onboarding, add the other five setup scopes with repeated `--scope` flags before creating the request. Keep state outside the repository and uploaded content. The helper uses private local JSON storage (mode 0600); never print or attach that file. No scopes are added by default.

Show the returned `verification_uri` exactly as one complete clickable link with the client name, scopes, and expiry. This is an approval link, not a sign-in secret. The owner signs in and approves there; never ask for an API key, device secret, setup code, or emailed sign-in token in chat. Do not claim that an email was delivered without evidence.

After the owner approves:

```bash
python3 scripts/authorize.py poll --state ~/.claw-me/setup-authorization.json
```

Each invocation polls once. `pending` means approval has not been recorded; wait for the owner instead of repeatedly polling. `authorized` means the key and granted scopes were saved privately. Read the `api_key` field only inside the client credential loader, or import it into its secret manager without printing it or embedding it in shell arguments. The helper does not configure the client's MCP connection. Configure the official MCP URL `https://claw.me/api/v1/mcp` with that credential, inspect available tools, and verify a permitted read-only action before claiming connection success. A smaller approved scope set may leave setup awaiting additional owner access; never claim missing tools are available.

Re-running `start` with the same state and arguments reuses the request. An uncertain creation or token exchange stops rather than issuing duplicates; inspect its status without displaying private contents. Expired or denied requests need a new owner-reviewed request, not an automatic loop.

## REST equivalent and OAuth distinction

If the helper cannot run, use this exact non-OAuth pair, keeping responses in secure local storage:

1. `POST https://claw.me/api/v1/agent-auth/requests` with `owner_email`, `client_name`, `client_type`, and explicit `scopes`.
2. Save `request_id` and `device_secret` before displaying `verification_uri`.
3. After owner approval, `POST /api/v1/agent-auth/requests/{request_id}/token` with JSON containing `device_secret`. A pending response has `status: authorization_pending`; an approved response has `status: authorized`, `api_key`, and granted `scopes`. Save the key before any further work: exchange is single-use.

Never send that request ID to `/oauth/token`. Client-managed OAuth uses either the authorization-code flow below or `/api/v1/agent-auth/oauth/device_authorization` with `client_id`, exchanging `device_code` at `/api/v1/agent-auth/oauth/token` with that same `client_id` and the device-code grant type. Always send explicit `scope=onboarding:read` for a connection check. OAuth returns `access_token`; the non-OAuth pair returns `api_key`. Keep one protocol for the entire request.

## Client-managed native MCP OAuth

Discover https://claw.me/.well-known/oauth-authorization-server and https://claw.me/.well-known/oauth-protected-resource. Use authorization code only when current discovery advertises `authorization_code` and `S256`; otherwise use the documented device flow. Do not infer that a newer bundle has already been deployed.

The canonical MCP resource is `https://claw.me/api/v1/mcp`. The client registers at `/api/v1/agent-auth/oauth/register` with `client_name`, `redirect_uris`, `grant_types: ["authorization_code"]`, and `token_endpoint_auth_method: "none"`. Redirect URIs must be HTTPS or loopback HTTP. The client, not this skill's helper, manages callbacks and securely keeps its PKCE verifier.

The client opens `/api/v1/agent-auth/oauth/authorize` with its returned `client_id`, exact registered `redirect_uri`, `response_type=code`, `code_challenge_method=S256`, `code_challenge`, `state`, `resource=https://claw.me/api/v1/mcp`, and explicit minimal scopes. The owner signs in and reviews access. The client validates callback state and exchanges form data at `/api/v1/agent-auth/oauth/token`: `grant_type=authorization_code`, `code`, `client_id`, `redirect_uri`, `code_verifier`, and the same `resource`. Store the returned `access_token` privately; never put callback URLs, codes, or verifiers in chat. No client secret or refresh-token grant is supported.

Native MCP authorization-code grants accept API scopes, not `openid` or `profile`. Device authorization supports these identity scopes when the client needs OIDC; they are not prerequisites for MCP. Keep one flow's fields together. After configuration, initialize MCP, send `notifications/initialized`, inspect `tools/list`, and run `account_get_permissions` with `onboarding:read`. Approval alone does not prove connection success.
