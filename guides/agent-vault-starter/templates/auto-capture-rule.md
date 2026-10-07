# Auto-capture rule

Paste this block into `~/.claude/CLAUDE.md` so every Claude Code session on your machine carries it. Replace the path. This is the rule that turns every session into an ingestion event: the agent writes to the vault without being asked.

---

## Knowledge layer

The vault at `/ABSOLUTE/PATH/TO/vault` is where all real operational information lives. It is an agent-maintained wiki (people, companies, clients, projects, decisions, sources). I rarely write it by hand. You maintain it.

**Auto-capture rule. Do this without being asked.** Whenever real operational information surfaces in any project, capture it to the vault as part of finishing the work. Do not ask permission. Just do it and mention it in one line. This covers:

- **Client and deal facts.** New facts, status changes, scope, money, dates, contacts, decisions, commitments.
- **Notes.** Meeting and call notes, takeaways, and anything I say to "note", "remember", or "save".
- **Important emails.** Whenever I have you pull, read, or summarize important emails, land them in the vault too.

How to capture:

- Quick capture: append a short timestamped markdown file to `/ABSOLUTE/PATH/TO/vault/inbox/`. The ingest operation drains it later.
- Substantial item (client update, transcript, key email thread): run the `/vault-ingest` skill, callable from any project. It lands the raw material in `sources/YYYY/`, creates or updates the wiki and ops pages, cross-links, and updates `index.md`, `hot.md`, and `log.md`.
- Follow the vault contract at `/ABSOLUTE/PATH/TO/vault/CLAUDE.md`. Never invent facts. No emojis, no tables, no em or double dashes, absolute dates.

Vault skills callable from anywhere: `/vault-ingest`, `/vault-query`.
