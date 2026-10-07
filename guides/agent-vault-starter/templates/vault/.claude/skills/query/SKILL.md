---
name: query
description: Answer a question from the vault. Searches hot.md, index.md, MOCs, then pages, synthesizes a cited answer, optionally files reusable knowledge back. Use when the user asks "what do I know about X", "query the vault", "what is going on with Y", or any question the vault might answer.
argument-hint: [question]
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# /query

The second operation. Search, synthesize, cite, optionally file back.

## Parse `$ARGUMENTS`

A natural-language question. If empty, ask what the principal wants to know.

## Retrieval order

1. **`hot.md`** for anything about current state, active clients, or recent events.
2. **`index.md`** or the relevant MOC (`wiki/mocs/`) to locate candidate pages.
3. **Individual pages** in `wiki/` and `ops/`. Read all candidates, not just the first hit. Pull 3-5 pages minimum when they exist.
4. **`sources/`** only when the synthesis layer is thin.

## Steps

1. Identify entities and concepts in the question. Map them to pages via the retrieval order.
2. Read candidates in parallel. Synthesize the answer.
3. Cite every claim with `[[wikilinks]]` or file paths.
4. Flag gaps explicitly. Suggest what to ingest if the vault cannot answer well.
5. **File back (optional).** If the synthesis is reusable knowledge, offer to file it as a page or merge into one. Ask the principal first. New pages follow templates and schema, get an index.md line.
6. Append to `log.md`: `## [YYYY-MM-DD HH:MM] query | <question summary>`

## Rules

- The answer comes first, then citations, then gaps.
- Do not invent. If the vault does not know, say so. No general-knowledge fill unless asked.
- No em dashes, no markdown tables, no emojis.
