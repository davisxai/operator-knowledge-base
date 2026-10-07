---
name: vault-ingest
description: Fold raw input (file, URL, transcript, pasted text, or the inbox) into your agent-maintained vault from ANY project. Lands the source, creates or updates wiki and ops pages, cross-links, updates index, hot, and log. Use when the user says "ingest this", "add to the vault", "feed the vault", "store this in obsidian", or "process the inbox" while working outside the vault.
argument-hint: [source path, URL, or empty to drain inbox]
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebFetch
---

# /vault-ingest

Runs the vault's `ingest` operation no matter what directory you are in.

**VAULT ROOT:** `/ABSOLUTE/PATH/TO/vault`

## How to run

1. Load the contract first, every time:
   - `<VAULT ROOT>/CLAUDE.md` (schema contract and write rules)
   - `<VAULT ROOT>/meta/schema.md` (frontmatter spec)
   - `<VAULT ROOT>/.claude/skills/ingest/SKILL.md` (the canonical operation definition)
2. Execute the `ingest` operation exactly as that SKILL.md defines it, with one adjustment: every path it references is relative to the VAULT ROOT above. Always read and write using absolute paths under `<VAULT ROOT>`, regardless of the current working directory. Never create vault files inside the current project.
3. Treat `$ARGUMENTS` as the ingest input: a file path, a URL, pasted text, or empty to drain `<VAULT ROOT>/inbox/`.
4. Follow all vault write rules: land sources immutably in `<VAULT ROOT>/sources/YYYY/`, merge never duplicate, cross-link every entity with `[[wikilinks]]`, update `index.md` / `hot.md` / `log.md`, validate frontmatter against the schema, no emojis, no markdown tables, no em or double dashes, absolute dates.

$ARGUMENTS
