# The Vault

An agent-maintained Obsidian second brain. Markdown files on disk, an agent writes most of them, and a schema decides what is allowed to land.

This is the knowledge layer the rest of the system reads from. The chat agent answers out of it. The email classifier pulls its roster from it. The nightly consolidation loop writes back into it.

Design and contract only. No note contents.

---

## 1. The core idea

An LLM wiki, not a human notebook.

The human rarely writes pages by hand. The agent owns the synthesis. That single inversion is what makes everything else necessary. If a machine is the author, the schema has to be strict and the audit trail has to be complete, because nobody is reading every write.

Three layers, split by **mutability** rather than by topic:

- **Immutable raw.** `sources/YYYY/`. Transcripts, articles, emails, documents. Agents read them. They never edit or delete them.
- **Agent-owned synthesis.** `wiki/`. People, companies, concepts, decisions, maps of content.
- **Mutable business state.** `ops/`. Clients, pipeline, projects. Has a lifecycle and terminal states.

> [!TIP]
> Folders route by type and mutability. Topic lives in links and properties. There is no `clients/marketing/` tree to maintain, because a page's subject is expressed through wikilinks, frontmatter, and tags. The same fact stays reachable from several angles without being filed twice.

---

## 2. Layout

```
CLAUDE.md            the schema contract, read first by every operation
index.md             master catalog, one line per page with a hook
hot.md               rolling ~500 word recent-context cache
log.md               append-only operation log
inbox/               zero-friction unstructured capture, drained by ingest
sources/YYYY/        immutable raw layer, date-prefixed slugs
wiki/                people/ companies/ concepts/ decisions/ mocs/
ops/                 clients/<name>/brief.md, pipeline/, projects/
daily/YYYY-MM-DD.md  agent-appended journal
archive/             closed projects and deals, moved whole at done or lost
meta/                schema.md, templates/, bases/
.claude/skills/      the four canonical operation definitions
```

Scale as of 2026-07-29, since honest numbers beat adjectives: roughly 76 person pages, 26 company pages, 26 concept pages, 6 maps of content, 1 decision page, 44 pending inbox captures, and 163 log lines since the vault was initialized on 2026-06-09.

That one decision page against 76 person pages is the honest signal of where a vault like this drifts. Entity capture outruns reasoning capture. The layer that would pay back the most is the thinnest one.

---

## 3. index, hot, log

Three root files solving three different retrieval problems. This is the most portable part of the design.

**`index.md` is the catalog.** One line per page, each with a one-sentence hook, grouped into sections and alphabetical within section. Its job is to let an agent locate a page without globbing the filesystem or burning context on full text search.

The hook is what makes it work. A bare filename list forces the agent to open pages to find out whether they are relevant. A hook turns the index itself into a decision surface.

**`hot.md` is the working set.** About 500 words: current state, active work, pipeline, people, watch items. It is rewritten, not appended to, whenever context shifts. Its job is to answer "what is going on" in a single read. A recency cache in front of a large corpus, for the same reason a CPU has L1.

**`log.md` is the audit trail.** Every write appends exactly one line:

```
## [YYYY-MM-DD HH:MM] <operation> | <title>
```

It does three jobs at once. It proves what the agent did. It gives the enrichment loop a cursor for what changed since. It makes agent behavior debuggable after the fact.

Three files, three access patterns: catalog lookup, recency, provenance and change detection. Systems that build only one of the three end up doing full scans for the other two.

---

## 4. Maps of content as a reachability guarantee

`wiki/mocs/` holds curated lists of linked pages, each with a one-line hook, organized around durable axes rather than topics of the month.

The rule that gives them teeth lives in the lint spec: **every page must be reachable from `index.md` or from a map of content.** An orphan page is a defect, not an inconvenience.

That converts "did we remember to link it" from a discipline problem into a checkable invariant.

---

## 5. Frontmatter as a validated API contract

The schema file describes itself as the contract between the vault, the agents, and the dashboard. Writes that do not validate are rejected.

Treating a knowledge base as a typed API rather than a pile of prose is the reason automation on top of it can be trusted.

**Universal fields on every note:** `type`, `created` (set once, never changed), `updated` (bumped on every edit), `status`, `tags` (first tag always equals `type`), `aliases`.

**Ten types**, each with its own required fields, its own template, and its own home folder: person, company, concept, decision, client, deal, project, source, daily, moc.

**Status vocabularies are per layer**, which is the subtle part:

- Wiki pages use a **maturity** vocabulary: `seedling` (thin, needs enrichment), `growing` (useful, gaps remain), `evergreen` (complete, stable, trustworthy).
- Ops pages use a **lifecycle** vocabulary: active, won, lost, done, plus a richer set for client records.
- Sources skip status semantics entirely and carry a `processed` boolean.

Two different questions get two different fields. "How good is this page" and "where is this work" are not the same axis, and overloading one field to carry both is how status columns become meaningless.

`seedling` is also what makes autonomous enrichment targetable. The enrichment loop globs for it and knows exactly what to work on.

**Validation rules:** every field for the type must be present, empty string where noted but never a missing key. Enums match exactly. Dates are absolute `YYYY-MM-DD`, never relative. Slugs are lowercase, hyphenated, canonical.

**A color system lives in the schema too.** One hex per type, declared once as the source of truth for three consumers: the Obsidian graph config, a CSS snippet, and the external dashboard. Design tokens defined in the data contract instead of re-picked in every renderer.

---

## 6. Templates and views

`meta/templates/` holds one file per type. Each ships with complete frontmatter, a one-sentence identity statement, a facts section where every fact carries a source, an open-questions checklist, and a dated activity log.

Two template conventions are worth stealing outright:

**A fenced subjective section the agent may not fill.** Person and client templates carry a "Subjective notes" block, labeled as the human's read and explicitly opinion rather than fact. The contract forbids the agent from writing in it. The agent does not get to manufacture my opinions. Making that boundary structural beats making it a rule someone has to remember.

**Open questions as checkboxes.** Gaps are first-class content, not omissions. This is what makes "state what is missing instead of papering over it" actually work. There is a place to put the missing thing.

`meta/bases/` holds Obsidian Bases view definitions. Pure queries over frontmatter: filter on type, group by stage, order by a named property. Because the frontmatter is a validated contract, database-style views come free with no separate database. Pipeline by stage is a working board rendered straight out of markdown files.

---

## 7. The four operations

Three canonical operations, plus an enrichment loop layered on top.

### ingest

Raw in, structure out. Input is an inbox entry, a file path, a URL, a transcript, or pasted text. Empty input means drain the inbox, oldest first.

1. **Land the source.** Write to `sources/YYYY/YYYY-MM-DD-slug.md` with source frontmatter and `processed: false`. Immutable from this moment. Inbox captures move here and are removed from `inbox/`.
2. **Extract entities.** People, companies, concepts, deals, clients, projects, decisions. Check the index first, then glob and grep the wiki and ops layers for existing pages.
3. **Create or update.** New pages copy the matching template and get filled completely. No placeholder text ever ships. Existing pages merge, never duplicate. Contradictions get flagged with both versions and both sources, never silently resolved.
4. **Cross-link.** Every entity mention that has a page gets wrapped in a wikilink. Pages already touched get rescanned for newly created entities.
5. **Update the access layer.** Add index lines. Rewrite the hot file if current context shifted. Wire the page into its map of content. Flip the source's processed flag, which is the only edit a landed source is ever allowed.
6. **Log one line. Report** what landed, what was touched, and what is ambiguous.

Step 1 carries the most weight. Landing the raw material before synthesizing means every synthesized claim has a durable, unedited artifact behind it. Provenance becomes a byproduct of write order rather than extra bookkeeping.

### query

The retrieval order is the whole design. Cheapest and most recent first:

1. `hot.md` for anything about current state.
2. `index.md` or the relevant map of content, to locate candidates.
3. Individual wiki and ops pages. Read all candidates, not the first hit. Three to five pages minimum when they exist.
4. `sources/` only when the synthesis layer is too thin to answer.

Wiki before sources. Every claim cites a wikilink or a file path. Answer first, then citations, then gaps.

> [!IMPORTANT]
> If the vault does not know, say so. No general-knowledge fill unless explicitly asked for. A knowledge base that quietly answers from model priors is worse than no knowledge base, because you stop being able to tell the two apart.

An optional file-back step offers to write reusable synthesis back as a page, but only with approval. That is what keeps query from polluting the corpus with its own inferences.

Queries append to the log too. Reads are logged, not just writes, so the log doubles as a record of what I keep asking about.

### lint

The coherence gate. Eight checks, read-only by default, with a fix mode that applies only safe repairs.

1. Schema validation, including first-tag-equals-type and absolute dates.
2. Broken wikilinks.
3. Orphans. Any page unreachable from the index or a map of content.
4. Index drift in both directions. Pages missing from the index, and index lines pointing at deleted pages.
5. Placeholder text that escaped a template.
6. Contradictions across pages. Always reported, never auto-fixed.
7. Stale ops. Past next-action dates, records with no activity in 30 or more days, terminal-status pages not yet archived.
8. Source hygiene. Sources sitting unprocessed for more than seven days, and any source file modified after landing, which is a contract violation.

Two rules define its safety envelope:

- **Lint never deletes anything.** It only adds and edits.
- **Ambiguity escalates to the human** instead of being resolved.

That is how an autonomous maintenance pass earns write access. Not by being smart, by being structurally incapable of destroying content.

### vault-build

The enrichment loop, written to be driven by a repeating interval runner. One iteration does exactly one task.

**Orient in under 60 seconds.** Read the hot file, the index, the last 15 log lines, and the inbox listing, in parallel.

**Pick the next task from a fixed priority queue, stop at the first viable one.**

1. Drain the inbox.
2. Refresh the hot file if it is more than 3 days old or contradicts newer page state.
3. Advance stale ops using a read-only cross-check against the business repo.
4. Enrich the `seedling` page with the most inbound links.
5. Discover and ingest a file in the business repo newer than the last log entry.
6. Repair map-of-content and index integrity.
7. Run a partial lint.

**Execute end to end, log one line, report in under 100 words.**

Four design notes carry over to any autonomous loop:

- **One task per iteration, and the loop is the chain.** The agent is explicitly forbidden from chaining tasks itself. Each iteration is bounded, logged, and independently reviewable. That is what stops a long-running agent from drifting into an unbounded work session.
- **The priority queue is the policy.** "What should the agent do next" is answered by a static ordered list, not by model judgment at runtime. Reproducible, auditable, and cheap to change.
- **Inbound link count selects the enrichment target.** The thinnest page that the most other pages depend on gets fixed first.
- **Research is budgeted.** For an unknown person: one search, at most two fetches. If nothing concrete surfaces, stop and record the gap. Hard caps beat telling an autonomous agent to be thorough.

Explicit read-only zones: the sources layer, the predecessor vault, and the business repo. Readable, never writable by the loop.

---

## 8. Skill packaging, two layers

The same four operations exist in two places, and the split is deliberate.

**Canonical definitions live inside the vault** at `<VAULT>/.claude/skills/{ingest,query,lint,vault-build}/SKILL.md`. Those are the real specs.

**Thin global wrappers live in the user skills directory**, one per operation, roughly 25 lines each. Every wrapper does four things:

1. Hardcodes the vault root path.
2. Instructs the agent to load the contract first, every time. The vault's own rules file, the schema where relevant, and the canonical in-vault spec.
3. Says to execute that canonical spec exactly, resolving every referenced path absolutely against the vault root regardless of the current working directory, with an explicit guard: never create vault files inside the current project.
4. Restates the non-negotiable write rules inline as a backstop.

Why the shape works:

- **The vault owns its own semantics.** Changing ingest behavior means editing one file inside the vault. The wrappers never change.
- **The operations are callable from anywhere.** Capture happens while working in unrelated repos, which is where information actually surfaces. A knowledge base you can only write to from inside its own directory does not get written to.
- **Loading the contract is step one of every invocation, not a memory assumption.** The schema is re-read on every run rather than trusted to persist in context. Standing constraints drift over long sessions, so they get reloaded instead of remembered.

Discoverability is handled by the skill description field, which enumerates literal trigger phrases so the operations fire on intent instead of requiring recall of a command name.

---

## 9. Capture design

The capture path is deliberately structureless. The contract says it plainly: capture goes to the inbox unstructured, do not force structure at capture time, ingest applies structure later.

Most inbox files are a title heading and free-form notes. Filenames are date-prefixed slugs, with a time component when there is more than one in a day.

This is a write-optimized front door in front of a read-optimized store. Structuring at capture adds friction exactly when friction costs the most, in the middle of doing something else. Deferring it to a batch operation that already has the whole vault in view also produces better structure, because the ingest pass can see existing entities and merge instead of duplicating.

> [!WARNING]
> The cost of this is visible: 44 captures pending against a vault initialized about seven weeks earlier. Deferred structuring only works if the drain actually runs. That is exactly why draining the inbox is priority one in the enrichment queue and stale-inbox detection is a lint check.

---

## 10. Write rails, in code

The rules above are contract text. Some of them are also enforced in the vault library, which is where they actually hold.

- A single function refuses any write, rename, or delete under the sources layer. The comment notes the check lives there and nowhere else.
- Every filesystem mutation resolves through a path check confirming the target stays inside the vault root, rejecting absolute paths and parent-directory escapes.
- A date coercion pass normalizes YAML-parsed date objects back to `YYYY-MM-DD` strings, so a note cannot fail validation on a field the caller never touched.
- Three directories are never walked: the Obsidian config, git metadata, and the agent config folder.

The predecessor vault is a frozen archive and must never be written to. That is stated in the operations spec, not just remembered.

---

## 11. Source of truth rules, consolidated

- Sources are immutable. The only permitted edit to a landed source is flipping processed to true.
- Every write appends exactly one line to the log.
- Every new page gets an index entry with a one-line hook, in the right section, alphabetical.
- Every write validates against the schema before it lands. The `updated` field bumps on every edit.
- Merge, never duplicate. A fact lives in one place and is referenced from everywhere else.
- Contradictions surface with both versions and both sources. Never silently reconciled.
- Never invent facts, and never invent the human's opinions.
- Missing information is stated as missing rather than papered over.
- When a deal or project reaches a terminal state, the whole folder moves to archive and the index updates. Archive moves require approval.
- Automated work is referenced by the operator persona name, never by the model name.

**Style rules are in the contract too.** No emojis. No markdown tables, use key/value bullets. No em dashes or double dashes. Absolute dates only. Short direct sentences, answer first. Lowercase hyphenated slugs.

Enforcing style in the data contract rather than at review time means every generated page is consistent by construction. Banning tables in particular keeps every page readable as raw text, which is how an agent reads it.

---

## 12. What to take

Ranked by how much they carry.

1. **Split by mutability, not topic.** Immutable raw, agent-owned synthesis, mutable state. Topic lives in links and properties.
2. **index, hot, and log as three distinct retrieval surfaces.** Catalog, recency cache, audit trail. Do not collapse them.
3. **Frontmatter as a validated API contract.** Rejecting non-conforming writes is what makes downstream views and dashboards possible with no separate database.
4. **Land raw before synthesizing.** Provenance becomes a byproduct of write order.
5. **Maturity status on knowledge pages.** A `seedling` value is a queryable work queue for autonomous enrichment.
6. **A fixed priority queue plus one task per loop iteration.** Bounded, logged, reviewable autonomous work.
7. **Lint that adds and edits but never deletes, and escalates ambiguity.** How a maintenance agent earns write access.
8. **Thin global wrappers around in-vault canonical specs.** Callable from anywhere, semantics owned in one place.
9. **Unstructured capture, deferred structuring.** Only works if the drain is scheduled.
10. **A fenced subjective section the agent may not fill.** Structural separation of fact from opinion beats a rule that has to be remembered.

---

Built by OperatorOS | [operatoros.ai](https://operatoros.ai)
Follow [@daviss.dev](https://instagram.com/daviss.dev) and [@os.operator](https://instagram.com/os.operator) on Instagram.
