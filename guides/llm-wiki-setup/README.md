# LLM Wiki Setup

> Follow [@davis.mcm](https://instagram.com/davis.mcm) and [@operatoros](https://instagram.com/operatoros) on Instagram for more guides like this.

---

### Andrej Karpathy's llm-wiki pattern, set up from zero in an afternoon.

On April 4, 2026, Andrej Karpathy published an idea file called [llm-wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f). It describes a knowledge base the agent writes and keeps current, instead of one it searches from scratch every time you ask. His line: "Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase."

The idea file is abstract on purpose. It says your agent should build out the specifics with you. This guide is the specifics: the folder, a schema file you can paste, the prompts for each operation, and the Obsidian settings. It works for any domain. Research, a book, a client, a business, your own notes.

My company runs on this pattern. If you want the full business version with captures from every session and a nightly consolidation agent, that is the [Agent Vault Starter](../agent-vault-starter/). Start here first.

---

## What you'll get

→ The day-one folder, created with one command, with git history from the first commit

→ A `CLAUDE.md` schema you paste and edit: folder map, page types, frontmatter, naming, link rules, the three operations, write rules

→ `index.md` and `log.md` set up the way the idea file describes

→ Copy-paste prompts for the first session, ingest, batch ingest, query, filing answers back, lint, and finding new sources

→ The Obsidian settings checklist

→ When and how to add search once the index is not enough

→ The four skills I run every day, adapted to this setup: ingest, query, lint, and a build loop that enriches the wiki on its own

---

## Contents

1. [Why a wiki and not RAG](#1-why-a-wiki-and-not-rag)
2. [Who does what](#2-who-does-what)
3. [Install](#3-install)
4. [The folder](#4-the-folder)
5. [The schema file](#5-the-schema-file)
6. [index.md and log.md](#6-indexmd-and-logmd)
7. [The three operations](#7-the-three-operations)
8. [Obsidian settings](#8-obsidian-settings)
9. [Search at scale](#9-search-at-scale)
10. [The skills I use daily](#10-the-skills-i-use-daily)
11. [Your first week](#11-your-first-week)
12. [Sources](#12-sources)

---

## 1. Why a wiki and not RAG

Most tools that let an AI read your documents work the same way. You upload files. At question time the system pulls the chunks that look relevant and the model writes an answer from them. Karpathy names NotebookLM, ChatGPT file uploads, and most RAG systems as examples.

His point is that nothing accumulates. Ask a question that needs five documents and the model pieces the fragments together again, every time.

The wiki flips it. When a source arrives, the agent reads it once and folds it into the pages that already exist. Entity pages get the new facts. Topic summaries get revised. Contradictions get flagged against the claims they contradict. By the time you ask a question, the cross-references and the synthesis are already written.

In his words, the knowledge is "compiled once and then kept current, not re-derived on every query."

---

## 2. Who does what

The rule that makes the whole thing work: you never (or rarely) write the wiki yourself.

**You:**
- Pick the sources
- Ask the questions
- Steer what gets emphasized
- Decide what it all means

**The agent:**
- Summaries
- Cross-references
- Filing
- Every page update, every index line, every log line

Karpathy's reason is the core of the pattern: "Humans abandon wikis because the maintenance burden grows faster than the value." An agent touches fifteen files in one pass and does not get bored of it. Maintenance stops being the thing that kills the wiki.

In practice he keeps the agent open on one side and Obsidian on the other, and reads the pages update as they talk.

---

## 3. Install

You need [Obsidian](https://obsidian.md), [Claude Code](https://docs.anthropic.com/en/docs/claude-code) (or Codex, or any agent that reads a schema file), and git.

```bash
git clone https://github.com/davisxai/operator-knowledge-base.git
cd operator-knowledge-base/guides/llm-wiki-setup
bash scripts/new-wiki.sh ~/Documents/MyWiki
```

The script creates the folder below, copies the three templates, writes the first log line, and makes the first git commit. It refuses to overwrite a folder that already exists.

Then:

1. Open `~/Documents/MyWiki/CLAUDE.md` and fill in the Domain line. One or two sentences on what this wiki is about.
2. Open the folder in Obsidian as a vault.
3. Open the agent inside it:

```bash
cd ~/Documents/MyWiki
claude
```

4. Paste the first-session prompt from [prompts/prompts.md](prompts/prompts.md). The agent interviews you and proposes edits to the schema before anything gets ingested.

---

## 4. The folder

```
MyWiki/
├── CLAUDE.md          the schema. The rules for everything below
├── index.md           the catalog. The agent reads it first
├── log.md             append-only record of every operation
├── raw/               your sources. Read-only for the agent
│   └── assets/        images, downloaded locally
└── wiki/              pages the agent writes
    ├── sources/       one summary page per source
    ├── entities/      people, companies, products, places
    ├── concepts/      ideas, methods, themes
    └── answers/       answers worth keeping
```

**raw/ is immutable.** Karpathy calls it your source of truth. The agent reads it and never modifies it. If the wiki ever drifts, the sources are still there to rebuild from.

**wiki/ belongs to the agent.** It creates the pages, updates them, and keeps the links consistent. You read it.

**Start small.** Four page folders is enough for most domains. Add one when a page type keeps showing up that does not fit. A book wiki might add `characters/` and `themes/`. A business wiki might add `clients/` and `decisions/`. Change the schema first, then let the agent create the folder.

---

## 5. The schema file

Karpathy calls the schema "the key configuration file." It is what makes the agent "a disciplined wiki maintainer rather than a generic chatbot." For Claude Code it is `CLAUDE.md`. For Codex it is `AGENTS.md`. The content is the same.

The template in [templates/CLAUDE.md](templates/CLAUDE.md) has seven sections. Each one answers a question the agent would otherwise guess at.

- **Domain.** What the wiki is about. Keeps the agent from filing everything it reads.
- **Folder map.** What each folder is for and who can write to it.
- **Page types and frontmatter.** Every page opens with YAML: type, created, updated, tags, and the source pages it draws on. Each type adds its own fields.
- **Naming.** Lowercase hyphenated slugs. Source pages are date-prefixed. One page per thing, merged, never duplicated.
- **Links.** Every mention of something that has a page gets a `[[wikilink]]`. Every claim links the source page it came from.
- **Operations.** Ingest, query, and lint as numbered steps.
- **Write rules.** raw/ is read-only. Every write gets logged. Every new page gets indexed. Absolute dates. No invented facts.

Treat it as a living file. Karpathy says you and the agent co-evolve it as you learn what works for your domain. When the agent does something you do not want twice, the fix goes in the schema, not in the next prompt.

My own is 73 lines.

---

## 6. index.md and log.md

Two files do the work a vector database would do at small scale. They have different jobs.

**index.md is content.** A catalog of every page in the wiki: a link and a one-line summary, grouped by type. The agent adds a line on every new page. On every question it reads the index first, then opens the pages that look relevant.

Karpathy reports this "works surprisingly well at moderate scale (~100 sources, ~hundreds of pages) and avoids the need for embedding-based RAG infrastructure." My index is 225 lines.

**log.md is time.** Append-only. One line per ingest, query, or lint pass, newest at the bottom. Every line starts with the same prefix:

```
## [2026-04-02] ingest | Article Title
```

The fixed prefix makes the log readable with plain unix tools:

```bash
grep "^## \[" log.md | tail -5
```

That returns the last five operations. The agent uses it to see what was done recently. You use it to see how the wiki grew. My log has 152 entries on that prefix.

---

## 7. The three operations

The exact steps are in the schema. The prompts are in [prompts/prompts.md](prompts/prompts.md).

### Ingest

You drop a source into `raw/` and name it. The agent reads it, tells you the key takeaways, and waits for you to say what matters. Then it writes the source page, updates every entity and concept page the source touches, flags contradictions with both versions kept, updates the index, and logs it.

Karpathy's numbers: "A single source might touch 10-15 wiki pages." He ingests one source at a time and stays involved. Batch ingest works once the schema has held up for a dozen or so sources and you trust what the agent files.

### Query

You ask. The agent reads the index, opens the pages, follows links, and answers with citations to the pages it used. If the wiki does not know, it says so and names the source that would answer it.

The part most setups miss: good answers go back in. Karpathy: "good answers can be filed back into the wiki as new pages." A comparison you asked for, an analysis, a connection you found. Filed in `wiki/answers/`, linked from the pages it draws on. Your questions compound the same way your sources do.

### Lint

Run it weekly, or after a big batch. The agent checks for:

- Contradictions between pages
- Claims a newer source has superseded
- Orphan pages with no inbound links
- Concepts mentioned across pages that still lack their own page
- Missing cross-references
- Pages missing required frontmatter
- Gaps a web search could fill

It fixes the safe ones (links, frontmatter, index lines) and lists the rest for you. Karpathy also uses lint to find what to read next: the agent is good at suggesting the questions the wiki cannot answer yet. That prompt is in the prompts file too.

---

## 8. Obsidian settings

Obsidian is the viewer. The files are the system. These settings come from the idea file.

- **Web Clipper.** The official Obsidian browser extension. Saves a web article as markdown. Point it at `raw/` and clipping becomes the first step of ingest.
- **Attachment folder.** Settings, Files and links, "Attachment folder path", set to `raw/assets/`. Every image lands in one place.
- **Download hotkey.** Settings, Hotkeys, search "Download attachments for current file", bind it (Karpathy suggests Ctrl+Shift+D). After clipping, hit it and the article's images download to disk, so the agent can read them instead of relying on links that break. The agent reads the text first, then views the images.
- **Graph view.** The fastest way to see the shape of the wiki. Hubs show up as dense nodes. Orphans float alone, which tells you what lint should catch.
- **Dataview.** A community plugin that queries frontmatter. Because the agent writes YAML on every page, you get live lists for free: every source ingested this month, every entity of one kind, every page still missing a field.

Two more from the idea file:

- **The wiki is a git repo.** Version history, branches, and diffs of every agent edit. The install script runs `git init` for you. Commit after each session.
- **Marp** turns a markdown page into a slide deck, with an Obsidian plugin. Useful when a query answer should become a presentation.

---

## 9. Search at scale

The index is enough until it is not. When the catalog gets too long for the agent to scan well, add search.

Karpathy's pick is [qmd](https://github.com/tobi/qmd) by Tobias Lütke. A local search engine for markdown with hybrid BM25 and vector search plus LLM re-ranking, all on your machine. MIT, 30,392 stars on 2026-10-14. It ships as a CLI, so the agent can shell out to it, and as an MCP server, so the agent can call it as a native tool.

Add it in the schema: tell the agent to run qmd first on queries and fall back to the index. The wiki itself does not change.

---

## 10. The skills I use daily

The prompts work inside the wiki folder. The skills work from anywhere. I run the same four against my own vault every day, from whatever project I am in, and these are those four adapted to the folder this guide sets up.

- **[/wiki-ingest](skills/wiki-ingest/SKILL.md)** Takes a file in `raw/`, a URL, or pasted text. Saves anything new to `raw/` first, then runs the ingest steps from your schema.
- **[/wiki-query](skills/wiki-query/SKILL.md)** Answers from the wiki only, cites every page it used, and offers to file the answer back.
- **[/wiki-lint](skills/wiki-lint/SKILL.md)** The weekly health check. `report` changes nothing. `fix` repairs links, frontmatter, and index lines, and asks you about anything that changes a claim.
- **[/wiki-build](skills/wiki-build/SKILL.md)** One enrichment pass. It picks the single most valuable gap (an unprocessed source, a missing page, an orphan, a lint finding), fixes it, logs it, and stops.

Install them once:

```bash
cp -R skills/wiki-* ~/.claude/skills/
```

Then open each `SKILL.md` and replace `/ABSOLUTE/PATH/TO/MyWiki` with the path to your wiki. Claude Code picks them up without a restart.

Every skill reads your `CLAUDE.md` before it does anything, so the schema stays the single source of rules. Change the schema and all four change with it.

The build skill is made to run on a loop. Leave this running and the wiki fills its own gaps:

```
/loop 30m /wiki-build
```

---

## 11. Your first week

**Day 1.** Run the install. Fill in the Domain line. Run the first-session prompt and let the agent interview you about the schema. Approve its edits.

**Day 2.** Clip or drop in three sources you already know well. Ingest them one at a time. Read every page the agent touches. When something is filed wrong, fix the schema, not the page.

**Day 3.** Ask five real questions. File the best answer back. Open the graph view.

**Day 4 to 6.** Ingest a source a day. Watch the entity pages fill in from more than one source.

**Day 7.** Install the four skills. Run `/wiki-lint`. Run the find-the-next-sources prompt. Commit.

After a week the agent has a schema that fits your domain and a wiki with enough links to answer questions you did not plan for. From there, batch ingest.

---

## 12. Sources

- Andrej Karpathy, llm-wiki idea file, April 4, 2026: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- qmd by Tobias Lütke: https://github.com/tobi/qmd
- Obsidian Web Clipper: https://obsidian.md/clipper
- Dataview: https://github.com/blacksmithgu/obsidian-dataview
- My own vault's numbers (73-line schema, 225-line index, 152 log entries) counted from disk on 2026-10-14.
