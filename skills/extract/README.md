# /extract

Turn any messy input into structured decisions, action items, facts, open questions, quotes, and context. Transcripts, meeting notes, Slack dumps, email threads, raw text.

## Install

```bash
mkdir -p ~/.claude/skills/extract
curl -o ~/.claude/skills/extract/SKILL.md https://raw.githubusercontent.com/davisxai/operator-knowledge-base/main/skills/extract/SKILL.md
```

Or clone the repo and `cp -r skills/extract ~/.claude/skills/`.

## Usage

```
/extract path/to/transcript.md
```

Or paste the messy text into chat and type `/extract`.

## What you get

Six sections, empty ones skipped: Decisions (with who decided), Action Items (who, what, when), Facts, Open Questions, Key Quotes with attribution, and Context. Given a file path, it writes `[filename]-extracted.md` next to the source; otherwise it prints to the terminal.

## Why it's built this way

The discipline is in what it refuses to do: it never infers a decision that wasn't explicitly made (that's an open question), never invents an owner for a task (that's "unassigned"), and never pads short input with empty sections. Extraction you can trust beats extraction that looks complete.

## Customize

The production version at OperatorOS adds a final step that files action items into a task tracker (Linear via MCP). Add your own step 4 pointing at whatever tracker MCP you run.
