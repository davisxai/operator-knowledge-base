# Skills

Claude Code skills ported from the OperatorOS production library. These are the real working versions, sanitized of internal integrations, not simplified demos.

Every skill folder has the same layout:

- **README.md** what it does, install, usage, and why it's built the way it is
- **SKILL.md** the artifact itself: frontmatter (name, description, argument-hint, allowed-tools), phased process, output format, and quality rules

## Install

Any skill, two ways:

```bash
# single skill
mkdir -p ~/.claude/skills/extract
curl -o ~/.claude/skills/extract/SKILL.md https://raw.githubusercontent.com/davisxai/operator-knowledge-base/main/skills/extract/SKILL.md

# or clone once and copy what you want
git clone https://github.com/davisxai/operator-knowledge-base.git
cp -r operator-knowledge-base/skills/extract ~/.claude/skills/
```

No restart needed. Invoke with `/skill-name`.

## Index

- **[create/](create/)** The skill that builds every other skill. Five orchestration decisions, then a complete artifact.
- **[extract/](extract/)** Messy input (transcripts, notes, chat dumps, email threads) to structured decisions, action items, facts, questions, and quotes.
- **[research/](research/)** Three parallel discovery tracks, two-source verification on every claim, one clear recommendation.
- **[recurring-report/](recurring-report/)** Fixed-shape status report from your real systems, built for scheduled runs.
- **[swarm/](swarm/)** Decompose a task into 2-6 parallel subagents with wave structure and complete agent files.
- **[system-design/](system-design/)** Any system into a buildable architecture: pipeline, tools, volume math, cost stack, decision list.

## The standard these follow

- Least-privilege tool lists: a skill gets only the tools its steps actually use
- Trigger-rich descriptions so Claude fires them without being asked by exact name
- Explicit output formats, so two runs of the same skill produce the same shape
- Quality rules at the bottom of every skill, including what NOT to do
- No emojis, no markdown tables, no invented numbers

The full playbook on writing your own is in [guides/claude-code-skills-starter-kit/](../guides/claude-code-skills-starter-kit/).
