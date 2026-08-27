<!-- SPDX-License-Identifier: MIT -->

# Recovery

Use status reads before repeating any mutation.

- Expired or consumed handoff codes cannot be reused. Generate a new code.
- If the owner denied scopes, continue with the granted subset or explain the missing capability.
- Never ask the owner to reveal a device secret or API key.
- A canceled or expired Checkout session is not a completed payment.
- After an MPP timeout, query the payment ID before creating another quote.
- Duplicate webhook delivery is expected; receipts and fulfillment are idempotent.
- Keep onboarding resumable while provisioning is pending or failed.
- Do not claim an action completed until its receipt is final.
- When bootstrap inference is exhausted, pause model work and direct the owner to connect a provider; do not auto-charge.
