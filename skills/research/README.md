# /research

Deep technical research that runs three discovery tracks in parallel (web, your codebase, alternatives), cross-references every claim across at least two sources, and delivers one clear recommendation with an implementation path.

## Install

```bash
mkdir -p ~/.claude/skills/research
curl -o ~/.claude/skills/research/SKILL.md https://raw.githubusercontent.com/davisxai/operator-knowledge-base/main/skills/research/SKILL.md
```

## Usage

```
/research best authentication pattern for multi-tenant SaaS with Supabase
/research should we adopt Drizzle or stay on Prisma
```

## What you get

A structured report: summary, findings with confidence ratings and sources, options compared with production-health signals, what your codebase already commits you to, one recommendation with migration cost, and an implementation path with the key risk named.

## Why it's built this way

Three rules do the heavy lifting: every claim needs two independent sources or it gets marked unverified, the current codebase gets checked before anything is recommended, and the report must include the contrarian take. Research that only confirms the popular answer is marketing.
