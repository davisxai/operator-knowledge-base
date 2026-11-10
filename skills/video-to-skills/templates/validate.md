---
name: {{SLUG}}-validate
description: Check a draft (a script, a post, an offer, an email) against the rules {{NAME}} states in {{SOURCE}} and against the user's own voice file, and return a line by line pass and fail list with the fix for each miss. Use when the user says "check this against {{NAME}}", "{{SLUG}} validate", "would {{NAME}} sign off on this", "run the rules on this draft", or "{{SLUG}}-validate".
argument-hint: [file path, or paste the draft]
allowed-tools: Read, Glob, Grep
---

# {{NAME}}: validate

A checklist with teeth. Every rule below is one {{NAME}} actually states in the talk, quoted. The draft either keeps each one or it does not, and a miss comes with the line that broke it and the fix.

## Read first, in order

1. `{{VOICE}}` for the user's own rules, especially the Anti-voice list. The user's rules are checked alongside his. If the file does not exist, run his rules only and say the voice check was skipped.
2. `{{ANALYSIS}}` sections 3 and 4 when a rule below needs more context.

## His rules

<!-- FILL: from analysis section 4, one entry per rule. Format: a bold one-line rule as an instruction, then the verbatim quote with timestamp, then one line on what a miss looks like in a draft. Group by cluster if the analysis grouped them. -->

## His structural rules

These come from how he builds a point, not from what he says to do. A draft that claims to use his structure is held to them.

<!-- FILL: from analysis sections 6 and 7, three to six rules in the same format: the rule, the evidence quote with timestamp, what a miss looks like. Typical ones: the open promises something specific, every claim gets a because or a number, one point per section, the close is a single rule or a callback, not a recap. -->

## Numbers he uses

A draft that repeats one of these as the user's own fact fails. The user's draft needs the user's numbers.

<!-- FILL: from analysis section 3, the claims with numbers, one line each: the number, the claim, the timestamp, and whether he named a source. -->

## Process

1. **Take the draft** from `$ARGUMENTS`, a file path or pasted text. Say what kind of piece it is in one line.
2. **Run his rules**, one at a time, top to bottom. For each: pass, or fail with the exact line from the draft and the fix, written in the user's voice.
3. **Run his structural rules** the same way, only if the draft is meant to use his structure. If it is not, say so and skip.
4. **Scan for borrowed numbers** against the list above. Any match is a fail with the slot to fill.
5. **Scan for borrowed phrases.** Any of these in the draft is a fail: <!-- FILL: the signature phrases from analysis section 8, comma separated -->.
6. **Run the user's Anti-voice list** from the voice file, one item at a time.
7. **Deliver** the report.

## Output

- **Piece:** what it is, one line.
- **His rules:** one line per rule, `PASS` or `FAIL`, and for every fail the draft line in quotes and the fix.
- **Structure:** the same, or "not applicable, the draft is not using his structure".
- **Borrowed numbers:** the matches, or "none".
- **Borrowed phrases:** the matches, or "none".
- **Your voice:** one line per Anti-voice item that fired, with the fix, or "clean".
- **Verdict:** `SHIP`, `FIX FIRST` (list the fails that matter most, at most three), or `REBUILD` (the structure is wrong, say which skeleton to use and point at `{{SLUG}}-script`).

## Quality rules

- Never pass a rule you did not check. If a rule cannot be judged from the draft, say "cannot judge from the draft" and why.
- Never soften a fail. The fix is written plainly, in the user's voice, and it is one line.
- Never add rules he did not state. If the draft has a problem outside his rules, put it under one heading, "Outside his rules", and keep it to three lines.
- Never rewrite the whole draft. That is the script skill's job. Fixes are per line.

Built from {{SOURCE}}. Analysis at {{ANALYSIS}}.
