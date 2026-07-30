# /swarm

Decompose a complex task into parallel subagents. It maps the wave structure (what runs in parallel, what depends on what), writes a complete agent file for every workstream, and hands you the exact invocation plan.

## Install

```bash
mkdir -p ~/.claude/skills/swarm
curl -o ~/.claude/skills/swarm/SKILL.md https://raw.githubusercontent.com/davisxai/operator-knowledge-base/main/skills/swarm/SKILL.md
```

## Usage

```
/swarm full codebase audit: security review, dependency updates, test coverage, performance bottlenecks, deployment readiness
```

## What you get

2 to 6 purpose-built agent files (mission, context, protocol, quality standards each), a wave map showing dependencies, and a copy-paste execution plan. Wave 1 agents run in parallel immediately; later waves consume their output.

## Why it's built this way

Two rules prevent the usual swarm failures. Target 2-6 agents: more than 6 means the scope is wrong, not the agent count. And workstreams are sequential only when one's output is another's required input; everything else runs parallel. Parallelism on shared state is a bug, not a feature.
