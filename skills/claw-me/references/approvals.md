<!-- SPDX-License-Identifier: MIT -->

# Proposals and approvals

Claw Me separates an Agent proposal from the owner's decision.

Prepare a proposal before actions that publish, send externally, spend money, change a provider/domain/runtime, modify durable configuration, delete, revoke, restore, or overwrite work.

Summarize the intended outcome, affected resources, expected cost or visibility, and recovery path. Do not place credentials or private message bodies in proposal metadata.

- The Agent that created a proposal cannot approve it.
- An approval applies only to the immutable payload and version shown to the owner.
- If the proposal changes, create a new proposal and request a new decision.
- Execute with the returned idempotency key. On an uncertain result, check status before retrying.

Low-risk reads can run without a proposal when the current token includes the required read scope.
