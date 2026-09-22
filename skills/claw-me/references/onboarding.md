<!-- SPDX-License-Identifier: MIT -->

# Agent-first onboarding

The live service owns the interview state. Do not recreate the question order from memory.

## Use your own account

“Account owner” means you, the user of a Claw Me account, not the owner of the claw.me domain. You do not need DNS access or permission from the service operator to host a Page.

For a durable Page, reuse your existing account. If you have not signed up, create an account at https://claw.me/register, accept the terms, and verify your email before starting a short-lived Agent approval request. Existing users can sign in at https://claw.me/login. Account feature setup can then continue with the Agent where supported. Do not ask users to forward approval codes to whoever owns claw.me. If account status is unknown, explain signup or sign-in first; do not infer it from an email address.

Anonymous 24-hour previews require no account, sign-in, or pairing. An authorization code is not an account or a sign-in link. If a request was already created, complete signup and return to its approval link; create a new request only after expiry when still needed. Preserve private request state.

## Existing Agent

1. Check the existing connection before starting or resuming the onboarding session.
2. For the full onboarding workflow, authorize `onboarding:read`, `onboarding:write`, `setup:read`, `setup:propose`, `billing:read`, and `billing:propose` through [authorization.md](authorization.md). Connection-only verification needs just `onboarding:read`. Select the scope set from the whole requested task before opening one approval request. Do not add Wiki, Drive, Pages, or email scopes unless the owner separately chooses that work.
3. The owner reviews the named client and requested scopes in Claw Me. The owner may deselect optional products and approve a smaller scope set.
4. Call `onboarding_resume`, ask exactly the returned question, and submit one answer at a time.
5. Use `onboarding_preview` before submitting a setup proposal.
6. Stop at any `human_action` returned by the service and direct the owner to its secure URL.

## Dashboard setup and Profile

Registration starts with email and explicit terms acceptance. Account setup choices follow registration. At https://claw.me/getting-started, choose **Get a prompt for my Agent** (`?mode=agent`) or **Use the guided dashboard instead** (`?mode=dashboard`). The Agent path then asks which client the owner uses and provides its plugin installation and connection guidance. Connect an Agent the owner already uses. Resume the existing account and interview after checkout; never create a duplicate account or purchase again to resolve a pending activation.

The dashboard has four steps: address, features and permissions, connect an Agent, and billing choice. After Stripe returns and the backend verifies the selected paid entitlement, Claw Me finishes the saved choice automatically and opens `?mode=dashboard&step=start`; never use the redirect itself as proof. The completed screen provides a full Agent handoff prompt, a visible Connect or Manage Agent route, and direct workspace destinations. Address selection and explicit owner confirmation of permissions are required. Account settings, Docs, public Templates, and Calculator at https://claw.me/calculator remain reachable. Back and Continue revisit saved steps without changing consent. After the required choices are saved, Agent connection is optional and workspace navigation is available; completed accounts do not enter the guide by default. Legacy review and page links resume the final billing choice if it has not been confirmed, then continue into the workspace.

Step 2 shows key Agent-access choices and separate Public sharing and Incoming email sections. For new unconfirmed choices, Incoming email defaults to Store for me only: email_receive is on and email_process is off. Public sharing defaults off. Preserve confirmed choices and existing drafts; a displayed default is not consent or a saved permission. The owner confirms the effective account permissions before Agents act within them.

Public profile editing and Page listings live at https://claw.me/pages?view=profile. Private Context, managed Memory, Style Guides and Workspaces live under Drive at https://claw.me/drive. Existing Agent connections and A2A discovery are in Settings → Connected Agents at https://claw.me/settings/agents. Private context stays private when reviewed; public profile visibility, listing an already-public Page, enabling Memory, and authorizing an Agent are separate actions. Public sharing is an account-wide upper bound, not automatic publication. A2A connections use existing scopes and plan eligibility; do not invent a separate global A2A switch or a routing service.

The connect step embeds the same setup prompt as Settings → Connected Agents. Copying it does not install a plugin or authorize a client. Discover actual tools and scopes after installation and authorization. The UI name Context still uses stable wiki_* MCP tools, wiki scopes, and /claw-me/wiki REST paths. Old /profile and /my-profile links redirect to Pages → Public profile; /wiki and /wikipage redirect to Drive → Context. Account settings are at /settings, and /pricing-calculator redirects to /calculator.

## Final billing choice

After address, owner-confirmed permissions, and Agent connection (which may be skipped), present the final choice explicitly: Free, Basic, or Plus. Optional usage billing is a later setting within Free, not an onboarding plan. Never select a paid option for the owner. Read [payments.md](payments.md) for allowances, separate wallet funding and the 72-hour warning. Free requires no card or purchase.

With the final-choice rollout, read `GET /api/v1/billing/onboarding` (`billing:read`) and record the owner-approved choice using `billing_onboarding_choice` or `POST /api/v1/billing/onboarding` (`billing:propose`), with `choice` and `confirm: false`. The response saves a `checkout_key`; reuse it as the hosted setup or checkout `idempotency_key` for that choice. Start `billing_start_checkout` for a subscription only after explicit approval. For Free, confirm `free` without card setup. Legacy `payg` selections are displayed as Free and do not block card-free completion. Never cancel or replace an existing subscription as part of onboarding.

For Free, or after the selected access is verified by the backend, submit the same choice with `confirm: true`. The server rejects unverified paid activation. Resume pending choices after cancellation, reload, or a delayed webhook; a Stripe redirect and a completed Agent interview are not proof of completed account billing. If these tools are absent from live discovery, report that the rollout is unavailable and use the supported flow.

After completion, call `claw_me_feature_guide` with `feature=all` and introduce only the products available to the account and current connection. Verify the connection and account state read-only first. Offer a useful private Page as the first task, then summarize what is connected, what remains private, and which actions still require owner approval.

## Interview contract

- Ask only the current server-provided question. If an existing-Agent session reports `completed` / `account_setup_complete` with no questions, do not restart the old interview. Completed dashboard setup can satisfy an older existing-Agent interview; this does not change the granted scopes or bypass owner consent.
- Present at most three choices, except for the `agent_client` catalog returned by the service. That catalog may show every supported connection from claw.me/plugins.
- Offer `Other` only when `allow_other` is true and send its text separately.
- Do not infer consent, payment approval, publication visibility, or a secret value from free-form conversation.
- Resume after interruptions instead of starting a duplicate session.

See `contracts/onboarding.v1.schema.json` for the portable state and answer contract.

## Portal-free owner delegation

When the owner explicitly delegates setup through their existing Agent and personal inbox, use [portal-free-setup.md](portal-free-setup.md). It replaces portal handoffs with email-verified owner REST operations while preserving scoped MCP and explicit owner decisions. Do not direct that owner back to the portal merely because a response includes a legacy `human_action.url` when an authorized API equivalent exists.
