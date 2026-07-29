# Claude Code Skills: The Starter Kit

> Follow @os.operator on Instagram for more guides like this.

---

## What This Is

A starter kit for Claude Code Skills 2.0. Five production-tested skills you can install in under 60 seconds, plus the knowledge to build your own.

### What you'll get

-> What skills are and how they work under the hood
-> How to install, create, and manage skills
-> 5 ready-to-use skill files with setup commands
-> Pro tips from running 40+ custom skills in production
-> A quick reference cheat sheet for daily use

---

## Skills Changed Everything

Claude Code 2.0 shipped Skills on March 3, 2026. Before that, you typed instructions from scratch every time. Now you write the playbook once and run it forever.

A skill is a markdown file. That's it. A structured prompt saved as a SKILL.md file that Claude Code reads and executes when you type a slash command. No plugins. No extensions. No API keys. One file, infinite reuse.

And skills compound. The more you build, the faster you work. Forty skills deep, my terminal handles commits, deployments, client proposals, code reviews, research, and system architecture from single commands.

---

## Why This Matters

Every repeated task is a skill you haven't written yet.

-> A 5-minute workflow you run 3x a day is 65 hours a year. One skill turns that into 30 seconds each time.
-> Skills aren't locked to Claude Code. The agentskills.io open standard works across 30+ tools: Cursor, GitHub Copilot, VS Code, Gemini CLI, OpenAI Codex.
-> Skills 2.0 added built-in evals, benchmarks, and A/B testing. Skills can now test and improve themselves.

---

## How Skills Work

### The File

Every skill lives in a single file called `SKILL.md`. It has two parts:

**Frontmatter** (the config block between `---` markers):

```yaml
---
name: my-skill
description: What this skill does and when to trigger it.
allowed-tools: Read, Write, Grep, Glob, Bash
---
```

**Body** (structured instructions Claude follows):

```markdown
# Skill Title

You are doing X. Follow these steps.

## Phase 1: Setup
Read the project context...

## Phase 2: Core Work
Execute the main task...

## Phase 3: Output
Present results in this format...
```

### Where Skills Live

-> **Global skills** (available in every project): `~/.claude/skills/[skill-name]/SKILL.md`
-> **Project skills** (shared with your team): `.claude/skills/[skill-name]/SKILL.md`

### How to Run a Skill

Type `/` followed by the skill name:

```
/commit
/research nextjs server actions
/system-design voice-agent acme-corp
```

Claude reads the SKILL.md, follows the instructions, and executes the workflow.

### How to Install a Skill

Drop the SKILL.md file into the right folder:

```bash
# Global (follows you everywhere)
mkdir -p ~/.claude/skills/my-skill
# paste or create SKILL.md inside

# Project (shared with collaborators)
mkdir -p .claude/skills/my-skill
# paste or create SKILL.md inside
```

No restart needed. Claude picks it up immediately.

---

## The 5 Skills

### 1. /create (Skill Creator)

The skill that builds every other skill. Describe any workflow and Claude writes the entire SKILL.md file, tests it, and saves it ready to use.

**What it does:**
-> Decides whether your request needs a skill or an agent
-> Chooses the right tools, model, and scope
-> Writes a complete SKILL.md with frontmatter, phases, and quality standards
-> Saves it to the correct location (global or project)

**Install:**

```bash
mkdir -p ~/.claude/skills/create
```

```yaml
---
name: create
description: >
  Create new skills or agents. Trigger when the user says "make a skill",
  "create an agent", "turn this into a skill", "automate this",
  "save this workflow", or "I keep doing this".
allowed-tools: Read, Write, Grep, Glob, Bash
---

# Skill & Agent Creator

Orchestrate the creation of reusable skills and agents for Claude Code.
The core job is making the right orchestration decisions: type, placement,
tools, model, scope, then writing a clean artifact.

## Decision 1: Skill or Agent?

Count how many of these agent signals are present. If 2 or more match,
create an agent. If 0-1 match, create a skill.

Agent signals:
- Needs to run autonomously in the background
- Requires its own isolated context
- Would benefit from a specific model selection
- Needs to spawn further sub-agents

## Decision 2: Placement

- References project-specific paths or schemas: .claude/skills/
- Cross-project utility: ~/.claude/skills/

## Write the File

Include frontmatter (name, description with trigger phrases, allowed-tools)
and a structured body with phases, quality standards, and output format.
```

**Try it:**

```
/create a skill that generates changelogs from git history grouped by type
```

---

### 2. Context7 (Live Documentation)

An MCP plugin by Upstash that fetches up-to-date, version-specific documentation for any library and injects it directly into your prompts. No more debugging deprecated methods.

**What it does:**
-> Resolves any library name to its documentation source
-> Pulls current API signatures, code examples, and version-specific syntax
-> Works silently in the background on every prompt

**Install (MCP server, not a skill file):**

```bash
claude mcp add context7 -- npx -y @upstash/context7-mcp@latest
```

That's it. Context7 runs automatically. When you ask Claude to write code using any library, it pulls the latest docs before generating.

**Verify it's working:**

```bash
claude mcp list
```

You should see `context7` in the list with a green checkmark.

**Details:**
-> Built by Upstash. Free and open source.
-> GitHub: github.com/upstash/context7
-> Free tier: 1,000 requests/month, 60 requests/hour
-> Supports thousands of libraries (Next.js, React, Supabase, LangChain, etc.)

---

### 3. /swarm (Parallel Agents)

Decomposes a complex task into independent workstreams, creates a purpose-built agent for each, and delivers a ready-to-execute orchestration plan.

**What it does:**
-> Analyzes your end state and identifies parallel workstreams
-> Creates agent files with specific tools, models, and missions
-> Maps wave structure (what runs in parallel, what depends on what)
-> Outputs exact invocation commands to launch the team

**Install:**

```bash
mkdir -p ~/.claude/skills/swarm
```

```yaml
---
name: swarm
description: >
  Decompose a complex task into parallel subagents and create all agent
  files for execution. Invoke when: "create agents for this", "spin up
  a swarm", "parallel agents", "swarm this", "break this into subagents".
argument-hint: <endstate or full task description>
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Swarm

Analyze a requested endstate, decompose it into independent parallel
workstreams, design a purpose-built subagent for each, create all agent
files, and deliver a ready-to-execute orchestration plan with wave
structure and exact invocation commands.

## Phase 1: Context Capture
Read project context. Inventory existing agents. Parse the endstate.

## Phase 2: Workstream Decomposition
Identify parallel workstreams. Each produces one independent deliverable.
Target 2-6 agents. Map wave structure before writing files.

## Phase 3: Agent Specification
For each workstream: name, model (haiku/sonnet/opus), tools (least-privilege),
output definition.

## Phase 4: Create Agent Files
Write each agent file with: mission, context, protocol (setup, core work,
verification, output), and quality standards.

## Phase 5: Orchestration Plan
Output the wave map with exact Task() invocations.
```

**Try it:**

```
/swarm full codebase audit: security review, dependency updates, test coverage, performance bottlenecks, and deployment readiness
```

---

### 4. /research (Deep Research)

Launches parallel discovery across the web, your codebase, and competing alternatives. Returns a synthesized report with cross-referenced findings and confidence ratings.

**What it does:**
-> Decomposes your question into 3-5 specific sub-questions
-> Runs 3 parallel tracks: web intelligence, codebase analysis, alternatives
-> Cross-references every claim across at least 2 sources
-> Rates confidence on each finding (High/Medium/Low)
-> Includes dissenting opinions and honest limitations

**Install:**

```bash
mkdir -p ~/.claude/skills/research
```

```yaml
---
name: research
description: >
  Deep technical research with parallel discovery across web, codebase,
  and alternatives. Synthesizes findings into actionable recommendations.
  Use when the user says "research this", "look into", "compare options
  for", "what's the best way to", or "find out about".
argument-hint: <topic, library, architecture question, or technical concept>
allowed-tools: Read, Grep, Glob, Bash, WebSearch, WebFetch
---

# Deep Research

You are a technical research analyst. Find the truth, verify it across
multiple sources, deliver a clear recommendation backed by evidence.
Never summarize a single source. Cross-reference everything.

## Phase 1: Decompose the Question
Break the topic into 3-5 specific sub-questions before searching.

## Phase 2: Parallel Discovery
Track 1 - Web Intelligence: 2+ queries per sub-question, prioritize
official docs over blogs, filter for 2025-2026 content.
Track 2 - Codebase Analysis: Search existing code for related patterns.
Track 3 - Alternatives: Find competitors, comparisons, benchmarks.

## Phase 3: Verify and Cross-Reference
Every claim needs 2+ independent sources. Flag conflicts.
Verify versions and pricing against official docs.

## Phase 4: Synthesize Report
Summary, findings with confidence ratings, options compared,
codebase context, recommendation, implementation path, sources.
```

**Try it:**

```
/research best authentication pattern for multi-tenant SaaS with Supabase
```

---

### 5. /system-design (Architecture)

Maps a business or software system into a clear, buildable architecture with pipeline stages, named tools, realistic volume estimates, and cost projections.

**What it does:**
-> Takes a system type or description as input
-> Researches current tools, pricing, and capabilities
-> Outputs a full architecture document with pipeline visualization
-> Includes volume estimates and monthly cost projections
-> Recommends specific tools at each stage

**Install:**

```bash
mkdir -p ~/.claude/skills/system-design
```

```yaml
---
name: system-design
description: >
  Map out a software or business system architecture with pipeline stages,
  tool recommendations, realistic volume/pricing numbers, and clear visual
  layouts. Use when the user says "system design", "map this system",
  "how should we build this", "architect this", or "lay out the pipeline".
argument-hint: "[system-type] [client-name]"
allowed-tools: Read, Write, Edit, Grep, Glob, WebSearch, WebFetch
---

# System Design

Map a business or software system into a clear, buildable architecture.
Output a document with pipeline visualization, named tools, realistic
volume estimates, and monthly cost projections.

## Phase 1: Requirements
Parse the system type. Research current tools and pricing.
Identify data flow, integrations, and scale requirements.

## Phase 2: Architecture
Design the pipeline: Input -> Process -> Store -> Serve -> Monitor.
Name specific tools at each stage. Include fallback options.

## Phase 3: Cost Model
Estimate monthly volume. Calculate costs per tool at that volume.
Total monthly cost with breakdown.

## Phase 4: Output
Pipeline diagram (text-based), tool recommendations with links,
volume/pricing table, implementation sequence, risks and mitigations.
```

**Try it:**

```
/system-design lead generation pipeline for a B2B SaaS company
```

---

## Pro Tips

**Start with /create, not a text editor.**
Don't write SKILL.md files by hand. Describe the workflow to /create and let Claude handle the structure. It knows the format better than you do.

**Keep skills single-purpose.**
One skill, one job. A skill that does code review AND deployment is two skills pretending to be one. Split them.

**Use argument-hint for flexible skills.**
Adding `argument-hint: "[topic]"` to your frontmatter lets the same skill handle different inputs. `/research nextjs` and `/research supabase auth` both use the same skill file.

**Global for you, project for teams.**
If only you use it, save it globally. If your team needs it, save it in the project. Don't mix these up.

**Read your CLAUDE.md first.**
Skills are powerful when they know your project. Make sure your CLAUDE.md has your conventions, stack, and preferences documented. Skills read it before executing.

---

## Limitations

-> **Context window matters.** Skills that launch many parallel searches or read large codebases can hit context limits. Keep skills focused.
-> **MCP tools require setup.** Context7 needs the MCP server installed. Other MCP-dependent skills (like /exa for web search) need their own API keys and config.
-> **Skills 2.0 evals are new.** The built-in eval and benchmark system works but is still maturing. Test important skills manually before trusting automated evals.
-> **Not all tools available everywhere.** WebSearch and WebFetch require internet access. Skills using them won't work in offline or restricted environments.
-> **Community skills vary in quality.** Third-party skill files from GitHub repos may be outdated or poorly structured. Read the SKILL.md before installing.

---

## Quick Reference

### Commands

```
/create [description]     Build a new skill from a description
/context7                 (automatic) Live docs for any library
/swarm [endstate]         Decompose task into parallel agents
/research [topic]         Deep research with cross-referenced findings
/system-design [type]     Full architecture with tools and pricing
```

### File Locations

```
~/.claude/skills/         Global skills (all projects)
.claude/skills/           Project skills (shared with team)
~/.claude/agents/         Global agents
.claude/agents/           Project agents
```

### Skill File Structure

```
---
name: skill-name
description: What it does and when to trigger it.
argument-hint: "[optional-args]"
allowed-tools: Read, Write, Grep, Glob, Bash
---

# Title

Instructions Claude follows when the skill is invoked.
```

### Installing a Skill

```bash
mkdir -p ~/.claude/skills/[name]
# Create SKILL.md inside with frontmatter + instructions
# No restart needed. Use immediately with /[name]
```

---

Built by OperatorOS | operatoros.ai
Follow @os.operator for production-grade AI guides.
