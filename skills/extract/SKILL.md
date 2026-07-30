---
name: extract
description: Extract structured data from messy input. Voice transcripts, meeting notes, Slack dumps, email threads. Outputs decisions, action items, facts, and questions. Use when the user says "extract from this", "pull out the key points", "what did we decide", "action items from this", "parse this transcript".
argument-hint: [file-path]
allowed-tools: Read, Write, Grep, Glob
---

# Structured Extraction

Pull structured data from any messy input source.

## Step 1: Identify the Input

If `$ARGUMENTS` is a file path, read it.
If the user pasted content directly, use that.
If neither, ask what to extract from.

Detect the input type:
- **Voice transcript** filler words, speaker labels, timestamps
- **Meeting notes** bullet points, loose structure, multiple topics
- **Slack/chat dump** usernames, timestamps, threaded replies
- **Email thread** forwards, replies, signatures mixed in
- **Raw text blob** unstructured, stream of consciousness

## Step 2: Extract by Category

### Decisions
- Anything explicitly agreed to ("we'll go with X", "let's do Y", "decided to Z")
- Who made or approved the decision
- Any conditions attached ("if X then we'll Y")

### Action Items
- Tasks assigned to specific people
- Deadlines mentioned
- Deliverables promised
- Format: `[WHO] [WHAT] [BY WHEN or "no deadline"]`

### Facts
- New information stated as true (numbers, dates, names, specs)
- Corrections to previously held beliefs
- Technical details (API endpoints, access needed, versions)

### Open Questions
- Things explicitly asked but not answered
- Things that need clarification
- Assumptions that weren't validated

### Key Quotes
- Statements worth preserving verbatim (strong opinions, requirements, constraints)
- Include speaker attribution

### Context / Background
- Information that's useful to know but isn't actionable
- Relationships between people or systems mentioned
- Historical context referenced

## Step 3: Output

If a file path was provided as an argument, write to `[same-directory]/[filename]-extracted.md`.
Otherwise, print to terminal.

```
# Extraction: [source name or date]

Input type: [transcript / notes / chat / email / text]
Date: [today or date from content]

## Decisions
- [Decision 1] (decided by [who])
- [Decision 2]

## Action Items
- [Person] [Task] [Deadline]

## Facts
- [Fact 1]

## Open Questions
- [Question 1] (asked by [who], if known)

## Key Quotes
- "[Quote]" [Speaker]

## Context
- [Background info]
```

## Rules

- Preserve exact spelling of proper nouns. If unclear, flag with "[spelling?]"
- Don't infer decisions that weren't explicitly made. If it was discussed but not decided, it's an open question.
- Action items need a WHO. If no one was assigned, note "unassigned".
- No markdown tables. No emojis.
- Strip filler words from quotes but keep the meaning intact.
- If the input is very short (under 10 lines), just extract what's there. Don't pad with empty sections.
