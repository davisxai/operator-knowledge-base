---
name: recurring-report
description: >
  Compile a recurring status report from multiple data sources. Built for scheduled runs
  (Claude Desktop's task scheduler or any cron-style trigger). Use when the user says
  "weekly report", "status summary", "recurring report", or wants to automate something
  they currently compile manually each week.
argument-hint: [sources and cadence, e.g. "Gmail label:client + Linear cycle, Fridays 9am"]
allowed-tools: Read, Write, Grep, Glob
---

# Recurring Report

Compile a status report from real sources on a schedule. The report is only as good as
its sources, so pull from systems of record, never from memory.

## Step 1: Resolve Sources

Parse `$ARGUMENTS` for sources and cadence. If none given, ask which of these to include:

- **Email** (via a connected Gmail MCP): last 7 days, filtered by the labels the user names
- **Notion** (via Notion MCP): a specific database or page
- **Linear** (via Linear MCP): current cycle issues and status changes
- **GitHub** (via `gh` CLI or GitHub MCP): PRs merged, issues closed, in named repos
- **Local files**: logs, changelogs, or notes folders the user points at

Confirm the source list once, then keep it stable across runs. A recurring report that
changes shape every week is not a report, it is noise.

## Step 2: Pull

Read from each configured source. Sources are independent, so pull them in parallel.

For each source, collect:
- What changed since the last report period
- What is open, blocked, or waiting on someone
- Countable numbers (items closed, emails needing reply, PRs merged)

If a source is unreachable, say so in the report rather than silently omitting it.
A report that hides a dead integration is worse than no report.

## Step 3: Compile

Group findings by source. Within each group:
- **Highlights** (3-5 bullets max)
- **Open items** (anything blocked, pending decision, or stale)
- **Notable numbers** (counts, totals; only numbers actually observed in the source)

## Step 4: Format

Output in the user's template if one exists. Default template:

```
# [Cadence] Report: [date range]

## This Period's Wins
- ...

## In Progress
- ...

## Blocked / Needs Decision
- ...

## Numbers
- ...

## Next Period's Focus
- ...

One line: the single most important thing right now.
```

Save the output to the destination the user specifies (file, Notion page, email draft).
Default: write to a dated file so the reports accumulate into a browsable history.

## Step 5: Schedule

To make it recurring:
- **Claude Desktop:** create a Scheduled Task that runs this skill with the confirmed
  sources and cadence (e.g. "every Friday at 9am").
- **Claude Code:** trigger it from any cron-style scheduler available in your setup.

The skill itself stays schedule-agnostic. The scheduler owns the cadence; the skill owns
the sources and format.

## Rules

- Numbers come from the sources, never from estimation. No source, no number.
- Keep section order identical between runs so week-over-week comparison is possible.
- Empty sections get "Nothing this period", not deletion, so absences are visible.
- No emojis, no markdown tables.
- End with the one-line most-important-thing. If you cannot name one, the report period
  was noise; say that instead.
