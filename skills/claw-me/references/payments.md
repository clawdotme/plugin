<!-- SPDX-License-Identifier: MIT -->

# Payments

Claw Me uses Stripe Billing and hosted Checkout for recurring plans and Managed OpenClaw. Machine Payments Protocol (MPP) is available only for supported one-time Claw Me purchases.

1. Read the billing catalog; do not hardcode prices or availability.
2. Create a quote for one exact owner, purpose, amount, and currency.
3. Explain whether payment uses recurring Checkout, one-time MPP, or hosted Checkout fallback.
4. Obtain the owner's explicit approval before initiating payment.
5. For MPP, use only the short-lived payment URL returned by Claw Me. Do not add a bearer token to the payment retry; the opaque URL already binds the quote.
6. Check `billing_payment_status` before retrying after a timeout.

- MPP v1 pays Claw Me only; it is not a general purchasing wallet.
- Agents never receive raw card details or reusable Stripe credentials.
- Wallet funds are closed-loop and non-withdrawable.
- Managed OpenClaw must be webhook-confirmed before provisioning or bootstrap allowance grant.
- Never enable auto-reload, raise a cap, or change a recurring plan without explicit owner approval.

For the portal-free rollout, read [portal-free-setup.md](portal-free-setup.md). `billing_quote` reports current catalog information, not a binding quote. `billing_start_checkout` and `billing_create_wallet_payment` create hosted Stripe sessions with an `idempotency_key`; payment status is separate from webhook-confirmed account activation. Do not describe MPP as available unless live discovery explicitly confirms it.


## Pay as you go

When the live catalog advertises PAYG, offer it alongside subscriptions. With
owner approval, call `billing_start_payg` with an `idempotency_key` and show the
returned hosted card-setup URL. It charges nothing and does not cancel an
existing subscription. Poll `billing_access_status` for verified eligibility,
`effectivePlan`, `billingMode`, and `graceEndsAt`; card setup is not a wallet load.

PAYG grants Basic workspace features with 100 emails and 50 MiB included storage,
no included meeting minutes or numbers. The first pilot keeps phone numbers and
managed hosting on subscription plans. Paid usage requires a funded wallet and
owner-set cap. Automatic reload authorization is separate. A missing last card
or failed required reload starts a 72-hour warning; do not promise unfunded work
during grace. Replace a missing card or complete an approved wallet load to
recover a failed reload. Never retry the failed automatic charge alongside a
replacement purchase. Subscription access takes precedence over PAYG status.
