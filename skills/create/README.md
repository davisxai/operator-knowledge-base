# /create

The skill that builds every other skill. Describe a workflow and it makes the five orchestration decisions (skill or agent, global or project, tools, model, scope), then writes the complete artifact and registers it.

## Install

```bash
mkdir -p ~/.claude/skills/create
curl -o ~/.claude/skills/create/SKILL.md https://raw.githubusercontent.com/davisxai/operator-knowledge-base/main/skills/create/SKILL.md
```

## Usage

```
/create a skill that generates changelogs from git history grouped by type
/create an agent that researches a company and writes a brief
```

It also fires proactively: if you run the same multi-step workflow twice in a conversation, it proposes capturing it.

## What you get

A complete SKILL.md or agent file in the right location, with least-privilege tools, trigger-rich description, structured phases, and a registry line for your CLAUDE.md. Plus a stated rationale for every decision it made.

## Why it's built this way

The hard part of skill-writing isn't the markdown, it's the five decisions before the markdown. The "2 or more agent signals" rule alone resolves most of the skill-vs-agent ambiguity that stalls people. And the scope rule (build the minimum artifact that solves it) is what keeps a library of 60+ skills maintainable.
