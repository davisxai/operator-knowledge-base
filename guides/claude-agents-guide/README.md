# Claude Agents: The Practical Guide

> Follow @os.operator on Instagram for more guides like this.

---

## What You'll Have When You Finish This

Three real SKILL.md files you can paste into Claude today. A working pattern for running 3-5 agents in parallel without burning your monthly quota. A list of the exact MCP integrations worth installing first, with the install commands. The honest list of where this breaks and how to recover.

You walk away with skills installed, agents running, and a clear next move.

---

## The Mental Model

An agent is a Claude session that runs its own loop: read context, plan, execute with tools, evaluate, repeat until the goal is hit. You give it the destination. It picks the route. Same model on Claude Desktop and Claude Code. Same SKILL.md format runs in both. The Skills standard was adopted across Cursor, GitHub Copilot, Codex, Gemini CLI, and 20+ other tools, so the playbooks you write here aren't locked to one app.

Running one agent isn't the point. The point is running five at once, each in its own context window, each following the same playbook. That's where the time savings actually land. Parallel subagents collapse multi-file work that would take a single thread all afternoon. They also burn several times the tokens of a single thread, so use them where the work is genuinely independent (5 audits, 5 research tracks, 5 reviews) and use one agent where the work is sequential.

---

## Desktop or Code? The Honest Map

We run client work on both. The split is permission-based, not preference-based.

**Use Claude Desktop (Cowork) for:**
- Email triage, calendar work, Slack/Notion/Linear actions
- Reading and summarizing folders of documents
- Recurring reports that run on a schedule
- Anything where the agent should not touch your operating system

**Use Claude Code for:**
- Anything inside a git repository
- Anything that needs to run shell commands beyond a sandbox
- Multi-agent swarms where you want to spin up 5-10 subagents at once
- Server work, deployment, infrastructure

The honest line on permissions: Claude Code can do things Cowork won't. Modify your operating system. Deploy code. Change git history. Run any shell command. Cowork runs in a local VM sandbox, which is safer and slower. If your work is documents and integrations, Desktop is the right entry point. If your work touches the filesystem at depth, you need Code.

---

## The 5 Skills to Write First

Skills are Markdown files with YAML frontmatter. They tell any compatible agent how to handle a specific task. Save globally at `~/.claude/skills/<name>/SKILL.md` and they follow you across every project. Save at `.claude/skills/<name>/SKILL.md` inside a repo and your team gets them too.

Below are three real SKILL.md files that work in production. Paste these into your `~/.claude/skills/` and they run immediately. The other two are named with descriptions so you know what to build next.

### Skill 1: /extract

Paste any messy input. Get structured decisions, action items, facts, and open questions back. Pays back the first time you process a call transcript or a Slack dump.

```markdown
---
name: extract
description: Extract decisions, action items, facts, and open questions from messy input. Voice transcripts, meeting notes, Slack dumps, email threads. Use when the user says "extract from this", "what did we decide", "action items from this", or drops unstructured text.
---

Process the input through four passes.

Pass 1 - Decisions
Find every moment something was decided. Format: who decided what. Include the reasoning if it was given.

Pass 2 - Action Items
Pull every commitment to do something. Format: who is doing what, by when if stated. Mark "TBD" if no owner.

Pass 3 - Facts
Surface concrete facts stated: numbers, dates, names, claims worth verifying. One bullet per fact.

Pass 4 - Open Questions
List unresolved questions explicitly raised or implied by incomplete decisions.

Output four sections in that order. Skip a section if empty. Do not pad. Do not interpret beyond what was said.
```

**First run:**
> Paste your most recent meeting transcript into Claude and type `/extract`. You'll get a clean structured output in 10 seconds. Save it as your meeting notes template forever.

### Skill 2: /research

Deep research that spawns parallel subagents to investigate different angles, then synthesizes the findings. Works in both Desktop and Code. The skill includes the parallel pattern, so you don't have to write the prompt.

```markdown
---
name: research
description: Deep research with parallel discovery. Web, codebase, alternatives. Use when the user says "research this", "look into", "compare options for", "what's the best way to", "find out about", or when a technical or business decision needs evidence before committing.
---

Run research as a parallel investigation.

Step 1 - Frame
Restate the question in one sentence. List 3-5 sub-questions that, if answered, would settle the main question.

Step 2 - Parallel Investigation
Spawn one subagent per sub-question using the Task tool. Each subagent investigates its track independently and returns findings as structured notes.

Step 3 - Synthesis
Compile findings into one report with these sections:
  - TL;DR (3 sentences max)
  - Key Findings (bullet list, each with source if external)
  - Tradeoffs (where evidence conflicts or depends on context)
  - Recommendation (one clear pick, with reasoning)
  - Sources (links if web research)

Be specific. Name tools, cite numbers, link sources. If a sub-question can't be answered with confidence, say so explicitly. Do not invent.
```

**First run:**
> `/research what's the best AI transcription tool for a 1-person operator in 2026 - accuracy, speed, cost.`
> You'll see 3-5 subagents fire off, then a clean synthesis with a single recommendation.

### Skill 3: /recurring-report

For Claude Desktop's scheduled tasks (shipped April 2026). Set this up once, and a report lands in your inbox every Friday at 9am, compiled from real sources.

```markdown
---
name: recurring-report
description: Compile a recurring status report from multiple data sources. Schedule with Claude Desktop's task scheduler. Use when the user says "weekly report", "status summary", "recurring report", or wants to automate something they currently do manually each week.
---

Build the report in three phases.

Phase 1 - Source Pull
Read from each configured source in parallel. Default sources to look for unless overridden:
  - Gmail (last 7 days, filtered by labels the user provides)
  - Notion (a specific database or page if specified)
  - Linear (current cycle issues, status changes)
  - GitHub (PRs merged, issues closed)

Phase 2 - Compile
Group findings by source. Within each group:
  - Highlights (3-5 bullets max)
  - Open items (anything blocked, pending decision, or stale)
  - Notable numbers (counts, totals, percentages)

Phase 3 - Format
Output in the user's template format. Default template if none provided:
  - This Week's Wins
  - In Progress
  - Blocked / Needs Decision
  - Numbers
  - Next Week's Focus

End the report with a one-line summary of the most important thing. Save the output to the destination the user specifies (Notion page, email draft, file).
```

**First run:**
> In Claude Desktop, open the Scheduled Tasks panel. Create a new task: `/recurring-report from Gmail labeled "client" and my Linear active cycle. Format as my standard Friday report. Run every Friday at 9am.`

### Skill 4: /audit (named, write yourself)

Multi-track health check. Spawns parallel subagents across different audit dimensions (deps, tests, types, dead code, secrets, accessibility for code; or for non-code, against a checklist of your choice). Each track returns findings. Parent agent compiles a single report with priorities.

### Skill 5: /swarm (named, write yourself)

Decompose a complex task into parallel subagents. The skill writes the orchestration plan, creates the agent definitions, and spins them up. Power-user move. Best when the task has 3+ independent workstreams.

---

## Three Subagent Patterns That Pay Back Immediately

Patterns are prompts you can paste verbatim and get reliable agent behavior. The skill is in the structure of the prompt.

### Pattern 1: Parallel Research Across Independent Tracks

Use when researching 3-5 things that don't overlap. Example: competitor analysis, feature comparison, vendor evaluation.

```
Spawn N subagents in parallel using the Task tool.
Each one investigates exactly one item from this list:
  - [item 1]
  - [item 2]
  - [item 3]

Each subagent should research independently, focusing on:
  - What it does (one paragraph)
  - Pricing as of today
  - Best use case
  - Worst use case
  - One non-obvious tradeoff

Return findings as a structured note. After all subagents finish,
synthesize a comparison table and recommend the best option for [your context].
```

### Pattern 2: Cross-Checking a Decision

Use when you're about to commit to something and want a sanity check from independent perspectives.

```
I'm about to [the decision]. Before I commit, spawn 3 subagents:

Subagent 1: Argue the strongest case FOR this decision.
Subagent 2: Argue the strongest case AGAINST this decision.
Subagent 3: Identify what I'm not considering that should matter.

Each runs independently. After they finish, synthesize the
strongest 2-3 risks I should address before committing, and the
strongest 2-3 reasons this is the right call.
```

### Pattern 3: Pre-Commit / Pre-Send Validation (Code or Email)

Use before publishing anything that matters. Each track checks one dimension.

```
Run 4 parallel checks on [the artifact]:

Track 1: Find any factual or technical error.
Track 2: Find any tone or voice inconsistency with [your reference doc].
Track 3: Find anything redundant, padded, or unnecessary.
Track 4: Identify the strongest one-line improvement.

Report each track's findings separately. Do not synthesize.
I'll decide which to address.
```

---

## MCP Integrations Worth Installing First

MCP servers are how agents reach outside Claude. Install these first. They open the largest surface area for the smallest effort.

**Gmail** (`@gongrzhe/server-gmail-autoauth-mcp`)
- Unlocks: read, search, label, draft, send email
- Install via Claude Desktop > Customize > MCP, or in `claude_desktop_config.json`
- First use: "Summarize every unread email from this week and draft a reply to anything client-related."

**GitHub** (`@modelcontextprotocol/server-github`)
- Unlocks: issues, PRs, code search, file ops in any repo you have access to
- First use: "Find every open issue labeled `bug` across my 3 repos and rank by recency."

**Filesystem** (`@modelcontextprotocol/server-filesystem`)
- Unlocks: read, write, search inside specified folders on your machine
- Scope it tightly. Point at one project folder, not your home directory.
- First use: "Read every PDF in this folder and summarize the contracts into one comparison table."

**Notion** (`@notionhq/notion-mcp-server`)
- Unlocks: read pages, query databases, create pages, update pages
- First use: "Find every Notion page tagged 'lead magnet' and summarize what topics we've covered."

**Linear** or **Slack** (official MCPs)
- Linear: query issues, update status, comment, create
- Slack: search messages, post messages, read channels
- First use: "Read every Slack message in #engineering from this week and pull out anything that became a Linear issue (or should be one)."

For Claude Code, install MCPs at the user scope so they work in every project: `claude mcp add <name>`. For Claude Desktop, add them in the Customize section.

---

## Where This Breaks (and How to Recover)

Production-honest failure modes:

**Subagent runs forever and burns tokens.**
- Why: the skill or prompt didn't bound the work clearly.
- Fix: every skill must say "what done looks like." If the subagent doesn't know when to stop, it won't.

**Parallel agents all wrote conflicting changes to the same file.**
- Why: parallelism on shared state is a bug, not a feature.
- Fix: parallelize where work is genuinely independent. Sequential for anything that touches the same target.

**The agent hallucinated a tool or skill name.**
- Why: it was operating from training, not your actual configuration.
- Fix: name your skills explicitly in the prompt. "Use the /research skill" beats "research this."

**Cowork can't access a file.**
- Why: the VM sandbox doesn't have the path mounted.
- Fix: drag the file into the chat, or grant the folder explicitly in Settings.

**Skill works on Claude Code but not on Claude Desktop.**
- Why: the skill probably used a tool that doesn't exist in Cowork (often Bash).
- Fix: either restrict the skill to Code via the `allowed-tools` frontmatter, or rewrite the action to use MCP tools instead of shell commands.

**Token bill spiked unexpectedly.**
- Why: a parallel pattern fired more subagents than intended, or a skill is reading the same files repeatedly.
- Fix: add usage caps in the Claude API console. For Pro users, watch the daily indicator at the bottom of the app.

---

## Day 1, Day 7, Day 30

**Day 1 (next 30 minutes)**
- Paste `/extract` into `~/.claude/skills/extract/SKILL.md` (Code) or import into Desktop Skills panel.
- Run it on the messiest piece of text you've received this week.
- Install one MCP server (Gmail or Filesystem). 5 minutes.

**Day 7**
- You've written 2-3 more skills based on tasks you found yourself repeating.
- You've run at least one parallel subagent pattern. You've watched 3-5 agents fire at once.
- You've scheduled one recurring task on Claude Desktop.

**Day 30**
- Your skills directory has 5-10 skills. You stop typing long prompts.
- You're routing the right work to the right app (Desktop for documents, Code for repos).
- You've explored the GitHub `gh skill` CLI or the community skill library to install someone else's playbook.

The compound starts at week 4. Most people quit at day 3 because the first skill takes 20 minutes to write and feels slower than just typing the prompt. The second one takes 10 minutes. The fifth one takes 2. By month 2, you're not writing skills anymore. You're running them.

---

Built by OperatorOS | [operatoros.ai](https://operatoros.ai)
Follow [@os.operator](https://instagram.com/os.operator) for production-grade AI guides.

---

## Sources

- [Agent Skills - Claude API Docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Anthropic launches Cowork — VentureBeat](https://venturebeat.com/technology/anthropic-launches-cowork-a-claude-desktop-agent-that-works-in-your-files-no)
- [Create custom subagents - Claude Code Docs](https://code.claude.com/docs/en/sub-agents)
- [Use Agent Skills in VS Code](https://code.visualstudio.com/docs/copilot/customization/agent-skills)
- [gh skill CLI announcement](https://github.blog/changelog/2026-04-16-manage-agent-skills-with-github-cli/)
