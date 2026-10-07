<p align="center">
  <img src="assets/banner.png" alt="Documents, emails, PDFs, and sheets flow into the agent and out into a knowledge graph" width="100%">
</p>

# Agent Vault Starter

> Follow [@daviss.dev](https://instagram.com/daviss.dev) and [@os.operator](https://instagram.com/os.operator) on Instagram for more guides like this.

---

### From an agent that forgets to a folder of markdown it maintains itself.

A public benchmark ran eight AI memory products through 2,176 tasks. A plain markdown wiki the agent curates itself scored 98.5. Every product came in below it. My company runs on exactly that architecture: a folder of markdown files with a schema, three layers split by who is allowed to write, an agent that captures during the day, and a second agent that consolidates at 3am.

This guide ships the whole thing as files. Copy the starter vault, open it in Obsidian, run the skills from Claude Code, and you have the system. It is not a note-taking tutorial. It is the contract, the schema, the operations, and the schedule.

---

## What you'll get

→ A complete starter vault you copy with one command: contract, schema, ten page templates, folder skeleton, index, hot file, log
→ Five vault operations as Claude Code skills: `/ingest`, `/query`, `/lint`, `/build`, `/dream`
→ The auto-capture rule that turns every Claude Code session on your machine into an ingestion event
→ The dream agent: a four-phase nightly consolidation pass, as a skill, as a standalone system prompt, and as a launchd job
→ A frontmatter validator that rejects any page failing the schema, no dependencies
→ Five worked workflows with the exact prompt, and a quick reference card

---

## Prerequisites

- [Obsidian](https://obsidian.md) as the viewer. Free for personal use. The vault is plain markdown, so any editor works, but Obsidian renders the wikilinks and the graph.
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed and logged in. The five operations are Claude Code skills.
- git, so the vault has history. `scripts/new-vault.sh` initializes a repo for you.
- Python 3 for the validator. Standard library only.
- macOS for the launchd job. On Linux, run the same command from cron.

---

## Contents

1. [Why a folder beat the products](#1-why-a-folder-beat-the-products)
2. [Install](#2-install)
3. [The mental model](#3-the-mental-model)
4. [Layout](#4-layout)
5. [The schema is the contract](#5-the-schema-is-the-contract)
6. [The five operations](#6-the-five-operations)
7. [Capture from every session](#7-capture-from-every-session)
8. [The dream agent](#8-the-dream-agent)
9. [Practical playbook](#9-practical-playbook)
10. [Cost and best practices](#10-cost-and-best-practices)
11. [Troubleshooting](#11-troubleshooting)
12. [Quick reference](#12-quick-reference)
13. [Sources](#13-sources)

---

## 1. Why a folder beat the products

On August 3, 2026, a developer posting as Major-Shirt-8227 published a benchmark on r/AI_Agents. One agent, eight memory systems swapped underneath it, 272 scored tasks each, 2,176 in total. Of the 272, 72 asked about facts that were never stored, to catch systems that invent memories.

A plain markdown wiki the agent curates itself, following Karpathy's llm-wiki pattern, scored 98.5. The best hosted product scored 96.9.

The reason it wins is the reason it is worth building. The agent can read the whole of what it knows with the same tools it uses for everything else. You can open any file and read what it believed when it got something wrong. There is no embedding step between a fact and the page that holds it.

What the benchmark does not give you is the structure that keeps a machine-written wiki trustworthy. That is what this starter is: the schema, the write rules, and the two agents that keep it current.

---

## 2. Install

Clone the knowledge base, then create your vault from the starter.

```bash
git clone https://github.com/davisxai/operator-knowledge-base.git
cd operator-knowledge-base/guides/agent-vault-starter
bash scripts/new-vault.sh ~/Documents/Vault
```

The script copies `templates/vault/`, stamps today's date into `index.md` and `hot.md`, writes the first log line, and runs `git init` with a first commit. It refuses to overwrite an existing folder.

Open the new folder in Obsidian as a vault. Then open Claude Code inside it:

```bash
cd ~/Documents/Vault
claude
```

Claude Code reads `CLAUDE.md` on start, which is the vault contract. The five skills under `.claude/skills/` are available immediately. Drop any file into `inbox/` and run your first ingest:

```
/ingest
```

That is the install. Everything below is how it works and how to run it.

---

## 3. The mental model

Three layers, split by who is allowed to write. Two agents keep it current. Every agent reads the hot file and the index before it acts.

```
                 CAPTURE (any session, any time)
                            |
                            v
                        inbox/            unstructured, timestamped
                            |
                      /ingest or /dream
                            |
        +-------------------+-------------------+
        v                   v                   v
   sources/YYYY/          wiki/                ops/
   immutable raw     agent-owned synthesis   mutable business state
   agents read,      people, companies,      clients, pipeline, projects
   never edit        concepts, decisions     lifecycle, then archive/
        |                   |                   |
        +-------------------+-------------------+
                            |
                  index.md   hot.md   log.md
                  catalog    ~500w    append-only
                            ^
                            |
                 READ FIRST (every agent, every action)
```

**Sources are immutable.** A transcript lands once and never changes. The wiki can be rebuilt from sources at any time.

**The wiki is agent-owned.** The principal rarely writes a page by hand. The agent synthesizes, and the schema is what makes that safe.

**Ops is live state.** Clients, deals, projects. It has a lifecycle. When something hits `done` or `lost`, it moves whole into `archive/`.

**Folders route by mutability, not by topic.** Topic lives in wikilinks and frontmatter. The same fact stays reachable from several angles without being filed twice.

---

## 4. Layout

```
Vault/
    CLAUDE.md            the contract, read first by every operation
    index.md             master catalog, one line per page with a hook
    hot.md               rolling ~500-word current-state cache
    log.md               append-only operation log
    inbox/               zero-friction capture, drained by ingest
    sources/YYYY/        immutable raw: transcripts, emails, articles
    wiki/
        people/
        companies/
        concepts/
        decisions/
        mocs/            maps of content, one per topic
    ops/
        clients/<name>/brief.md
        pipeline/        deals
        projects/
    daily/YYYY-MM-DD.md  agent-appended journal
    archive/             closed deals and projects, moved whole
    meta/
        schema.md        the frontmatter spec
        templates/       one per page type
    .claude/skills/      ingest, query, lint, build, dream
```

### The three root files

- **index.md** is the catalog. One line per page with a hook, grouped by section, alphabetical. Every new page gets a line. Agents read this first to locate anything.
- **hot.md** is the warm cache. About 500 words on what is active right now: clients, live deals, open threads. Agents read this first when asked what is going on. Ingest and dream rewrite it when current context shifts.
- **log.md** is append-only. Every write adds one line: `## [YYYY-MM-DD HH:MM] <operation> | <title>`. It is the audit trail of what the agents did to your memory.

> [!NOTE]
> Every page must be reachable from `index.md` or a map of content. That is the reachability guarantee. A page nobody links to is a page no agent will find, and `/lint` reports it as an orphan.

---

## 5. The schema is the contract

Every page opens with frontmatter. Six universal fields on every note, then per-type fields. The full spec is [templates/vault/meta/schema.md](templates/vault/meta/schema.md). Writes that do not validate get rejected.

```yaml
---
type: person
created: 2026-10-07
updated: 2026-10-07
status: seedling
tags:
  - person
aliases:
  - "Jane Doe"
company: "acme-co"
role: "Head of Ops"
relationship: prospect
last_contact: "2026-10-07"
---
```

**Ten page types:** person, company, concept, decision, client, deal, project, source, daily, moc. Each has a template in `meta/templates/` and a folder it lives in.

**Status is a trust level.** Wiki pages move `seedling` to `growing` to `evergreen`. An agent reading a seedling knows to treat it as thin. Ops pages use `active`, `won`, `lost`, `done`. Clients get their own lifecycle: `discovery`, `active`, `client`, `paused`, `lost`, `closed`.

**First tag equals type.** Dates are absolute, `YYYY-MM-DD`, never relative. Slugs are lowercase and hyphenated.

The validator enforces all of it from the command line:

```bash
python3 scripts/validate-frontmatter.py ~/Documents/Vault
```

It checks every page under `wiki/`, `ops/`, `sources/`, `daily/`, plus `index.md` and `hot.md`. One line per violation, exit code 1 if any. On the day this guide shipped it checked 172 pages in my vault and found zero.

> [!IMPORTANT]
> The schema is what lets a machine be the author. If frontmatter is not a validated contract, you cannot build views on top of it, you cannot sync entities to a database, and you cannot trust anything an agent wrote. Write the schema before the first page.

---

## 6. The five operations

Each one is a skill in `.claude/skills/`. Run them from inside the vault.

### /ingest

The first operation. Takes raw input (a file path, a URL, pasted text, or nothing to drain the inbox) and folds it in. Six steps: land the source in `sources/YYYY/` with frontmatter, extract entities, create or update pages from the templates, cross-link every entity mention, update `index.md` and `hot.md` and the relevant map of content, append to `log.md`. Contradictions get flagged with both versions and their sources. Never invents facts.

### /query

Answer a question from the vault. Retrieval order: `hot.md` for current state, then `index.md` or the relevant map of content, then the pages themselves, three to five minimum when they exist, then sources only if the synthesis is thin. Every claim is cited with a wikilink or a path. If the vault does not know, it says so instead of filling the gap with general knowledge.

### /lint

Keep it coherent. Eight checks: schema validation, broken wikilinks, orphans, index drift, placeholder text that shipped, contradictions across pages, stale ops (deals past their next action date, clients quiet for 30 days, done pages not yet archived), and sources hygiene. Read-only by default. `/lint fix` applies the safe fixes and reports the rest.

### /build

One bounded enrichment task per run, from a priority queue: drain the inbox, refresh the hot file, advance stale ops, enrich the seedling with the most inbound links, wire orphans into the index, partial lint. Designed to be driven on a loop. One task, then stop.

### /dream

The nightly consolidation pass. Section 8 covers it in full.

---

## 7. Capture from every session

This is the part that makes the vault grow without you. Two pieces.

### The auto-capture rule

A standing rule in your global `~/.claude/CLAUDE.md`. Every Claude Code session on the machine carries it, in every project. When real operational information surfaces, the agent writes it to the vault as part of finishing the work, without being asked. Quick captures land in `inbox/` as a timestamped file. Substantial items run the ingest skill.

The full block is in [templates/auto-capture-rule.md](templates/auto-capture-rule.md). Paste it into `~/.claude/CLAUDE.md` and replace the path.

### The vault-ingest skill

The rule needs a way to run the vault's ingest from any project. That is the [vault-ingest](../../skills/vault-ingest/) skill in the central library. It holds no logic of its own. It loads the vault's contract and the vault's own ingest skill, then runs that against absolute paths.

```bash
mkdir -p ~/.claude/skills/vault-ingest
curl -o ~/.claude/skills/vault-ingest/SKILL.md https://raw.githubusercontent.com/davisxai/operator-knowledge-base/main/skills/vault-ingest/SKILL.md
```

Open the file and replace `/ABSOLUTE/PATH/TO/vault` with yours.

> [!TIP]
> **Capture is unstructured on purpose.** The inbox has no schema. Forcing structure at capture time is what makes people stop capturing. Structure gets applied later by ingest or dream, when the agent has time to read the index and merge properly.

---

## 8. The dream agent

Dream, as in memory consolidation during sleep. A second agent, same tools, one extra permission: it can write to the vault. It runs once a night and folds the day's signal in.

### Four phases

1. **Orient.** Read `hot.md` and `index.md`. Skim the maps of content and any page the signal will touch.
2. **Gather signal.** The principal's own words first (chat exports, voice note transcripts, notes). Then inbox captures, daily notes, pages changed in the last 24 hours, and any external digest your setup drops in the inbox. From all of it, list new facts, drift, and contradictions.
3. **Consolidate.** Surgical edits. Read a page before changing it. Fold new facts in. Resolve every contradiction with a dated line. Create new pages only for genuinely new entities. Never touch `sources/`.
4. **Prune and index.** Rewrite `hot.md` as a 500-word current-state cache. Refresh `index.md`. Log one line.

### The priority rule

Your own chat turns outrank emails and existing pages. If you said it in conversation, that is the current truth, and a page that disagrees gets corrected.

### Three guards

A scheduled run self-skips unless there is real work. A lock file younger than 30 minutes means a pass is already running. A last dream under one hour ago means wait. Zero changed files in 24 hours means nothing to do. `/dream force` bypasses all three.

### Run it

By hand, from inside the vault:

```
/dream
```

Headless, which is what the schedule uses:

```bash
cd ~/Documents/Vault && claude -p "/dream"
```

On a schedule, with the launchd job in [templates/com.vault.dream.plist](templates/com.vault.dream.plist). Edit the two paths, then:

```bash
cp templates/com.vault.dream.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.vault.dream.plist
launchctl list | grep com.vault.dream
```

It fires at 03:00 local while the Mac is awake. The pass is gated and idempotent, so a missed night is consolidated by the next run. Logs land in `/tmp/vault-dream.out.log`.

### Outside Claude Code

If you run agents with the Claude Agent SDK or your own harness, [templates/dream-agent-prompt.md](templates/dream-agent-prompt.md) is the same four-phase process as a standalone system prompt. Your write tool has to refuse `sources/`, validate frontmatter against the schema, and append to the log.

> [!TIP]
> **Test the headless command once before you load the schedule.** Run `claude -p "/dream"` from the vault folder and read the summary it prints. If it works by hand, the plist only adds the clock.

---

## 9. Practical playbook

### Use Case 1: Ingest a call transcript

**Scenario:** You just finished a discovery call and the transcript is in your downloads folder.

**The prompt:**
```
/ingest ~/Downloads/acme-discovery-2026-10-07.md
```

**What happens:**
- The transcript lands in `sources/2026/2026-10-07-acme-discovery.md` with source frontmatter, `processed: false`.
- Every person and company in it gets a page or an update. The deal moves in `ops/pipeline/`.
- Every mention is wikilinked. `index.md` gets a line per new page. `hot.md` is rewritten if the deal changed state. One line in `log.md`.

**Expected outcome:** A report listing the source landed, the pages touched, and any contradictions for you to resolve.

> **Pro tip:** Name the file with the date and the counterparty before you ingest. The slug is derived from the filename.

### Use Case 2: Capture from another project

**Scenario:** You are in a client's codebase with Claude Code and the client mentions a new stakeholder in an email you asked the agent to read.

**The prompt:**
```
Read the latest thread from the client and summarize the decision.
```

**What happens:**
- The agent answers the question.
- Because the auto-capture rule is in your global config, it also appends a timestamped file to the vault's `inbox/` with the stakeholder's name and the decision, and tells you in one line.
- Nothing else changes until ingest or dream runs.

**Expected outcome:** One new file in `inbox/`. The vault grew without you opening it.

> **Pro tip:** If the agent did not capture, the rule is missing or the path is wrong. Open `~/.claude/CLAUDE.md` and check both.

### Use Case 3: Ask what is going on with a client

**Scenario:** It is Monday and you want the state of one engagement before a call.

**The prompt:**
```
/query what is the current state with Acme and what is the next action
```

**What happens:**
- `hot.md` is read first. Then the client brief under `ops/clients/acme/`, the deal page, and the people pages.
- The answer comes first, then citations as wikilinks, then any gaps the vault cannot fill.

**Expected outcome:** A cited answer in under a minute, with the next action and its date from the deal page.

> **Pro tip:** If the answer cites `sources/` instead of wiki pages, the synthesis layer is thin on that client. Run `/build` a few times with the `clients` focus.

### Use Case 4: Lint before a weekly review

**Scenario:** Friday. You want the vault clean before the dream passes run over the weekend.

**The prompt:**
```
/lint fix
```

**What happens:**
- Schema violations get missing fields added. Broken wikilinks get repointed to close matches. Orphans get an index line.
- Contradictions, stale deals, and archive moves are reported, never auto-fixed.

**Expected outcome:** A report grouped by check, counts first, with the pages that need your call.

> **Pro tip:** Run the Python validator too. It is the same schema check without a model in the loop, which makes it a good pre-commit hook on the vault repo.

### Use Case 5: Close a deal and archive it

**Scenario:** A deal is won and the project is done.

**The prompt:**
```
Acme signed. Mark the deal won, the client status client, and archive the project.
```

**What happens:**
- The deal page gets `status: won` and a dated history line. The client brief gets `status: client` and the retainer.
- The finished project moves whole into `archive/`. `index.md` is updated. `hot.md` reflects the new state.

**Expected outcome:** Three pages changed, one moved, four lines in `log.md`.

> **Pro tip:** Say it in chat. The dream pass treats your own words as the highest-priority signal, so even if you only mention it in passing, it lands.

---

## 10. Cost and best practices

### Cost levers

1. **Keep the hot file at 500 words.** Every agent reads it first, on every action. A tight hot file keeps every read small.
2. **Tier the models.** Lint and build are mechanical, run them on a smaller model. Query is the reasoning product, give it the frontier model. Dream sits in between.
3. **Gate the dream.** The three guards mean a quiet day costs nothing. Do not run consolidation on a timer without the activity check.
4. **Sources are immutable, so nothing gets re-ingested.** A landed transcript is read when the wiki is thin, not on every query.

### Best practices

1. Write the contract and the schema before the first page. Every downstream decision depends on them.
2. Capture unstructured. Structure later.
3. Never let an agent edit `sources/`. If the write tool cannot enforce it, the rule will eventually be broken.
4. One line in the log per write. When a page is wrong, the log tells you which pass wrote it.
5. Resolve contradictions with a dated line, not a silent overwrite.
6. Say decisions out loud in chat. The dream pass is built to catch them.
7. Keep the vault in git. History is free and the validator makes a clean pre-commit hook.

---

## 11. Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| `/ingest` is not found | Claude Code was not started inside the vault | `cd` into the vault, then run `claude`. Skills load from `.claude/skills/` in the working directory |
| The agent captured nothing from another project | Auto-capture rule missing or wrong path | Paste `templates/auto-capture-rule.md` into `~/.claude/CLAUDE.md`, replace the path |
| Validator reports `first tag must equal type` | Template edited by hand | First entry under `tags:` must be the page type |
| `/query` keeps citing sources instead of pages | Wiki is thin on that topic | Run `/build` a few times, or `/ingest` the relevant sources again |
| Dream says "nothing to consolidate" every night | The 24-hour activity check found no changed files | Confirm captures are landing in `inbox/`, or run `/dream force` once |
| launchd job never fires | Mac asleep at 03:00, or paths not edited | `pmset repeat wakeorpoweron MTWRFSU 02:55:00`, and check both paths in the plist |
| `claude -p "/dream"` exits immediately | Not logged in, or run outside the vault | Run `claude` once interactively to log in, and `cd` into the vault first |
| A page has placeholder text like `...` or `YYYY-MM-DD` | Template filled incompletely | `/lint` reports it. Fill or delete the section |

---

## 12. Quick reference

**Create a vault**
```bash
bash scripts/new-vault.sh ~/Documents/Vault
```

**Operations (inside the vault)**
```
/ingest [path | url | empty to drain inbox]
/query  <question>
/lint   [report | fix]
/build  [clients | pipeline | people | concepts]
/dream  [force | dry-run]
```

**Validate**
```bash
python3 scripts/validate-frontmatter.py ~/Documents/Vault
```

**Schedule the dream (macOS)**
```bash
cp templates/com.vault.dream.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.vault.dream.plist
launchctl start com.vault.dream        # run once now
launchctl unload ~/Library/LaunchAgents/com.vault.dream.plist
```

**Install the global capture skill**
```bash
mkdir -p ~/.claude/skills/vault-ingest
curl -o ~/.claude/skills/vault-ingest/SKILL.md https://raw.githubusercontent.com/davisxai/operator-knowledge-base/main/skills/vault-ingest/SKILL.md
```

**Files**
- Contract: `CLAUDE.md`
- Schema: `meta/schema.md`
- Templates: `meta/templates/<type>.md`
- Skills: `.claude/skills/<operation>/SKILL.md`
- Log format: `## [YYYY-MM-DD HH:MM] <operation> | <title>`

**Status vocab**
- Wiki: `seedling`, `growing`, `evergreen`
- Ops: `active`, `won`, `lost`, `done`
- Client: `discovery`, `active`, `client`, `paused`, `lost`, `closed`
- Deal stage: `lead`, `discovery`, `proposal`, `build`, `retainer`, `closed`

---

## 13. Sources

- The benchmark post: r/AI_Agents, Major-Shirt-8227, August 3, 2026. https://www.reddit.com/r/AI_Agents/comments/1veeix3/i_ran_8_ai_agent_memory_systems_through_2176/
- ClawDrop's writeup of the benchmark, August 5, 2026 (the scores quoted above): https://clawdrop.org/playbooks/agent-memory-benchmark/
- The llm-wiki pattern the winning setup followed is Andrej Karpathy's.
- The design in full, as it runs in production: [ai-os/vault.md](../../ai-os/vault.md), [ai-os/architecture.md](../../ai-os/architecture.md) section 6 for the consolidation loop, [ai-os/claude-code-layer.md](../../ai-os/claude-code-layer.md) for the capture rule and hooks, [ai-os/build-your-own.md](../../ai-os/build-your-own.md) for the build order.
- Vault counts in this guide were pulled from the live vault on October 7, 2026.

---

Built by OperatorOS | [operatoros.ai](https://operatoros.ai)
Follow [@daviss.dev](https://instagram.com/daviss.dev) and [@os.operator](https://instagram.com/os.operator) for production-grade AI guides.
