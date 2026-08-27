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
