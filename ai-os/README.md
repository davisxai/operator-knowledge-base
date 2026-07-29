# AI OS

The AI operating system I actually run. Not a rendered HTML page pretending to be Jarvis.

This section documents the working version: what processes run, where state lives, which model does which job, what the agent is allowed to touch, and the parts that broke in production. It is written for someone who wants to build their own, so it stays at the level of design decisions and mechanisms rather than screenshots.

Inventory date: 2026-07-29. Everything here traces to files in the actual repos.

> [!NOTE]
> Client names, contract values, credentials, server addresses, and vault contents are deliberately excluded. What is left is the architecture, and the architecture is the interesting part anyway.

---

## What it does

Four jobs, running every day.

- **Mail.** Three Gmail accounts sync into one database. Every thread gets classified by a model into one of seven categories and labeled back in Gmail.
- **Knowledge.** An Obsidian vault on disk holds people, companies, concepts, decisions, and business state as markdown. An agent writes it. I mostly read it.
- **Chat.** An agent with read access to the vault and propose-only access to email. It answers from the vault and cites the pages it used.
- **Brief.** One generated summary each morning: what needs a human, whether the systems are healthy, where the pipeline stands.

Everything else is support for those four.

---

## The honest shape

The dashboard runs on my laptop, bound to loopback. It is not on the internet. The always-on half runs on a server. Those two halves never talk to each other directly. They both talk to a hosted Postgres database over TLS, and that is the only shared surface.

That decision drives most of the design. If the local UI wants the server to archive an email, it inserts a row into an `actions` table. The server picks it up, does the work, writes the result back. No tunnel, no open port on the laptop, no service discovery.

```
      LOCAL MACHINE                                  SERVER
+---------------------------+                +------------------------+
|  Dashboard (Next.js)      |                |  Worker (Node)         |
|  bound to 127.0.0.1:3100  |                |  always on, PM2        |
|                           |                |                        |
|  - panels + command bar   |                |  - Gmail delta sync    |
|  - chat agent (Opus)      |                |  - triage (Haiku)      |
|  - nightly consolidation  |                |  - daily brief (Sonnet)|
|  - vault filesystem I/O   |                |  - actions queue       |
|                           |                |  - connectors          |
+-------------+-------------+                +-----------+------------+
              |                                          |
              |  TLS                                TLS  |
              v                                          v
      +--------------------------------------------------------+
      |            Postgres (hosted Supabase)                   |
      |  threads / emails / triage / actions / runs / briefs    |
      |  notifications / sync_state / vault_entities / clients  |
      +--------------------------------------------------------+
              ^
              |  read + guarded write
              |
+-------------+-------------+
|  Obsidian vault (markdown)|
|  sources/ wiki/ ops/      |
|  index.md hot.md log.md   |
+---------------------------+
```

One public endpoint exists on the server: a signed webhook receiver for email delivery events. Nothing else is exposed.

---

## Component map

- **Dashboard.** Next.js App Router app on the laptop. Sixteen panels driven off one declarative registry, so the sidebar, command palette, and router all derive from a single array. Hosts the chat agent runtime and the nightly vault consolidation loop. Has direct filesystem access to the vault.
- **Worker.** Plain Node and TypeScript on a server under PM2. Cron jobs, Gmail sync, triage, the actions queue, a heartbeat, and a connector registry. Mail tokens live only here.
- **Database.** Hosted Postgres. Drizzle owns the schema and migrations. 26 tables, 14 applied migrations. Also the message bus between the two processes.
- **Vault.** Obsidian-compatible markdown on disk. Three layers split by mutability, not by topic. Its own contract file, schema, templates, and four canonical operations.
- **Claude Code layer.** The developer-machine operating layer that builds and drives all of the above. A global constitution file, 66 skills, 19 agents, MCP servers, hooks, and per-project memory.

---

## Files in this section

- **[architecture.md](architecture.md)** The runtime. Three processes and one database, the actions queue as an approval gate, Gmail triage design, cron cadences, the connector plane, model tiering, the voice layer, deployment shape, and the stated security posture.
- **[vault.md](vault.md)** The agent-maintained second brain. Split by mutability, the index/hot/log triad, frontmatter as a validated contract, the four operations, and how autonomous enrichment stays bounded.
- **[claude-code-layer.md](claude-code-layer.md)** Claude Code configured as a business operating system. CLAUDE.md structure, the skills library, agent tiering, the MCP lineup by name, hooks and permissions, and the memory pattern.
- **[build-your-own.md](build-your-own.md)** Build order, what to skip, and the failure modes that showed up in production.

---

## Three things worth taking even if you build nothing else

**The database is the message bus.** Two processes that never speak directly, coordinating through rows. It removes an entire class of networking and auth problems, and it gives you an audit trail for free.

**Propose, then approve.** The chat agent cannot touch Gmail. Its email tools insert `proposed` rows into the actions table for a human to approve in the UI. Sending is not implemented at all. The most the agent can do is propose a draft.

**Prompt rules are not enforcement.** There is a post-processing pass in the brief generator that strips em dashes out of model output, because the model emits them anyway despite being told not to. If a constraint matters, put it in code, not in a prompt.

---

Built by OperatorOS | [operatoros.ai](https://operatoros.ai)
Follow [@daviss.dev](https://instagram.com/daviss.dev) and [@os.operator](https://instagram.com/os.operator) on Instagram.
