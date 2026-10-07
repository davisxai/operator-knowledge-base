---
name: build
description: Run one iteration of the continuous vault enrichment loop. Picks the single highest-value task from a priority queue and executes it end to end. Designed to be driven by a scheduler or a /loop. Use when the user says "build the vault", "enrich the vault", or as the loop body.
argument-hint: [optional focus: clients | pipeline | people | concepts]
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebFetch, WebSearch
---

# /build

One iteration. Pick ONE task, finish it, log it. The loop is the chain, do not chain tasks yourself.

## Step 1: orient (under 60 seconds)

Read in parallel:
- `hot.md` (current state)
- `index.md` (catalog)
- last 15 lines of `log.md` (recent activity)
- `inbox/` listing (pending captures)

## Step 2: pick the next task (priority order, stop at first viable)

1. **Drain inbox.** If `inbox/` has captures, ingest the oldest one per the ingest skill.
2. **Refresh hot.md.** If `hot.md` was last updated more than 3 days ago or contradicts newer page state, rewrite it (~500 words) from `ops/` current state.
3. **Advance stale ops.** Find deals in `ops/pipeline/` with a past `next_action_date` or clients with no activity in 30+ days. Cross-check your project folders (read-only) for newer state and update the deal or brief.
4. **Enrich a seedling.** Glob `wiki/**` for `status: seedling`. Pick the one with the most inbound links. Knock out open questions using your own files, Grep, or one focused web pass.
5. **MOC and index integrity.** New pages missing from their MOC or `index.md`. Wire them in.
6. **Lint nudge.** Partial lint (broken links and orphans only). Fix safe issues.

## Step 3: execute end to end

Use parallel tool calls. Update affected pages, frontmatter (`updated`, `status`), `index.md`, MOCs, and `hot.md` as needed. Validate every write against `meta/schema.md`.

## Step 4: log

Append one line to `log.md`: `## [YYYY-MM-DD HH:MM] build | <task>: <outcome>`

## Step 5: report

One short paragraph: what changed, what to expect next iteration. Under 100 words.

## Rules

- One task per iteration.
- `sources/` is read-only. Project folders outside the vault are read-only.
- Never invent facts or the principal's opinions. Unknowns get stated as unknowns on the page.
- For unknown people: ONE focused web pass (one WebSearch, max two WebFetch). If nothing concrete surfaces, stop and note the gap.
- No em dashes, no double dashes, no markdown tables, no emojis. Absolute dates.
