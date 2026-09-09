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

The landing screen at https://claw.me/getting-started offers Manual Setup or Ask Your Agent. These choices are only shown before the step flow. Resume the existing account and interview after checkout; never create a duplicate account or purchase again to resolve a pending activation.

The dashboard has four steps: address, features and permissions, connect an Agent, and Getting Started. Address selection and explicit owner confirmation of permissions are required. Account settings, Docs, public Templates, and Calculator at https://claw.me/calculator remain reachable. Back and Continue revisit saved steps without changing consent. After the required choices are saved, Agent connection is optional and workspace navigation is available; completed accounts do not enter the guide by default. Legacy review and page steps lead to Getting Started.

Step 2 shows key Agent-access choices and separate Public sharing and Incoming email sections. For new unconfirmed choices, Incoming email defaults to Store for me only: email_receive is on and email_process is off. Public sharing defaults off. Preserve confirmed choices and existing drafts; a displayed default is not consent or a saved permission. The owner confirms the effective account permissions before Agents act within them.

Profile at https://claw.me/my-profile contains Public profile, Agent context, and Connections. Step 2 covers key choices; detailed visibility, Page listings, API access, and existing A2A setup belong in Profile. Private context stays private when reviewed; public profile visibility, listing an already-public Page, and authorizing an Agent are separate actions. Public sharing is an account-wide upper bound, not automatic publication. A2A connections use existing scopes and plan eligibility; do not invent a separate global A2A switch or a routing service.

The connect step embeds the same setup prompt as the Agents page. Copying it does not install a plugin or authorize a client. Discover actual tools and scopes after installation and authorization. The UI name Profile context still uses stable wiki_* MCP tools, wiki scopes, and /claw-me/wiki REST paths. Old /wiki and /wikipage links redirect to Profile’s Agent context. /profile remains Account settings, and /pricing-calculator redirects to /calculator.

## Managed OpenClaw

The human completes identity and the initial recurring add-on payment before the Agent exists. Provisioning is not a free trial.

After the runtime is ready:

1. Resume the same onboarding session through the hosted OpenClaw gateway or the configured Telegram, WhatsApp, or email channel.
2. Do not repeat answers gathered before provisioning.
3. Explain that the Claw Me-funded inference allowance is temporary and help connect a durable provider early.
4. Never request provider credentials in chat. Use the secure provider handoff URL returned by Claw Me.

## Interview contract

- Ask only the current server-provided question.
- Present at most three choices, except for the `agent_client` catalog returned by the service. That catalog may show every supported connection from claw.me/connect.
- Offer `Other` only when `allow_other` is true and send its text separately.
- Do not infer consent, payment approval, publication visibility, or a secret value from free-form conversation.
- Resume after interruptions instead of starting a duplicate session.

See `contracts/onboarding.v1.schema.json` for the portable state and answer contract.

## Portal-free owner delegation

When the owner explicitly delegates setup through their existing Agent and personal inbox, use [portal-free-setup.md](portal-free-setup.md). It replaces portal handoffs with email-verified owner REST operations while preserving scoped MCP and explicit owner decisions. Do not direct that owner back to the portal merely because a response includes a legacy `human_action.url` when an authorized API equivalent exists.
