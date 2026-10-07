---
name: lint
description: Scan the vault for schema violations, broken wikilinks, orphan pages, placeholder text, contradictions, and stale ops state. Reports findings, optionally fixes safe issues. Use when the user says "lint the vault", "check the vault", "find orphans", or for weekly maintenance.
argument-hint: [optional: fix | report]
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# /lint

The third operation. Keep the vault coherent.

## Parse `$ARGUMENTS`

- Empty or `report`: scan and report, do not modify.
- `fix`: apply safe automatic fixes; report ambiguous issues for the principal.

## Checks

1. **Schema validation.** Every page's frontmatter against `meta/schema.md`: universal fields present, per-type fields present, enums exact, first tag equals type, dates absolute. Fix mode: add missing fields with best-effort values.

2. **Broken wikilinks.** Every `[[target]]` must resolve to a filename in the vault (path links like `[[ops/clients/acme/brief]]` resolve by suffix). Fix mode: repoint close slug matches; otherwise list.

3. **Orphans.** Every page must be reachable from `index.md` or a MOC. Fix mode: add an index line.

4. **Index drift.** Pages missing from `index.md`, or index lines pointing at deleted pages.

5. **Placeholder text.** Template placeholders that shipped (`...`, `YYYY-MM-DD`, `page-slug`, `Full Name`). Always report.

6. **Contradictions.** Claims that disagree across pages (numbers, dates, roles, stages). Always report, never auto-fix.

7. **Stale ops.** Deals with `next_action_date` in the past, clients with no activity entry in 30+ days, `done` or `lost` pages not yet moved to `archive/`. Always report; archive moves need the principal's nod.

8. **Sources hygiene.** Sources with `processed: false` older than 7 days (ingest candidates). Any source file modified after landing (violation).

## After running

1. Append to `log.md`: `## [YYYY-MM-DD HH:MM] lint | <mode>: N issues, M fixed`
2. Report grouped by check, counts first, specific pages named.

## Rules

- Read-only by default. Fix mode only when explicitly passed.
- Never delete pages or content. Lint adds and edits, never removes.
- Ambiguity goes to the principal.
