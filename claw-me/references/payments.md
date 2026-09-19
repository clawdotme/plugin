<!-- SPDX-License-Identifier: MIT -->

# Payments

Claw Me uses Stripe Billing and hosted Checkout for recurring plans. Machine Payments Protocol (MPP) is available only for supported one-time Claw Me purchases.

1. Read the billing catalog; do not hardcode prices or availability.
2. Create a quote for one exact owner, purpose, amount, and currency.
3. Explain whether payment uses recurring Checkout, one-time MPP, or hosted Checkout fallback.
4. Obtain the owner's explicit approval before initiating payment.
5. For MPP, use only the short-lived payment URL returned by Claw Me. Do not add a bearer token to the payment retry; the opaque URL already binds the quote.
6. Check `billing_payment_status` before retrying after a timeout.

- MPP v1 pays Claw Me only; it is not a general purchasing wallet.
- Agents never receive raw card details or reusable Stripe credentials.
- Wallet funds are closed-loop and non-withdrawable.
- Never enable auto-reload, raise a cap, or change a recurring plan without explicit owner approval.

For the portal-free rollout, read [portal-free-setup.md](portal-free-setup.md). `billing_quote` reports current catalog information, not a binding quote. `billing_start_checkout` and `billing_create_wallet_payment` create hosted Stripe sessions with an `idempotency_key`; payment status is separate from webhook-confirmed account activation. Do not describe MPP as available unless live discovery explicitly confirms it.


## Optional usage billing on Free

Offer three plans: Free, Basic and Plus. Free signup never requires a card.
Offer usage billing within Free when an owner needs a custom domain or extra
usage, only when enabled in the live catalog. It is not a fourth plan.
With explicit owner approval, call the compatibility-named `billing_start_payg`
with an `idempotency_key` and show its hosted card-setup URL. Setup charges
nothing and never cancels an existing subscription. `billing_access_status`
returns the actual `effectivePlan` (Free remains `free`), `usageBillingEligible`,
legacy `billingMode`, and payment recovery deadline. Card eligibility alone
never authorizes wallet debits: separately obtain approval for funding and
the spending controls in Billing. Discover exact tool names and schemas;
do not invent a tool to change spending consent. Automatic reload is a separate opt-in.

The same 100 monthly emails and 1 GB storage stay included. Eligible Free
accounts retain 100 Pages, one durable Drive, one connected domain, Wiki and
approved Agent access; storage capacity is 10 GiB, with overages after 1 GB.
Numbers still require Basic or Plus. Their subscription
allowances take precedence until cancellation actually takes effect.
A missing last card or failed required reload starts the existing 72-hour
warning. Do not promise unfunded work during grace. Replace a missing card or
complete an approved wallet load to recover a failed reload. Do not retry the
failed automatic charge alongside a replacement purchase. Billing suspension
retains data and wallet funds and leaves the account on Free.

Monthly quota notices appear at 80% and 100% and link to usage billing. Email
and meeting allowances reset at the start of the next UTC calendar month;
storage capacity does not reset. Existing mailroom retention applies to held
inbound mail, which is not released to an Agent until billing and permissions
allow it. Usage notices go to the verified account email independently of the
metered alias. Never interpret a quota notice as owner approval to spend.
