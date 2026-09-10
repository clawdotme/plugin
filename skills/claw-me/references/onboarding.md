<!-- SPDX-License-Identifier: MIT -->

# Agent-first onboarding

The live service owns the interview state. Do not recreate the question order from memory.

## Existing Agent

1. Start or resume the onboarding session.
2. If the owner has not authorized this client, begin device authorization with `openid`, `profile`, `onboarding:read`, and only the write/proposal scopes needed.
3. The owner reviews the named client and requested scopes in Claw Me. The owner may deselect optional products and approve a smaller scope set.
4. Call `onboarding_resume`, ask exactly the returned question, and submit one answer at a time.
5. Use `onboarding_preview` before submitting a setup proposal.
6. Stop at any `human_action` returned by the service and direct the owner to its secure URL.

## Dashboard setup and Profile

Registration starts with email and explicit terms acceptance. Account setup choices follow registration. At https://claw.me/getting-started, choose **Get a prompt for my Agent** (`?mode=agent`) or **Use the guided dashboard instead** (`?mode=dashboard`). The Agent path then asks which client the owner uses and provides its plugin installation and connection guidance. Assume an existing Agent unless the owner asks for Managed hosting. Resume the existing account and interview after checkout; never create a duplicate account or purchase again to resolve a pending activation.

The dashboard has four steps: address, features and permissions, connect an Agent, and billing choice. Finishing the saved billing choice shows Setup complete; a completed owner returning to Getting Started is sent to Pages. Address selection and explicit owner confirmation of permissions are required. Account settings, Docs, public Templates, and Calculator at https://claw.me/calculator remain reachable. Back and Continue revisit saved steps without changing consent. After the required choices are saved, Agent connection is optional and workspace navigation is available; completed accounts do not enter the guide by default. Legacy review and page links resume the final billing choice if it has not been confirmed, then continue into the workspace.

Step 2 shows key Agent-access choices and separate Public sharing and Incoming email sections. For new unconfirmed choices, Incoming email defaults to Store for me only: email_receive is on and email_process is off. Public sharing defaults off. Preserve confirmed choices and existing drafts; a displayed default is not consent or a saved permission. The owner confirms the effective account permissions before Agents act within them.

Profile at https://claw.me/my-profile contains public profile editing and private agent context. Step 2 covers key feature and sandbox choices; detailed visibility and page listings belong in Profile. Existing agent connections and A2A discovery belong under Agents at https://claw.me/agents?view=authorizations. Private context stays private when reviewed; public profile visibility, listing an already-public Page, and authorizing an Agent are separate actions. Public sharing is an account-wide upper bound, not automatic publication. A2A connections use existing scopes and plan eligibility; do not invent a separate global A2A switch or a routing service.

The connect step embeds the same setup prompt as the Agents page. Copying it does not install a plugin or authorize a client. Discover actual tools and scopes after installation and authorization. The UI name Profile context still uses stable wiki_* MCP tools, wiki scopes, and /claw-me/wiki REST paths. Old /wiki and /wikipage links redirect to Profile’s Agent context. /profile remains Account settings, and /pricing-calculator redirects to /calculator.

## Final billing choice

After address, owner-confirmed permissions, and Agent connection (which may be skipped), present the final choice explicitly: Free, pay as you go when enabled in the live catalog, Basic, or Plus. Never select a paid option for the owner. Read [payments.md](payments.md) for allowances, separate wallet funding and the 72-hour warning. Free requires no card or purchase.

With the final-choice rollout, read `GET /api/v1/billing/onboarding` (`billing:read`) and record the owner-approved choice using `billing_onboarding_choice` or `POST /api/v1/billing/onboarding` (`billing:propose`), with `choice` and `confirm: false`. The response saves a `checkout_key`; reuse it as the hosted setup or checkout `idempotency_key` for that choice. Start `billing_start_payg` for PAYG or `billing_start_checkout` for a subscription only after explicit approval. Never cancel or replace an existing subscription as part of onboarding.

For Free, or after the selected access is verified by the backend, submit the same choice with `confirm: true`. The server rejects unverified paid activation. Resume pending choices after cancellation, reload, or a delayed webhook; a Stripe redirect and a completed Agent interview are not proof of completed account billing. If these tools are absent from live discovery, report that the rollout is unavailable and use the supported flow.

## Managed OpenClaw

Check the live hosting availability before offering checkout or provisioning. Managed hosting remains unavailable while its launch gates are disabled; an existing Agent does not require this add-on. When available, the human completes identity and the initial recurring add-on payment before the Agent exists. Provisioning is not a free trial.

After the runtime is ready:

1. Resume the same onboarding session through the hosted OpenClaw Gateway. Use another channel only after its setup and permissions are verified; released email does not automatically start an Agent session.
2. Do not repeat answers gathered before provisioning.
3. Explain that the Claw Me-funded inference allowance is temporary and help connect a durable provider early.
4. Never request provider credentials in chat. Use the secure provider handoff URL returned by Claw Me.

## Interview contract

- Ask only the current server-provided question. If an existing-Agent session reports `completed` / `account_setup_complete` with no questions, do not restart the old interview. Completed dashboard setup can satisfy an older existing-Agent interview; this does not change the granted scopes or bypass owner consent.
- Present at most three choices, except for the `agent_client` catalog returned by the service. That catalog may show every supported connection from claw.me/connect.
- Offer `Other` only when `allow_other` is true and send its text separately.
- Do not infer consent, payment approval, publication visibility, or a secret value from free-form conversation.
- Resume after interruptions instead of starting a duplicate session.

See `contracts/onboarding.v1.schema.json` for the portable state and answer contract.

## Portal-free owner delegation

When the owner explicitly delegates setup through their existing Agent and personal inbox, use [portal-free-setup.md](portal-free-setup.md). It replaces portal handoffs with email-verified owner REST operations while preserving scoped MCP and explicit owner decisions. Do not direct that owner back to the portal merely because a response includes a legacy `human_action.url` when an authorized API equivalent exists.
