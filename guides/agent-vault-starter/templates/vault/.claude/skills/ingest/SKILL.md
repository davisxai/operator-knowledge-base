---
name: ingest
description: Take raw input (inbox entry, file, URL, transcript, pasted text) and fold it into the vault. Lands the raw material in sources/, creates or updates wiki and ops pages, cross-links, updates index.md, hot.md, and log.md. Use when the user says "ingest this", "add to the vault", "process the inbox", drops a transcript path, or pastes a URL.
argument-hint: [source path, URL, or empty to drain inbox/]
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebFetch
---

# /ingest

The first operation. Read raw material, synthesize, cross-reference, file.

## Parse `$ARGUMENTS`

- A path inside `sources/` (already landed, just process).
- A path outside the vault or a URL: fetch or copy, land in `sources/`.
- Empty: drain `inbox/`, oldest capture first.

## Steps

1. **Land the source.** Save content to `sources/YYYY/YYYY-MM-DD-slug.md` with source frontmatter per `meta/schema.md` (url, source_type, date_ingested, processed: false). Sources are immutable after this step. Inbox captures get moved here, then removed from `inbox/`.

2. **Read and extract entities.** People, companies, concepts, deals, clients, projects, decisions. Check `index.md` first, then Glob/Grep `wiki/` and `ops/` for existing pages.

3. **Create or update pages.**
   - New page: copy the matching template from `meta/templates/`, fill it completely, validate frontmatter against `meta/schema.md`. Never ship placeholder text.
   - Existing page: merge new information, bump `updated`, do not duplicate facts. Contradictions get flagged with both versions and their sources.
   - Routing: people/companies/concepts/decisions to `wiki/`; client state to `ops/clients/<name>/brief.md`; deal movement to `ops/pipeline/`; project state to `ops/projects/`.

4. **Cross-link.** Every entity mention with a page gets `[[wrapped]]`. Scan pages you touched for newly-created entities.

5. **Update the access layer.**
   - `index.md`: one line with a hook for every new page, alphabetical within section.
   - `hot.md`: rewrite if current context shifted (new deal stage, client event, decision).
   - Relevant MOC in `wiki/mocs/` if the new page belongs on one.
   - Flip the source's `processed` to true.

6. **Log.** Append one line to `log.md`: `## [YYYY-MM-DD HH:MM] ingest | <title>`

7. **Report.** Source landed, pages touched, contradictions or ambiguities for the principal.

## Rules

- Sources are immutable. Never edit a landed source (except the processed flag).
- Wiki and ops pages are yours. The principal rarely writes them by hand. Nothing bland or incomplete.
- Never invent facts or the principal's opinions. Subjective sections stay empty until the principal fills them.
- No em dashes, no double dashes, no markdown tables, no emojis. Absolute dates only.
