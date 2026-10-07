---
name: dream
description: Nightly vault consolidation. Gathers the day's signal (inbox captures, daily notes, pages changed in the last 24 hours, any chat or email digest dropped in inbox/), folds it into wiki and ops pages with surgical edits, resolves contradictions, rewrites hot.md, refreshes index.md. Use when the user says "dream", "consolidate the vault", "run the nightly pass", or from a scheduled job.
argument-hint: [optional: force | dry-run]
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# /dream

Dream, as in memory consolidation during sleep. One unattended pass. Be surgical, be correct, leave the vault cleaner than you found it.

## Gate (skip unless there is real work)

Run these checks first. If any fails and `$ARGUMENTS` is not `force`, stop and report "nothing to consolidate".

1. **Lock.** If `.dream.lock` exists and is younger than 30 minutes, another pass is running. Stop. Otherwise write `.dream.lock` with the current timestamp and delete it in every exit path.
2. **Interval.** If the last `dream` line in `log.md` is under one hour old, stop.
3. **Activity.** Count: files in `inbox/`, pages under `wiki/`, `ops/`, `daily/` modified in the last 24 hours (`find . -name '*.md' -mtime -1`). If the count is zero, stop.

`dry-run` runs all four phases but writes nothing and prints what it would change.

## Phase 1: Orient

Read `hot.md` and `index.md`. Skim the MOCs in `wiki/mocs/` and any page the signal will touch. Build the current picture before changing anything.

## Phase 2: Gather signal

Read, in this priority order:

1. **The principal's own words.** Any file in `inbox/` that is a chat export, a voice note transcript, or a note the principal wrote. These are primary and authoritative. When they conflict with an email or an existing page, the principal's stated position wins.
2. **Inbox captures** written by agents during the day.
3. **Daily notes** from the last 24 hours.
4. **Pages changed** in the last 24 hours.
5. **External digests** if your setup drops them in `inbox/` (an email summary, agent run summaries, a morning brief).

From all of it, list three things: new facts (people, companies, deals, decisions not yet in the vault or thinly covered), drift (pages whose state is now out of date), contradictions (a new fact that conflicts with what a page says).

## Phase 3: Consolidate

- Update existing pages by reading them first and folding the new facts in. Do not rewrite a page wholesale. Change only what the signal warrants.
- When a new fact contradicts an old one, update the page to the correct state and add a one-line "Updated YYYY-MM-DD: ..." under the relevant section. Do not leave a contradiction standing.
- Create new pages only for genuinely new entities. Start from `meta/templates/`. Pick the correct type and folder. New wiki pages start at `seedling` unless they are already well covered.
- Operate on ops state too: a deal that moved stages, a client whose status changed, a project that progressed.
- Every write validates against `meta/schema.md`. Bump `updated`. Never touch `sources/`.
- Move each consumed inbox capture to `sources/YYYY/` with source frontmatter and `processed: true`.
- Do not invent facts. Only write what the signal or the existing vault supports. If unsure, leave it out.

## Phase 4: Prune and index

Rewrite `hot.md` as a tight, roughly 500-word current-state cache: what is active, who matters right now, the live deals, the open threads. Drop what is stale. Refresh `index.md` so every new or renamed page has a line. Append one line to `log.md`: `## [YYYY-MM-DD HH:MM] dream | created N, updated M, resolved K contradictions`.

## Rules

- No contradictions left unresolved.
- Never edit `sources/`.
- Absolute dates only, YYYY-MM-DD. Never "today" or "yesterday" inside a page.
- Be surgical. Do not rewrite pages wholesale or invent facts.
- The principal's voice: direct, short sentences, no emojis, no em dashes or double dashes.

End with a 2 to 4 sentence summary: pages created, pages updated, contradictions resolved.
