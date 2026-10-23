# Phone and connected-agent Inbox

Read this reference for Flutter chat, host pairing, blocking questions or voicemail. Phone features require the current pilot to be available for the account and device; installing the skill alone does not enable them.

## Navigation and connection

The Flutter app opens on **Chat**, with **Inbox** and **Phone** as its other tabs. Drive and Pages open the connected account's real web workspace from Settings, with a browser account check. The normal app uses real connections and does not display sample workspaces. Missions is hidden. On the web, **Inbox** replaces the Sandbox label. Existing `/sandbox` URLs, scoped API paths and MCP names remain compatible.

The phone signs in with Claw Me and the owner reviews each phone and host connection. An outbound host connector carries chat and native questions/approvals without requiring the phone to share the host's Wi-Fi, install Tailscale or pin a gateway certificate. The host must remain online. Do not infer that a phone connection authorizes Pages, Drive or this Agent's API access, or use a connector credential as a general API key.

## Blocking questions and approvals

OpenClaw's native `ask_user` tool can submit questions where its installed Gateway and primary session support it and the connector has question access. Discover availability rather than promising it on every version/channel. Keep the exact question, options, session binding and timeout. An answer resolves that question; it does not approve a command. Do not resolve the owner's question on their behalf.

Codex hooks can forward future questions and approvals from explicitly selected chats or an explicitly reviewed all-chat connection on that computer. All-chat access does not copy chat history or connect other computers. Hook installation and normal client trust are separate from account approval. Preserve native approval rules and the exact request's identity, revision, digest and conversation.

Chat and Inbox show the same native approval. Decide it once; inspect its receipt after an uncertain send instead of resubmitting an approval. Native command approvals and blocking questions are separate from MCP's advisory `sandbox_request_review` workflow. Do not treat an advisory review as native execution permission.

In Settings → Notifications, the owner chooses timing per category. Agent questions and approvals support immediate or off because they may expire. Inbound email, voicemail, missed calls and chat replies support immediate, digest or off; digests run every 15 minutes, hourly or daily. Live call ringing is a separate device control, not a delayed call alert. Turning ringing off preserves the saved line and leaves carrier voicemail routing in place. In the phone pilot, email alerts open the existing web Inbox for review; the native Inbox handles connected-agent requests. Notification settings do not release messages to an Agent.

Notifications depend on supported phone push configuration, iOS permission, an active connection and request expiry. Check the current request on opening an alert. Do not promise delivery or claim a Wi-Fi/cellular test passed without an observed result.

## Incoming calls and voicemail

Phone supports answering incoming calls and listening to voicemail. Sending a ringing call to voicemail requires a configured carrier mailbox for that same line. Rejecting a call alone does not create a mailbox. Current setup verifies an already-enabled Telnyx SIP mailbox and its signed event destination; it does not purchase a number or reroute calls automatically.

Keep carrier ownership explicit. A Claw Me sign-in is not a Telnyx login and does not transfer a phone or WhatsApp number. The phone's manually connected Telnyx line is bound to the exact Claw Me account; an old unbound saved line must be connected again by its owner. Prefer user-owned carrier accounts for new setups. Existing managed numbers require a separate reviewed carrier migration; do not reassign or unregister them based on a product sign-in. Telnyx delegated OAuth account linking is not yet integrated into this phone pilot. Do not promise a Sign in with Telnyx button that is not available or invent account-linking MCP tools. Help with supported setup while the owner completes terms, verification and billing actions.

Voicemail access requires a separate phone review with Claw Me. Existing phone or Agent grants do not expand automatically. The owner can listen, mark read/unread, archive and remove available messages. Claw Me message details expire after 14 days; carrier recording availability and retention are separate. Removing a message from Claw Me does not delete the carrier's copy. Recording availability also depends on a verified carrier download location.

Phone access does not release recordings to an Agent, start an Agent turn, transcribe audio or add content to memory. Do not invent voicemail MCP tools or treat a recording as approved context. Telnyx documents native voicemail for SIP-connected numbers; programmable eSIM voice is a separate capability. Confirm the particular mobile line's routing before offering voicemail on its eSIM number or Apple Visual Voicemail.
