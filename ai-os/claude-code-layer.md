# The Claude Code Layer

Claude Code configured as a business operating system rather than a coding assistant.

This is the layer that builds and drives everything else in this section. It is also the cheapest part to copy, because it is all plain markdown and JSON on your own machine.

Inventory date: 2026-07-29.

---

## 1. Six layers, six failure modes

The whole configuration stacks into six mechanisms. Each one behaves differently when it fails, and that is the reason to keep them separate.

- **Layer 1: Global CLAUDE.md.** An always-loaded constitution. Identity, hard rules, registries.
- **Layer 2: Skills.** 48 global plus 18 project-scoped. On-demand procedures loaded by name.
- **Layer 3: Agents.** 11 global plus 8 project-scoped. Fan-out workers with their own tool grants and models.
- **Layer 4: MCP servers.** Access to external systems.
- **Layer 5: Hooks and permissions.** Deterministic enforcement that does not depend on the model remembering anything.
- **Layer 6: Memory.** Per-project persistent facts, auto-written, index-linked.

The organizing rule:

> [!TIP]
> Anything that must never be forgotten goes in Layer 1 or Layer 5. Anything that is a repeatable procedure goes in Layer 2. Anything that is parallelizable goes in Layer 3.

Layer 1 is instruction. Layer 5 is enforcement. Confusing the two is the most common configuration mistake. A rule in CLAUDE.md is a strong suggestion. A rule in the deny list is a wall.

---

## 2. CLAUDE.md as an operating system

The global file is roughly 16 KB across sixteen top-level sections. The ordering is not accidental. Identity first, then what to build on, then how to behave, then what tools exist, then when to act without asking.

Sections, in file order:

- **Identity and business.** Who the company is, what it sells, the stack, one stated core principle. Plus a naming rule: the agent refers to itself by a fixed persona name in all written output, never as "Claude".
- **Project registry.** Named repos with absolute paths and one-line purposes, split into production and active. This is the map that lets a cold session find anything.
- **Knowledge layer.** Points at the vault, with a standing auto-capture rule: when real operational information surfaces in any project, write it to the vault without asking. This is the highest-value instruction in the file, because it turns every session into an ingestion event.
- **Work philosophy.** Six principles. Parallelize only when it pays. Prefer existing libraries over custom builds. Batch repetitive edits instead of looping. Auto-validate on completion. Read docs before using an unfamiliar API. Build progressively, never duplicate.
- **Hard rules.** About fifteen absolute prohibitions and requirements. Formatting bans, credential bans, path requirements, batching requirements.
- **Communication.** Response length, lead with the answer, absolute clickable file paths with line numbers, banned punctuation, banned metaphors.
- **Code quality.** Read before write. Edit existing files over creating new ones. Keep changes minimal. No speculative error handling. No compatibility shims. Delete dead code completely.
- **Git.** Commit only when asked. Explain why, not what. Stage specific files, never stage everything. Never force push or amend published commits.
- **Documentation.** One job per document. Link instead of copying. Update facts at the source.
- **Agent registry.** Every globally available subagent, name and one-line purpose.
- **Skill registry.** Every global skill, name, invocation syntax, one-line purpose.
- **MCP notes.** Which servers exist, what each is for, and the rate limit rules.
- **Issue tracker rules.** Label taxonomy, which skills auto-create issues, identifier conventions.
- **Skill auto-triggers.** The most unusual section. A long list of situational patterns mapped to skills, with a standing instruction to surface the relevant skill in one line rather than waiting to be asked.
- **When to ask versus proceed.** An explicit split. Destructive operations, externally visible actions, ambiguous requirements, and unverified proper nouns require asking. Reading, linting, in-scope edits, and proposing plans do not.

**Four patterns worth taking:**

**Registries inside the constitution.** The skill and agent registries live in CLAUDE.md, not only on the filesystem. The model knows what exists before it goes looking. Discovery costs zero tokens.

**A proper-noun rule.** Never guess brand names, entity names, or proper nouns. Ask if unsure. Hallucinated names are the most expensive failure mode in client work, and it is a category the model is confidently bad at.

**Formatting bans as authorship signature.** No em dashes, no markdown tables, no emojis, no specific overused metaphors. They read as style rules. They function as a consistency mechanism across everything the system produces.

**An explicit autonomy boundary.** The ask-versus-proceed split removes friction in both directions: over-asking on safe work, and under-asking on irreversible work.

Project-level CLAUDE.md files layer domain rules on top. The business repo's version adds folder structure rules, a progressive-documents doctrine with worked good and bad examples, an internal-versus-client-facing separation rule, and the no-tables rule restated with five concrete substitutions.

---

## 3. The skills library

66 skills total: 48 global, 18 project-scoped. Plus 12 enabled plugins pulling in another two dozen.

Each skill is a directory holding a `SKILL.md` with YAML frontmatter carrying `name`, `description`, and often `argument-hint` and `allowed-tools`. Heavier skills add `references/`, `scripts/`, and `examples/` subdirectories so the instruction file stays short and the payload only loads when needed.

> [!IMPORTANT]
> Skill descriptions are written as **trigger lists, not summaries.** A typical description ends with six to ten literal phrases the user might say. The description is a routing surface, not documentation. This is the single thing that decides whether a large skill library gets used or becomes shelfware.

Grouped by what they do:

**Engineering lifecycle.** session-start, prime, map-codebase, plan, refactor, scaffold, fix, test, verify, review, audit, deploy-check, commit, changelog, deps, env-sync, snapshot.

**Stack specific.** supabase, seo, perf, api-doc, n8n, onboard-dev.

**Research and knowledge.** research, exa, context7, watch, extract, transcript.

**Vault operations.** ingest, query, lint, and the enrichment loop. Callable from any project. Covered in [vault.md](vault.md).

**Business operations.** Client onboarding, discovery call processing, scope and proposal document generation, an internal pricing calculator, engagement status, handoff packages, a priorities war room, issue tracker CRUD, and system design mapping.

**Writing.** Site copy, cold outreach copy, founder-voice sequences, an AI-writing-tell remover built from a public taxonomy of signs of AI writing, social scripts, and lead magnet generation.

**Design and document generation.** Excalidraw diagrams, technical diagram export, an anti-templated frontend skill, a design MCP wrapper, branded deck generation, a deck audit-and-fix cycle, a cumulative research cycle, and social video production.

**Meta.** Skill and agent creation, task decomposition into parallel subagents, and a rules-reloading skill.

### Two meta-patterns

**The loop-body skill.** Four skills are written as a single idempotent iteration meant to be driven by an interval runner. Each one picks the highest-value next action, does it end to end, and terminates. The runner supplies the repetition.

That composition gives you continuous improvement with no long-running process to babysit, no drift across a marathon session, and a natural review point after every iteration. If you write one pattern from this whole document, write this one.

**The gate check.** The copy skills refuse to present output until a named checklist passes. The constraint lives inside the procedure, not in the operator's head. A skill that can say no to itself is worth five that cannot.

**The proactive-capture rule.** The skill-creation skills are instructed to trigger on their own: if a workflow has been executed twice in one conversation, suggest capturing it. The library grows by noticing repetition instead of by remembering to write skills.

---

## 4. Agents

11 global, 8 project-scoped. Each is one markdown file with frontmatter carrying `name`, `description`, `tools`, `model`, `memory`, and `permissionMode`.

Two description styles are in use. Simple agents get one line. Complex agents get a description containing worked example blocks: a user request, the routing decision, and a commentary line explaining why that agent matched. Those examples exist to train invocation, not to explain the agent.

**Model and tool tiering is deliberate.** Research and generation agents run a mid-tier model. A pure structure validator runs the cheapest tier with read-only tools. A research agent gets web fetch, web search, read, write, grep, glob. A validator gets read, grep, glob and nothing else.

A validator does not need a frontier model or write access. Giving it both is how a review pass turns into an unrequested refactor.

Global agents by function: deep company analysis, discovery and competitor research, systematic root cause debugging, test writing against existing conventions, multimodal prompt construction, and comprehensive pre-production validation.

The debugger's framing is worth quoting as a pattern: diagnose what **is** wrong at runtime, not what **looks** wrong in code.

Project agents by function: document structure validation against the project rules, engagement directory scaffolding, and autonomous social video production that reads a brand reference before every run.

**The fan-out pattern shows up twice.** One competitive-landscape swarm runs four parallel research agents on separate tracks plus a fifth that merges the four reports into one analysis. One audit swarm runs three parallel agents over documentation, technology claims, and business gaps, plus a fourth synthesizer.

The shape both share: N independent investigators, one synthesizer, no shared state between the investigators. Parallelism on shared state is a bug, not a feature.

---

## 5. MCP servers

Names and purposes only. No endpoints, tokens, workspace identifiers, or config values.

**Configured globally, both remote OAuth:**

- **linear.** Issue tracker.
- **slack.** Team messaging.

**Additional servers present at runtime:**

- **Three separate Gmail servers**, one per mailbox role rather than one server handling every account. Splitting by role is the notable choice, because it lets rules and rate limits differ per channel and it makes a mistaken cross-mailbox action structurally harder.
- **claude-in-chrome.** Browser automation against an existing Chrome session.
- **computer-use.** Desktop screenshots and control for native apps.
- **shadcn.** Component registry search and install. A standing rule names this as the only component source, with hand-rolled primitives banned.
- **cloudflare-bindings.** Edge platform bindings.
- **Managed connectors** for CRM, design, mail, calendar, drive, notes and docs, and a generative media platform.

**Custom, built in-house:** a zero-dependency stdio MCP server, about 400 lines of Node standard library, that wraps the dashboard's own REST API as tools. Any Claude Code session on the machine can then drive the AI OS. Sixteen tools: approve or deny queued actions, list agent runs, read and clear notifications, read inbox threads, queue an email action, re-triage a message, pull the overview, and search, read, write, and tree the vault.

It registers with one `claude mcp add` command pointing at the script. The dashboard has to be running for the tools to work.

That is the general move worth copying. If you already have an internal API, wrapping it as an MCP server is a few hundred lines with no dependencies, and it turns your app into something the agent can operate.

**The tiering rule that governs all of them.** For any task: a dedicated MCP for the target app first. Browser automation second, for web apps with no dedicated server. Desktop control last, and only for native apps and cross-app workflows.

That order prevents the common failure of driving a web app through pixel clicks when an API exists three feet away.

**Documented mail rate rules**, because these servers will hit limits before anything else does: batch reads capped at ten messages, sends capped at ten per minute, metadata-only format when headers are all you need, and thread fetch preferred over individual message fetch.

---

## 6. Hooks and permissions

The layer that does not depend on the model cooperating.

### Permissions

Three lists in settings: 79 allow, 32 deny, 19 ask.

- **Deny** is a hard block. Recursive deletes of root, home, parent, current directory, and named source folders. Disk-level commands. Force push in both flag forms. Uninstalling framework-critical packages. Deleting git metadata, lockfiles, and config files. Sudo variants of destructive commands. Process kills by name.
- **Ask** is the reversible-but-consequential tier. Push, publish, reset, rebase, merge, dependency updates, database push and reset, container commands, service management, sudo, kill, ownership changes.
- **Allow** is the large routine tier: read and build commands that would otherwise generate constant prompts.

The design principle: deny what can destroy work, ask for what is externally visible or hard to undo, allow everything else so you are not answering prompts all day. A permission system people click through is not a permission system.

### Declarative hook rules

Eight rules, each a markdown file with frontmatter carrying a name, an enabled flag, an event type (bash, file, or prompt), a regex pattern or condition list, and an action of block or warn. The body is the message shown when it fires.

**Blocking:**

- Destructive recursive delete against root, home, parent, or a bare current directory.
- Force push in either flag form.
- Hardcoded secrets, matched as a credential-looking key name followed by a sixteen-plus character quoted string.
- Any write to a file matching an env-file pattern.

**Warning:**

- Debug statements in written content.
- Commands referencing production.
- Blocker language in a prompt, which nudges an issue tracker status update.
- Completion language in a prompt, which nudges closing the relevant issue.
- Transcript or call-notes language in a prompt, which nudges running the discovery skill.

The prompt-event rules are the interesting half. Three of the eight are not safety rails at all. They are workflow nudges that read my own phrasing and remind the system to keep the issue tracker in sync.

Process compliance enforced by regex on natural language. No amount of instruction achieves this reliably. A regex does.

### Session hooks and the multi-pane bus

Three hooks are wired: session start, prompt submit, and stop. All three point at scripts in a shared directory, and together they implement a manual multi-agent orchestration layer over tmux.

```
   PANE 0                    PANE 1, 2, 3
+--------------+          +-----------------+
| orchestrator |          |   worker-1..3   |
+------+-------+          +--------+--------+
       |                           ^
       |  dispatch script          |
       |  (tmux send-keys, or      |
       |   queue a task file)      |
       +---------------------------+
       |
       |  Stop hook on each worker extracts its
       |  final message to reports/unread/
       v
+--------------------------------------------+
|  ~/.claude/bus/                            |
|  inbox/  reports/unread  reports/read      |
+--------------------------------------------+
       |
       |  UserPromptSubmit hook on the orchestrator
       |  sweeps unread reports into context
       v
   back to PANE 0
```

How it works:

- Every script no-ops unless a role environment variable is set, so normal sessions on the machine are unaffected.
- As orchestrator, the session-start hook injects a role briefing: you coordinate three worker sessions in other panes, here is how to dispatch, worker reports will arrive automatically. It explicitly warns that workers share no context, so every dispatch must carry the working directory, the files, the constraints, and the exact deliverable.
- As a worker, the same hook briefs the session that its final message each turn is its only channel back. Every task has to end with a concise report: what was done, files touched, commands run, open questions.
- The dispatch script sends a prompt to a registered pane if one exists, and otherwise queues a task file in a per-worker inbox.
- The stop hook, active only for workers, parses the session transcript, extracts the last assistant message, and writes it to an unread reports directory.
- The prompt-submit hook, active for the orchestrator, injects those unread reports into context on the next prompt.

The premise is that sessions in different terminals share nothing except the filesystem and hooks, and that is enough. Four panes, three shell scripts, no framework.

### Plugins and statusline

12 plugins enabled across 4 marketplaces: feature development, hook authoring, security guidance, frontend design, code review, PR review, commit commands, agent SDK scaffolding, setup recommendations, CLAUDE.md maintenance, and skill creation.

The statusline is a shell command that reads session JSON and renders platform, model display name, current directory basename, and git branch.

---

## 7. Memory

Memory is per project, stored under a per-project directory. 27 projects currently carry one. The largest holds 87 files.

**The structure is an index file plus atomic notes.** `MEMORY.md` is a categorized list of one-line summaries, each linking to a dedicated file holding the detail. Nothing lives only in the index. The index exists so a cold session can scan every fact it might need in one read, then load only the two or three files that matter.

**Filenames are typed by prefix.** Counts from the largest memory directory:

- `feedback_` (40). Corrections and standing preferences.
- `project_` (19). Per-workstream state.
- `reference_` (13). Stable facts about tools, systems, and setups.
- `client_` (9). Per-engagement facts.
- `user_` (2), `content_` (1), `corporate_` (1), `bug_` (1).

> [!TIP]
> The dominance of `feedback_` is the finding. Two thirds of what this system remembers is not project state. It is corrections. Every time I push back on an output, the correction becomes a durable file and a line in the index.

That is the pattern to copy. Most people treat agent memory as a project journal. The higher-value use is a correction log, because corrections are the thing the model has no other way to learn and the thing you are most tired of repeating.

**Agent memory is separate.** A per-agent directory tree lets subagents declared with user-scoped memory accumulate their own context across runs, independently of the main session.

---

## 8. Ten principles that generalize

1. **Put the map in the constitution.** Registries of skills, agents, and repos live in the always-loaded file. Discovery costs nothing.
2. **Write skill descriptions as trigger lists.** Ten literal phrases beats one accurate summary. Descriptions are for routing.
3. **Encode the autonomy boundary explicitly.** A written ask-versus-proceed split eliminates both over-asking and dangerous under-asking.
4. **Separate mechanism by failure mode.** Never-violate rules become permission denies and blocking hooks. Usually-hold rules become CLAUDE.md text. Procedures become skills.
5. **Use hooks for workflow, not just safety.** Regex on your own phrasing enforces process compliance that instruction does not.
6. **Make memory a correction log.** The highest-value persistent memory is every correction ever issued, stored atomically and indexed.
7. **Write loop-body skills.** One highest-value iteration that exits, composed with an interval runner, gives continuous improvement with nothing to babysit.
8. **Gate output behind a checklist inside the skill.** Quality constraints belong in the procedure, not in your head.
9. **Tier models and tools per agent.** A structure validator does not need a frontier model or write access.
10. **Reload rules instead of trusting recall.** A dedicated skill exists purely to re-read project standing rules and surface conflicts with in-chat instructions, because constraints demonstrably drift over long sessions.

---

Built by OperatorOS | [operatoros.ai](https://operatoros.ai)
Follow [@daviss.dev](https://instagram.com/daviss.dev) and [@os.operator](https://instagram.com/os.operator) on Instagram.
