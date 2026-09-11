# AgentMail distribution and Claw Me plugin comparison

Research date: 11 September 2026. Scope: AgentMail.to, the company behind `agentmail-to` on GitHub. This is a public-source inventory, not a claim that every listing was submitted by AgentMail or that every install works today. Search indexes can lag; an indexed listing is weaker evidence than an opened page. Counts and directory security scores are not used as quality evidence.

## Top ten discovery destinations for an agent

Ranked by my practical usefulness for finding inspectable source and a concrete install path, not by traffic, market share or claimed download counts. Rechecked on 11 September 2026. Directory snapshots can lag the source; install the current official repository after inspecting it.

| Rank | Destination | Why I would use it |
| --- | --- | --- |
| 1 | [GitHub](https://github.com/agentmail-to/agentmail-plugins) | Canonical plugin files, history, validation and client manifests; best place to verify what is actually installed. |
| 2 | [skills.sh](https://skills.sh/agentmail-to/agentmail-skills/agentmail) | Official-source skill discovery with a direct cross-client install command. |
| 3 | [Cursor Marketplace](https://cursor.com/marketplace/agentmail) | Native plugin installation with bundled skills and MCP; strongest fit for Cursor users. |
| 4 | [ClawHub](https://clawhub.ai/agentmail) | Official AgentMail publisher and OpenClaw distribution; inspect the publisher to avoid community namesakes. |
| 5 | [Playbooks](https://playbooks.com/skills/agentmail-to/agentmail-skills/agentmail) | Readable skill body, upstream link and install command. |
| 6 | [Claude Skills Hub](https://claudeskills.info/skills/agentmail-to/agentmail-skills/agentmail/) | Official-source skill text with client-specific installation guidance. |
| 7 | [Agent-Skills.md](https://agent-skills.md/skills/agentmail-to/agentmail-skills/agentmail) | Repository attribution and skill-file navigation make source inspection straightforward. |
| 8 | [explainx.ai](https://explainx.ai/skills/agentmail-to/agentmail-skills/agentmail) | Searchable skill profile with installation guidance across clients. |
| 9 | [AwesomeSkill](https://awesomeskill.ai/skill/agentmail-to-agentmail-skills-agentmail) | Source-linked skill profile and file/download discovery; do not treat its risk score as an audit. |
| 10 | [ClaudeMarketplace.net](https://www.claudemarketplace.net/skills/agentmail) | Additional verified listing with full skill text and official-source installation command; independent of Anthropic. |

Ranks 5–10 are third-party discovery pages, not proof of official submission or native plugin packaging. All six pages were opened during the follow-up. SkillsMP is useful for broader community discovery, but the verified AgentMail entries in this audit are community variants, so it is outside this official-source shortlist.

## Finding

Claw Me already has comparable multi-client packaging. Its remaining competitive gaps are task-specific discovery, distribution reach, and recorded authenticated client tests. AgentMail has stronger email-specific workflow coverage; Claw Me serves a broader owner-controlled workspace product and should not copy unsupported outbound-email capabilities.

Sources inspected: [AgentMail plugin source](https://github.com/agentmail-to/agentmail-plugins) at `85df44be63eeaef0d8c0f1cd86121212f878ce05`; [Claw Me plugin source](https://github.com/clawdotme/plugin) at `bc738950042369ad63533038c66817ba3fe06e98`. Claw Me plugin version is 0.5.5, its independently versioned skill bundle is 1.1.6. AgentMail plugin version is 0.3.0.

| Dimension | AgentMail | Claw Me assessment |
| --- | --- | --- |
| Native packaging | Codex, Claude Code, Cursor, Open Plugins manifests and hosted MCP | Comparable structure already present. |
| Portable distribution | Canonical skills repository exported into plugins | Canonical public bundle plus exact Skills CLI mirror; sync check passes. |
| Workflow discovery | Eight installed skills: SDK, CLI, MCP, toolkit, patterns, sending, reading, inbox administration | One 142-line entrypoint with conditional references. Concise enough; product workflows are less individually discoverable. |
| First-use guidance | Short task-specific steps, operation names, examples and recovery constraints | Added six README task examples and a client verification/troubleshooting guide. |
| Email functionality | Direct send/reply/forward and inbox administration | Intentionally narrower launch contract: released inbound content and separately enabled owner-only delivery. Not email feature parity. |
| Trust boundaries | Current send/read skills distinguish user authority from message content and reconcile uncertain sends | Comparable explicit boundaries, plus pinned bundle hashes, scoped access and reviewed changes. This is a documentation comparison, not a security audit. |
| Validation | Structural validator, SDK signature and webhook test files | Manifest/contract checks, integrity, mirror consistency, secret hygiene, SHA-pinned CI and CLI discovery already present. Full local validation passed. |
| Client evidence | Public Cursor listing; first-party client setup instructions | Compatibility metadata says “manifest,” appropriately. Authenticated end-to-end tests across clients were not run in this audit. |
| Distribution | Verified native listings plus a broad directory footprint below | Public GitHub installation exists; README explicitly does not claim a Cursor marketplace listing. |

Claw Me's CI action revisions are SHA-pinned; the inspected AgentMail validation workflow uses version tags. Conversely, AgentMail's SDK/webhook test files address implementation examples that Claw Me's package does not ship. Neither observation establishes an overall quality score.

## Official sources and native distribution

“Opened” means the page was fetched during this audit; “indexed” means a concrete listing with identifying content appeared in search. GitHub sources were also cloned for inspection. These are distribution surfaces, not independent installations.

| Website | Specific source/listing | What is published | Evidence |
| --- | --- | --- | --- |
| GitHub | [agentmail-plugins](https://github.com/agentmail-to/agentmail-plugins), [agentmail-skills](https://github.com/agentmail-to/agentmail-skills), [older Claude skill](https://github.com/agentmail-to/agentmail-claude-skill) | Official native plugin and canonical skills; older standalone source also exists | Plugin cloned; skill repositories indexed |
| Cursor | [Plugin](https://cursor.com/marketplace/agentmail), [SDK skill supplied by the user](https://cursor.com/marketplace/skills/agentmail) | Native marketplace plugin and individual skill surface | Skill opened; plugin indexed; first-party Cursor guide corroborates |
| ClawHub | [Official AgentMail organization](https://clawhub.ai/agentmail), [official directory](https://clawhub.ai/official) | Official OpenClaw plugin, `clawhub:@agentmail/agentmail` | Both opened; [AgentMail installation docs](https://www.agentmail.to/docs/integrations/openclaw) independently confirm |
| skills.sh | [AgentMail SDK](https://skills.sh/agentmail-to/agentmail-skills/agentmail), [email patterns](https://www.skills.sh/agentmail-to/agentmail-skills/agent-email-patterns) | Installable skills from the official repository | SDK opened; patterns indexed |
| agentmail.to | [Skills documentation](https://www.agentmail.to/docs/integrations/skills), [Cursor guide](https://www.agentmail.to/build/cursor), [Claude Code guide](https://www.agentmail.to/build/claude-code) | First-party installation and distribution guidance | Indexed; OpenClaw documentation opened |

Claude Code and Codex are supported install targets through AgentMail's GitHub-hosted marketplace. This does **not** establish a separate listing in Anthropic's curated directory or OpenAI's curated catalog. No such listing was verified. The plugin repository includes a vendor-neutral manifest; a manifest alone is not evidence of publication on another website.

## Third-party directories carrying official-source skills

These pages identify `agentmail-to/agentmail-skills`; that identifies the upstream author, not the party who submitted the directory entry. Old aliases and cached content should not be installed in preference to the current canonical source.

| Website | Listing | Evidence / qualification |
| --- | --- | --- |
| ClaudeMarketplace.net | [agentmail](https://www.claudemarketplace.net/skills/agentmail) | Opened during follow-up; independent directory with official-source skill text |
| Playbooks | [agentmail](https://playbooks.com/skills/agentmail-to/agentmail-skills/agentmail) | Indexed; displays skill text and installer; snapshot has older SDK examples |
| Claude Skills Hub | [agentmail](https://claudeskills.info/skills/agentmail-to/agentmail-skills/agentmail/) | Indexed; current-style SDK routing and references |
| AwesomeSkill | [agentmail](https://awesomeskill.ai/skill/agentmail-to-agentmail-skills-agentmail) | Indexed; downloadable source snapshot |
| SkillJury | [agentmail](https://www.skilljury.com/skills/agentmail) | Indexed; review/discovery profile referring to skills.sh |
| AgentSkills.so | [agentmail](https://agentskills.so/skills/agentmail-to-agentmail-skills-agentmail) | Opened; hosted skill text and ZIP; older content |
| ClaudeMarketplaces | [agentmail-sdk](https://claudemarketplaces.com/skills/agentmail-to/agentmail-skills/agentmail-sdk) | Opened via CrossAITools redirect; deprecated alias |
| Agent-Skills.md | [AgentMail SDK](https://agent-skills.md/skills/agentmail-to/agentmail-skills/agentmail) | Indexed; source and install command |
| Skillselion | [agentmail-toolkit](https://skillselion.com/skills/agentmail-to/agentmail-skills/agentmail-toolkit) | Indexed; framework integration skill |
| Skills Playground | [agentmail](https://skillsplayground.com/skills/agentmail-to-agentmail-skills-agentmail/) | Indexed; abbreviated profile and Playbooks command, not demonstrably a full maintained bundle |
| xix.ai | [agentmail](https://xix.ai/skill/detail/agentmail.html) | Indexed; official-source skill profile |
| explainx.ai | [agentmail](https://explainx.ai/skills/agentmail-to/agentmail-skills/agentmail) | Indexed; official-source installation profile |
| Elite AI Tools | [agentmail-cli](https://eliteai.tools/agent-skills/agentmail-cli), [agentmail-mcp](https://eliteai.tools/agent-skills/agentmail-mcp) | Indexed; official source installation links |

CrossAITools is an additional historical URL, [here](https://crossaitools.com/skills/agentmail-to/agentmail-skills/agentmail-sdk), which now redirects to ClaudeMarketplaces; do not count it as an independent active destination.

## Community skills and mirrors for AgentMail.to

These are evidence of ecosystem presence, not the official multi-client plugin. The same website can carry official-source and unrelated same-name skills: check the upstream repository and API domain on each entry.

| Website | Listing | Publisher/source and evidence |
| --- | --- | --- |
| ClawHub | [adboio audit/listing context](https://clawhub.ai/adboio/agentmail/security/openclaw), [CLI](https://clawhub.ai/stepandel/skills/agentmail-cli), [Python helper](https://clawhub.ai/lausser/skills/python-agentmail-send-receive), [Email](https://clawhub.ai/davidsteelerose/k2ljl-agentmail), [temporary inbox variant](https://clawhub.ai/liguang00806/agentmail-temp) | Indexed legacy/community packages; separate from official @agentmail plugin |
| ClawSkills.sh | [adboio-agentmail](https://clawskills.sh/skills/adboio-agentmail) | Indexed ClawHub mirror, v1.1.1 |
| DiscoverAISkills | [AgentMail](https://discoveraiskills.com/skills/agentmail) | Indexed; explicitly sources ClawHub data. Some generic example prompts are inaccurate |
| SkillsMP | [Hermes AgentMail](https://skillsmp.com/creators/nousresearch/hermes-agent/optional-skills-email-agentmail), [Dynoclaw AgentMail](https://skillsmp.com/creators/adawodu/dynoclaw/skills-agentmail) | Indexed community repository skills |
| SkillIndex | [Hermes AgentMail](https://skillindex.io/skill/nousresearch-hermes-agent-optional-skills-email-agentmail) | Indexed community skill metadata |
| skills.rest | [agentmail](https://skills.rest/skill/agentmail) | Indexed; laurenzseifried/hektor-workspace source |
| AgentMagic | [agent-mail](https://agentmagic.com/skills/agent-mail) | Indexed; rimelucci author, @agentmail.to identity |
| MCP.Directory | [agentmail skill](https://mcp.directory/skills/agentmail) | Indexed; openclaw source, downloadable skill |
| browse.sh | [AgentMail Inbox](https://browse.sh/skills/agent.email/get-email-inbox) | Indexed; website skill for AgentMail API; official submission ownership not established |
| SkillHub | [agentmail-email](https://www.skillhub.club/skills/lightjunction-lightjunction-agentmail-email) | Indexed; personal LIghtJUNction mailbox workflow, not general official plugin |
| GitHub | [Hermes optional skill](https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/email/agentmail/SKILL.md) | Indexed; community runtime integration |

## MCP-only and reference listings

| Website | Listing | Qualification |
| --- | --- | --- |
| Glama | [AgentMail toolkit server](https://glama.ai/mcp/servers/%40agentmail-to/agentmail-toolkit), [Smithery connector profile](https://glama.ai/mcp/connectors/ai.smithery/agentmail) | Indexed MCP profiles; not evidence that the eight-skill plugin is bundled |
| PulseMCP | [Official AgentMail MCP Server](https://www.pulsemcp.com/servers/agentmail) | Indexed; explicitly calls its server.json a PulseMCP-managed mirror |
| LobeHub | [AgentMail MCP Server](https://lobehub.com/mcp/agentmail-to-agentmail-mcp) | Indexed, but live fetch returned 403; current availability not confirmed |
| Smithery | [AgentMail server URL](https://smithery.ai/servers/agentmail) | Opened only generic site content; Glama corroborates a connector. Treat current direct listing as unconfirmed |
| Context7 | [agentmail-skills](https://context7.com/agentmail-to/agentmail-skills) | Indexed reference profile reports failure fetching documentation; not a verified install destination |
| LinkedIn | [Official skills announcement](https://www.linkedin.com/posts/agentmailto_today-were-announcing-our-official-agentmail-activity-7452405942073135104-0ixy) | Indexed first-party announcement, not a plugin registry |

The inventory has 27 distinct domains across the first three tables (including Cursor, GitHub and the vendor site), plus six MCP/reference/announcement domains above. CrossAITools is a redirect, not a 34th active destination. These totals describe identified web presence, not 33 official publications. An exhaustive count of the open web cannot be guaranteed; private, unindexed and subsequently removed pages are outside this method.

## Excluded name collisions

- [UserAd/AgentMail](https://github.com/UserAd/AgentMail): local agent-to-agent messaging over Go/tmux, not AgentMail.to.
- [sickn33 skill](https://claudeskills.info/skills/sickn33/agentic-awesome-skills/agentmail/): explicitly uses `api.theagentmail.net`; also indexed by AISkillsify and SkillAtlas. Do not attribute to AgentMail.to.
- [MCP Market AI Email System](https://mcpmarket.com/tools/skills/agentmail-ai-email-system): describes `@theagentmail.net`, also excluded.
- [Glama kindrat86/agentmail](https://glama.ai/mcp/servers/kindrat86/agentmail): Mail.tm-backed verification toolkit.
- [Agents Mail](https://clawhub.ai/agents-mail/skills/agents-mail): explicitly identifies itself as agentsmail.org, a different provider.

## Recommended Claw Me next steps

1. Prioritize a Cursor native marketplace listing and verify official-source discovery on skills.sh. Existing manifests are a starting point; publication remains a separate action.
2. Evaluate ClawHub publication for the actual OpenClaw connector. A standalone skill is not equivalent to a runtime plugin/channel; preserve the existing public/private source boundary.
3. Keep one canonical reviewed skill source. If prompt trials show routing failures, add focused entrypoints for Pages, context, and email triage through the product-to-public sync pipeline. Do not duplicate all shared instructions just to match AgentMail's skill count.
4. Record real install/authorization/read evidence in Codex, Claude Code and Cursor before upgrading compatibility claims from “manifest” to “tested.” The new client-verification guide specifies the evidence.
5. Submit or correct a small set of high-relevance directories after canonical listings are ready. Link to the official repository, record listing ownership and refresh dates, and check copied claims for drift.

## Changes and verification in this audit

Added README task prompts with expected outcomes, explicit skill-only versus connection guidance, launch email limitations, and a client-verification/troubleshooting document. The canonical skill and permissions were not rewritten: their reviewed-source sync requirements remain intact. No listings were submitted and no runtime behavior was changed.

`./scripts/validate.sh` passed: exact skill mirror, 14-file bundle verification, plugin and contract checks, CI pinning, secret/privacy checks, template build, 11 tests, and pinned Skills CLI discovery. Authenticated account operations and marketplace installation were not exercised. No security or performance superiority claim is made.
