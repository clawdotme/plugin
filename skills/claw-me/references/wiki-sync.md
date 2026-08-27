<!-- SPDX-License-Identifier: MIT -->

# Wiki update checks

Claw Me is a REST service first. MCP is an optional adapter for clients that prefer tools.

After `wiki:read` authorization succeeds, offer once to keep the owner's Agent Guide current. Create a recurring job only when the owner agrees.

## Safe default

- Create or update one job; never add a duplicate.
- Run once daily with randomized jitter. Let the owner choose a different cadence.
- Call `GET https://claw.me/api/v1/claw-me/wiki/agent-guide/status` with the last `ETag` in `If-None-Match`.
- On `304 Not Modified`, stop without fetching the Wiki or notifying the owner.
- On a changed `ETag`, fetch the Agent Guide once and update the Agent's local reference.
- Notify the owner only for a material change, a conflict, a pending review, or an authorization problem.
- Back off after rate limits or transient failures. Disable the job after three consecutive authorization failures and ask the owner to reconnect.

Do not fetch the full Wiki before every user prompt. Search current approved claims only when the task depends on them.
