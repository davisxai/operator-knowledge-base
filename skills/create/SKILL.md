---
name: create
description: >
  Create new skills or agents. Trigger this proactively when a repeatable workflow, multi-step
  pattern, or autonomous task is identified during conversation, even if the user does not
  explicitly ask. Also trigger when the user says "make a skill", "create an agent", "turn this
  into a skill", "automate this", "save this workflow", or "I keep doing this". If a workflow
  has been executed twice in a conversation, suggest capturing it as a skill or agent.
allowed-tools: Read, Write, Grep, Glob, Bash
---

# Skill & Agent Creator

Orchestrate the creation of reusable skills and agents for Claude Code. The core job is making
the right orchestration decisions (type, placement, tools, model, scope) then writing a
clean artifact.

## Decision 1: Skill or Agent?

Count how many of these agent signals are present. If 2 or more match, create an agent.
If 0-1 match, create a skill.

**Agent signals:**
- Produces a standalone deliverable (report, analysis, structured findings written to a file)
- Runs autonomously without user interaction during execution
- Needs web access, deep research, or extended multi-step reasoning
- Benefits from running in background/parallel while the user does other work
- Trigger is proactive/automatic rather than user-invoked with a command
- Work takes many independent tool calls over an extended period

**Skill signals:**
- User invokes it explicitly with `/name` at a specific moment
- Follows a predictable sequence with defined phases
- Produces terminal output or modifies files the user is actively working on
- User needs visibility into each step (linting, reviewing, deploying)
- Completes quickly as part of the user's immediate workflow

The "2 or more" rule resolves ambiguity. A competitor research task that produces a report
(deliverable) and needs web access (research) is clearly an agent (2 signals). A changelog
that the user invokes and sees immediately is clearly a skill (0 agent signals).

## Decision 2: Global or Project?

**Global** (`~/.claude/skills/` or `~/.claude/agents/`):
- Works across multiple projects (git workflows, research, deployment)
- References no project-specific paths, schemas, or conventions
- The user described it in general terms ("every time I...", "for any project...")

**Project** (`.claude/skills/` or `.claude/agents/`):
- References specific file paths, schemas, APIs, or conventions in one codebase
- Only makes sense in the context of this particular project
- The user described it relative to "this project" or "this codebase"

Do not ask the user unless truly ambiguous. Most workflows that mention specific
database schemas or project paths are project-level. Most workflows about git, deployment,
research, or code quality are global.

## Decision 3: Tools (Least Privilege)

Only include tools the artifact actually needs. Think about what operations it performs:

- **Read, Grep, Glob** reading and searching files (start here, add others as needed)
- **Write** creating or overwriting files (needed if it produces output files)
- **Edit** modifying existing files in place
- **Bash** shell commands like git, npm, curl, mkdir (needed for CLI operations)
- **WebSearch, WebFetch** internet access (only for research/scraping tasks)
- **Task / Agent** spawning subagents (only if the artifact orchestrates parallel work; the tool is named Task in older Claude Code versions and Agent in newer ones)

Common patterns:
- Research agent: Read, Write, Grep, Glob, WebSearch, WebFetch
- Code quality skill: Read, Grep, Glob, Bash
- Setup/scaffold skill: Read, Write, Glob, Bash
- Analysis agent: Read, Write, Grep, Glob (no web, no bash)
- File generation skill: Read, Write, Glob

## Decision 4: Model (Agents Only)

- **sonnet** default choice. Balanced speed and capability. Good for most research, analysis, and code review.
- **haiku** lightweight monitoring, pattern detection, simple classification. Use when the agent watches for signals rather than producing deep analysis.
- **opus** deep reasoning, complex multi-step analysis, nuanced judgment. Use when quality of output is critical and speed is not.
- **inherit** use the same model as the parent. Good when you don't have a strong preference.

## Decision 5: Scope Control

Before writing, ask: what is the MINIMUM artifact that solves this? Then build exactly that.

- Simple skills (changelog, lint check, git summary) need NO references/, scripts/, or assets/
- Only create supporting files when SKILL.md would exceed ~150 lines without them
- A 40-line SKILL.md that nails the workflow beats a 200-line one with edge cases
- If the user asked for one thing, build one thing. Do not add adjacent features.

## Creation Process

### 1. Capture Intent

From conversation context or by asking:
- What does it do? (one sentence)
- When should it trigger? (user phrases or automatic conditions)
- What inputs does it take? (arguments, files, conversation context)
- What output does it produce? (terminal output, files, modifications)

### 2. Make Decisions

Run through Decisions 1-5 above. State each decision briefly:
- **Type:** skill/agent (because [N] agent signals matched: [list them])
- **Placement:** global/project (because...)
- **Tools:** [list] (because...)
- **Model:** [if agent] (because...)
- **Scope:** [what's in, what's deliberately out]

### 3. Write the Artifact

#### For Skills

```yaml
---
name: skill-name
description: What it does and when to trigger. Be specific and slightly pushy with trigger phrases.
argument-hint: [optional-args]
allowed-tools: Read, Grep, Glob
---
```

Body rules:
- Imperative voice ("Run lint check", not "You should run")
- Under 2,000 words. Move detail to `references/` if needed.
- Define clear phases/steps
- Specify output format
- Mark independent steps for parallel execution
- Include `argument-hint` if the skill takes parameters

#### For Agents

```yaml
---
name: agent-name
description: >
  What it does and when Claude should trigger it. Use example blocks to teach
  autonomous detection:

  <example>
  Context: [Situation where agent should fire]
  user: "[What the user says or does]"
  assistant: "[How Claude should respond, invoking this agent]"
  <commentary>[Why this agent is the right choice here]</commentary>
  </example>
model: [sonnet/haiku/opus/inherit]
color: [blue/cyan/green/yellow/magenta/red]
tools: [only what's needed]
permissionMode: default
---
```

Include 2-3 example blocks in the description covering different trigger scenarios.
This is how Claude learns WHEN to fire the agent autonomously.

Body rules:
- Second person ("You are a research analyst...")
- Define mission, context, protocol phases, output format
- Include quality standards
- Plain text output if results leave the codebase
- Color choice: blue/cyan for analysis, green for build tasks, yellow for validation, red for security, magenta for creative

### 4. Write Supporting Files (only if needed)

- `references/*.md` detailed docs, schemas, patterns (keeps SKILL.md lean)
- `scripts/*.sh` or `scripts/*.py` deterministic utilities run repeatedly
- `assets/` templates or images used in output

Most skills need zero supporting files. Only create them when the main file would be
unwieldy without them.

### 5. Register

After creating the artifact, update the appropriate CLAUDE.md:
- Global artifacts: add to `~/.claude/CLAUDE.md` under an Agent Registry or Skill Registry section
- Project artifacts: add to the project's CLAUDE.md
- One-line description matching the artifact's purpose

### 6. Confirm

Tell the user:
- What was created, where, and why those decisions were made
- How to invoke it (`/name` for skills, automatic for agents)
- Suggest a quick test

## House Conventions

All artifacts follow these OperatorOS rules. Adapt to your own, but have some:
- No markdown tables in artifact bodies. Structured bullet lists only.
- No emojis.
- No duplicating content across files. Reference instead.
- Parallel execution where steps are independent.
- Auto-validate: skills that produce code should include a lint/type-check step.
- Descriptions should be "pushy": include multiple trigger phrases so Claude actually fires them.

## Proactive Triggers

Watch for these signals and suggest creating a skill or agent:

- User runs the same multi-step workflow a second time
- User says "I always do this" or "every time I..."
- A research or analysis task takes 5+ steps and could be templated
- User builds something reusable across projects
- A quality gate or checklist is described verbally but has no automation
- User manually does something an agent could do autonomously

When detected: one sentence proposal. If accepted, run the full creation process.
