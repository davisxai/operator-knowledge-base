---
name: swarm
description: >
  Decompose a complex task into parallel subagents and create all agent files for execution.
  Invoke when: "create agents for this", "spin up a swarm", "parallel agents", "swarm this",
  "break this into subagents", "orchestrate agents for", "what agents do I need", "build a swarm",
  "I need agents for this", "decompose this task".
argument-hint: <endstate or full task description>
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Swarm

Analyze a requested endstate, decompose it into independent parallel workstreams,
design a purpose-built subagent for each, create all agent files, and deliver a
ready-to-execute orchestration plan with wave structure and exact invocation commands.

## Phase 1: Context Capture

Read all available project context before designing anything:

1. Inventory existing agents to avoid duplication:
   - `ls .claude/agents/ 2>/dev/null`
   - `ls ~/.claude/agents/ 2>/dev/null`
2. Read CLAUDE.md (project-level first, then `~/.claude/CLAUDE.md`) for
   conventions, registered tools, naming patterns, and tech stack
3. Glob for README.md and any architecture docs
4. Parse the argument (endstate/task) to extract:
   - Final deliverable and measurable success metric
   - Domain areas implied (database, API, UI, testing, scraping, enrichment, etc.)
   - Technology stack in use
   - Specific file paths, schemas, or services referenced
   - Which parts are independent vs sequentially dependent

## Phase 2: Workstream Decomposition

Identify parallel workstreams using strict rules:

**Parallelism rules:**
- Each workstream produces one independent deliverable
- Workstreams are sequential ONLY when one's output is another's required input
- One workstream = one agent, no shared agents
- Target 2-6 agents; more than 6 signals scope creep, merge related work

**Workstream types:**
- **Research/analysis** reads only, no production writes
- **Code generation** writes new files or implements features
- **Validation/testing** reads code and runs checks
- **Integration** connects two existing subsystems
- **Data/migration** transforms or moves data
- **Scraping/enrichment** external data acquisition

**Map wave structure before writing any files:**
- **Wave 1:** agents with zero blockers (start immediately, run in background)
- **Wave 2+:** agents that consume output from prior waves
- **Final:** integration or verification agents requiring all prior waves complete

State the wave map explicitly before proceeding to Phase 3.

## Phase 3: Agent Specification

For each workstream, define the full spec before writing the file:

**Name:** lowercase-hyphenated, verb-noun format
- Good: `scrape-directory-listings`, `validate-email-schema`, `build-sequence-manager`
- Bad: `agent1`, `helper`, `misc-tasks`

**Model selection:**
- `haiku` monitoring, classification, simple pattern detection, high-volume cheap tasks
- `sonnet` default for most tasks: research, code generation, analysis
- `opus` deep reasoning, complex architecture, nuanced multi-step judgment

**Tools (least-privilege):**
- Reading code only: Read, Grep, Glob
- Writing new files: add Write
- Modifying existing files: add Edit
- Running CLI, tests, builds: add Bash
- Live internet data: add WebFetch, WebSearch
- Spawning further subagents: add the subagent tool (Task in older Claude Code versions, Agent in newer ones); use sparingly

**Color:**
- `blue` or `cyan` research, analysis, reading
- `green` building, generating, implementation
- `yellow` validation, testing, quality
- `red` security, secret scanning, permissions
- `magenta` creative, templating, content

**permissionMode:** default is `default`. Use `bypassPermissions` only when the user
explicitly requests autonomous execution without approval prompts.

**Output definition:** what files it writes, what terminal summary it prints,
what context it hands off to the next wave.

## Phase 4: Create Agent Files

**Placement per agent:**
- References this codebase's specific paths, schemas, or APIs: `.claude/agents/<name>.md`
- Cross-project utility with no project-specific references: `~/.claude/agents/<name>.md`

Create directories if absent:
```bash
mkdir -p .claude/agents
mkdir -p ~/.claude/agents
```

**Write each agent file with this structure:**

```markdown
---
name: [agent-name]
description: >
  [What it does in one sentence. Include 3+ trigger phrases.]

  <example>
  Context: [Situation where this agent fires]
  user: "[What the user says]"
  assistant: "[How Claude responds, invoking this agent]"
  <commentary>[Why this agent fits]</commentary>
  </example>
model: [haiku|sonnet|opus]
color: [color]
tools: [comma-separated list]
permissionMode: default
---

## Mission

[One paragraph. What the agent accomplishes, what "done" looks like: specific
and measurable. How this fits into the overall endstate.]

## Context

[Project-specific knowledge: file paths, schema fields, API patterns, naming
conventions, existing services. Be specific. The agent receives only this
prompt, not the main conversation.]

## Protocol

### Phase 1: Setup
[First actions. What to read, what to verify before starting.]

### Phase 2: Core Work
[Primary operations. Specific files to create/modify. Commands to run.]

### Phase 3: Verification
[How to confirm output is correct. Tests, checks, validation.]

### Phase 4: Output
[Exact output format. Files written with full paths. Terminal summary.
Context to hand off to the next wave.]

## Quality Standards
- [Domain-specific correctness criterion]
- [Error handling: what to do when something fails]
- [Validation: how to confirm work is correct]
- [Scope boundary: what NOT to do]
```

Every section must contain specific, actionable content based on project context.
No generic placeholders.

## Phase 5: Orchestration Plan

After all agent files are written, output the execution plan:

```
SWARM: [Task Name]

Endstate: [One-sentence measurable success metric]

WAVE 1 (parallel, no dependencies):
  [agent-name] -> [what it produces]
  [agent-name] -> [what it produces]

WAVE 2 (parallel, depends on Wave 1):
  [agent-name] -> [what it produces] | needs: [Wave 1 agent output]

WAVE N (final integration):
  [agent-name] -> [final deliverable]

AGENT FILES CREATED:
  .claude/agents/[name].md
  ~/.claude/agents/[name].md

TO EXECUTE:

  Wave 1 (launch all in background):
    [subagent invocation with agent name + specific context prompt]

  Wave 2 (after Wave 1 completes):
    [subagent invocation with context + Wave 1 outputs]

  Wave N (final):
    [subagent invocation with full context]
```

## Phase 6: Registry Update

Add all new agents to the appropriate CLAUDE.md:
- Project agents: project's CLAUDE.md under an Agent Registry section
- Global agents: `~/.claude/CLAUDE.md` under an Agent Registry section

Format: `- **[agent-name]** [one-sentence description]`

## Quality Standards

- Every agent has a single measurable output, no ambiguous missions
- No two agents duplicate work; overlapping scope means merge or split
- Dependency chain is acyclic, no circular dependencies between waves
- Tool lists are minimal, no WebSearch unless live internet data is required
- Agent names are unique across project and global registries
- Each agent file is self-contained, no "see other file" references
- Orchestration plan includes exact invocations with background flags for Wave 1
- Project agents include specific file paths, not generic references
- No emojis, no markdown tables, no duplicated content across files
