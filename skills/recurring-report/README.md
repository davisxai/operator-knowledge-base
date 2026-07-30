# /recurring-report

A status report compiled from your actual systems (email, Notion, Linear, GitHub, local files) on a schedule. Set it up once, get the same-shaped report every week.

## Install

```bash
mkdir -p ~/.claude/skills/recurring-report
curl -o ~/.claude/skills/recurring-report/SKILL.md https://raw.githubusercontent.com/davisxai/operator-knowledge-base/main/skills/recurring-report/SKILL.md
```

## Usage

```
/recurring-report Gmail labeled "client" + my Linear active cycle, every Friday 9am
```

Then wire the cadence into a scheduler: Claude Desktop's Scheduled Tasks, or any cron-style trigger for Claude Code. The skill owns sources and format; the scheduler owns timing.

## What you get

A fixed-shape report: wins, in progress, blocked, numbers, next focus, and a closing one-liner naming the single most important thing. Written to a dated file by default so reports accumulate into history.

## Why it's built this way

Three rules keep it honest. Numbers only come from sources (no source, no number). Unreachable sources get reported as unreachable instead of silently dropped. And the section order never changes between runs, because a report you can't compare week over week is just a newsletter.

## Requirements

Each source needs its integration connected: a Gmail MCP for email, the Notion or Linear MCP if you use those, `gh` for GitHub. Local-file sources need nothing.
