<!-- SPDX-License-Identifier: MIT -->

# Agent-first onboarding

The live service owns the interview state. Do not recreate the question order from memory.

## Existing Agent

1. Start or resume the onboarding session.
2. If the owner has not authorized this client, begin device authorization with `openid`, `profile`, `onboarding:read`, and only the write/proposal scopes needed.
3. The owner reviews the named client and requested scopes in Claw Me.
4. Call `onboarding_resume`, ask exactly the returned question, and submit one answer at a time.
5. Use `onboarding_preview` before submitting a setup proposal.
6. Stop at any `human_action` returned by the service and direct the owner to its secure URL.

## Managed OpenClaw

The human completes identity and the initial recurring add-on payment before the Agent exists. Provisioning is not a free trial.

After the runtime is ready:

1. Resume the same onboarding session through the hosted OpenClaw gateway or the configured Telegram, WhatsApp, or email channel.
2. Do not repeat answers gathered before provisioning.
3. Explain that the Claw Me-funded inference allowance is temporary and help connect a durable provider early.
4. Never request provider credentials in chat. Use the secure provider handoff URL returned by Claw Me.

## Interview contract

- Ask only the current server-provided question.
- Present at most three choices.
- Offer `Other` only when `allow_other` is true and send its text separately.
- Do not infer consent, payment approval, publication visibility, or a secret value from free-form conversation.
- Resume after interruptions instead of starting a duplicate session.

See `contracts/onboarding.v1.schema.json` for the portable state and answer contract.
