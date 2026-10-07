# Vault

The knowledge layer for the person who owns this vault (the principal). An agent-maintained wiki: immutable raw sources, agent-owned synthesis, mutable business state. The principal rarely writes pages by hand. The agent maintains it. We call ours Operator. Nothing in this vault is allowed to be bland or incomplete.

## Structure

- **`CLAUDE.md`** this file. The schema contract. Every operation reads it first.
- **`index.md`** master catalog. One line per page with a hook. Agents read this first.
- **`log.md`** append-only operation log. Every write appends one line.
- **`hot.md`** rolling ~500-word recent-context cache. Read before answering "what is going on" questions.
- **`inbox/`** zero-friction capture. Unstructured. The ingest operation drains it.
- **`sources/YYYY/`** immutable raw layer (transcripts, articles, emails, documents). Agents read, never edit.
- **`wiki/`** synthesized agent-owned layer: `people/`, `companies/`, `concepts/`, `decisions/`, `mocs/`.
- **`ops/`** mutable business state with lifecycle: `clients/<name>/brief.md`, `pipeline/` (deals), `projects/`.
- **`daily/YYYY-MM-DD.md`** agent-appended journal.
- **`archive/`** closed projects and deals, moved whole when status hits `done` or `lost`.
- **`meta/`** `schema.md` (canonical frontmatter spec) and `templates/` (one per type).

Folders route by type and mutability. Topic lives in links and properties, not folders.

## Frontmatter contracts

`meta/schema.md` is the canonical spec. Summary:

- **Universal fields** on every note: `type`, `created`, `updated`, `status`, `tags`, `aliases`.
- **Status vocab:** wiki pages use `seedling` / `growing` / `evergreen`. Ops pages use `active` / `won` / `lost` / `done`.
- **person:** company, role, relationship, last_contact.
- **company:** category, relationship, website.
- **deal:** client, stage, value, next_action, next_action_date.
- **decision:** decided_on, relates_to, supersedes, confidence.
- **client:** company, status, retainer, started.
- **project:** client, repo.
- **source:** url, source_type, date_ingested, processed.

New pages start from the matching file in `meta/templates/`. Never ship placeholder text.

## The operations

Each one is a skill in `.claude/skills/`. Run them from inside the vault with `/ingest`, `/query`, `/lint`, `/build`, `/dream`.

### ingest

Take raw input (inbox entry, pasted text, transcript, URL, file) and fold it into the vault.

1. Land the raw material in `sources/YYYY/` with a date-prefixed slug filename and source frontmatter. Sources are immutable after this step.
2. Extract entities. Create or update wiki and ops pages per schema. Merge, never duplicate. Resolve contradictions by flagging both versions.
3. Cross-link aggressively: every entity mention with a page gets `[[wrapped]]`.
4. Update `index.md` (new pages get a line), `hot.md` (if it changes current context), and append to `log.md`.

### query

Answer a question from the vault. Retrieval order: `hot.md` first, then `index.md` or the relevant MOC, then individual pages. Wiki before sources. Cite paths or wikilinks for every claim. If the vault does not know, say so. Do not fill gaps with general knowledge unless asked.

### lint

Keep the vault coherent. Check: frontmatter validates against `meta/schema.md`, no broken wikilinks, no orphan pages (everything reachable from `index.md` or a MOC), no placeholder text, no contradictions, no stale ops pages. Report findings, fix safe issues, escalate ambiguity to the principal.

### build

One bounded enrichment task per run, picked from a priority queue. Drain the inbox, refresh the hot file, advance stale ops, enrich a seedling, wire orphans into the index.

### dream

The nightly consolidation pass. Orient, gather the day's signal, consolidate with surgical edits, prune and index. Runs unattended on a schedule.

## Write rules

- **`sources/` is immutable.** Agents read, never edit or delete a landed source.
- **Every write appends one line to `log.md`:** `## [YYYY-MM-DD HH:MM] <operation> | <title>`
- **Every new page gets an `index.md` entry** with a one-line hook, in the right section, alphabetical.
- **Writes must validate against `meta/schema.md`** before they land. Bump `updated` on every edit. Run `scripts/validate-frontmatter.py` from the guide if you want the check enforced by code.
- **Capture goes to `inbox/` unstructured.** Do not force structure at capture time. The ingest operation applies structure later.
- **The principal rarely writes pages by hand.** The agent owns the synthesis. Nothing bland, nothing incomplete. If information is missing, say what is missing instead of papering over it.
- **Never invent facts or the principal's opinions.** Subjective claims live under a clearly marked subjective section and stay empty until the principal fills them in.
- **Ops lifecycle:** when a deal or project hits `done` or `lost`, move the whole folder or file to `archive/` and update `index.md`.

## Style (enforced everywhere)

- No emojis. No markdown tables (use `- **Key:** Value` bullets). No em dashes or double dashes.
- Dates are absolute (`2026-10-07`), never relative.
- Direct, short sentences. Lead with the answer.
- Slugs: lowercase, hyphenated, canonical. `jane-doe`, `acme-co`.
- Reference automated work by the agent's name, never by the model's name.
