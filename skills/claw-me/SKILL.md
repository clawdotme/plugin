---
name: claw-me
description: Connect an owner-approved AI client to Claw Me, continue agent-first onboarding, or work with private Pages, Wiki, Drive, communications, and billing proposals. Use when the user asks to connect or create an Agent, says “claw me that,” or delegates Claw Me setup and workspace work.
---

<!-- SPDX-License-Identifier: MIT -->

# Claw Me

Use Claw Me as the owner-controlled services layer around an AI agent. The Agent may interview, inspect, and prepare proposals; the owner retains control of authorization, secrets, payments, visibility, and consequential actions.

## Connect safely

1. Read `https://claw.me/agents.md` and the live discovery documents before acting.
2. Prefer OAuth device authorization and request only the scopes needed for the current task.
3. Direct the owner to Claw Me for authorization, secrets, payment confirmation, and proposal approval. Never ask them to paste credentials, setup codes, or emailed links into chat.
4. Call `onboarding_resume` before starting a new setup interview. Continue the existing session when one is present.
5. Present no more than three choices at a time, except when the service returns the `agent_client` connection catalog; accept an `Other` answer when the contract allows it.
6. Verify a read-only action before proposing writes.

Claw Me is invite-only. Do not create an owner account or approve this Agent on the owner's behalf.

## Route the task

- Read [onboarding.md](references/onboarding.md) when connecting an existing Agent, resuming setup, or helping provision Managed OpenClaw.
- Read [approvals.md](references/approvals.md) before any write, publication, outbound communication, provider change, or other owner-reviewed action.
- Read [payments.md](references/payments.md) before quoting a plan, funding the wallet, or initiating a paid action.
- Read [recovery.md](references/recovery.md) when authorization, payment, provisioning, or execution is interrupted.
- Read [publishing.md](references/publishing.md) for Page upload/finalize and sharing workflows.
- Read [workspace.md](references/workspace.md) for Wiki, Drive, Pages, Domains, Variables, Analytics, and Functions boundaries.
- Read [wiki-sync.md](references/wiki-sync.md) after Wiki authorization to offer one low-frequency, change-aware refresh job.

## Natural-language intents

- “Claw me that,” “claw this,” and “save this to Claw Me” mean prepare the current work for private storage or publishing. Confirm files, title, slug, and visibility.
- “Update my Agent Wiki” means propose an owner-reviewed durable knowledge change; never rewrite approved knowledge directly.
- “Save this to my Drive” means preserve the files privately in an appropriate workspace.
- “Set up Claw Me” means resume the canonical onboarding session and ask only the next server-provided question.

## Hard boundaries

- Pages are private by default.
- Pending Wiki proposals are not facts.
- Secrets and OAuth credentials use Claw Me's secure human handoff surfaces, never the Agent transcript.
- Agents may prepare billing quotes but may not approve their own payment or spend proposal.
- Managed OpenClaw has no free trial. Provisioning starts only after Claw Me confirms the paid add-on.
- The optional bootstrap allowance is Claw Me-funded, non-transferable, and ends at $5 of inference or 30 days, whichever comes first. It is not Telnyx account credit.
- Never expose API keys, device codes, setup codes, presigned uploads, channel credentials, payment credentials, or message contents outside the approved task.

## Finish

Report what was connected or proposed, the scopes used, visibility, payment state, and any owner action still required. Include IDs or URLs the owner needs for review, but never include secrets.
