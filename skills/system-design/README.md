# /system-design

Map any software or business system into a buildable architecture: pipeline stages with named tools, a volume model that works backwards from the target, a monthly cost stack with real tiers, and the decision list that has to be settled before building.

## Install

```bash
mkdir -p ~/.claude/skills/system-design
curl -o ~/.claude/skills/system-design/SKILL.md https://raw.githubusercontent.com/davisxai/operator-knowledge-base/main/skills/system-design/SKILL.md
```

## Usage

```
/system-design lead generation pipeline for a B2B SaaS company
/system-design voice-agent
```

## What you get

An architecture document: ASCII pipeline diagram, per-stage detail (job, input, output, tool with alternatives, cost, setup, gotchas), the volume math shown explicitly, a cost stack that totals, and decisions split into "before build" versus "during build". Ships with five starting templates: lead gen, voice agent, RAG, automation, web app.

## Why it's built this way

Two habits make designs survive contact with reality. The volume model works backwards from the outcome (meetings booked, calls handled) instead of forward from tool capacity, and pricing gets verified against the vendor's current page instead of memory. A design with "TBD" in a tool slot fails the quality gate on purpose.
