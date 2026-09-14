<!-- SPDX-License-Identifier: MIT -->

# Authorize account access

This approves scoped access to the owner's Claw Me account, not to their computer. Installation, account approval, and account feature permissions are separate. Reuse credentials only when they cover the requested work; preserve other task credentials.

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

Never send that request ID to `/oauth/token`. Client-managed OAuth instead starts at `/oauth/device_authorization` with `client_id` and exchanges `device_code` at `/oauth/token` using that same `client_id` and the device-code grant type. OAuth returns `access_token`; the non-OAuth pair returns `api_key`. Keep one protocol for the entire request.
