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
