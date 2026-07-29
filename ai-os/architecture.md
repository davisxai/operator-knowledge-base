# Architecture

The runtime. Three processes, one database, and a set of rules about who is allowed to do what.

Read [README.md](README.md) first for the shape. This file covers the mechanisms.

---

## 1. Three processes, one database

- **Dashboard.** Next.js App Router, React 19, TypeScript strict. Runs on the laptop on port 3100, bound to `127.0.0.1`. Uses the pooled Postgres connection.
- **Worker.** Plain Node and TypeScript, bundled to a single file, running on a server under PM2. Uses the direct Postgres connection.
- **Database.** Hosted Supabase project. Drizzle owns the schema. supabase-js provides Realtime.

The pooled versus direct split matters. Migrations and long-lived worker connections go direct. The app goes through the pooler. Running a migration through a pooler is how you corrupt a schema state, so that rule is written down in the project rules and in a database skill.

The monorepo is pnpm workspaces:

```
apps/dashboard    Next.js UI + chat agent + consolidation loop
apps/worker       cron process, Gmail sync, triage, actions, connectors
packages/db       Drizzle schema, migrations, typed client
packages/vault    vault library: index, read, search, watch, safe-write
packages/shared   types, zod schemas, account constants
```

The vault library being its own package is deliberate. Both the dashboard and the tooling need vault access, and the write guards need to live in exactly one place.

---

## 2. The actions table as an approval gate

This is the most portable idea in the system.

The dashboard cannot reach Gmail. The chat agent cannot reach Gmail. Neither holds mail tokens. Both can insert a row into an `actions` table with status `proposed`. A human approves it in an Approvals panel. The worker picks up approved rows every 30 seconds and executes them.

Handlers implemented: mark read, archive, trash, star and unstar, create draft, and re-triage. That last one is an AI reclassify, handled before the Gmail action schema parse.

There is a comment in the source above the draft handler that defines the whole posture:

> Drafts only. Sending is never automated from the worker.

Three properties fall out of this:

- **Least privilege by construction.** The agent is not trusted to be careful. It is structurally incapable of sending mail, because the code path does not exist.
- **A queue is an audit log.** Every action anything ever proposed is a row, with who proposed it and what happened.
- **The UI stays offline-safe.** The laptop can be closed mid-approval. The row is still there.

All Gmail calls in the worker route through a shared backoff wrapper.

---

## 3. What runs on a schedule

Every cron on the worker, timezone fixed to one zone rather than inherited from the host:

- **Every 2 minutes.** Gmail delta sync across accounts, then a thread count reconcile, then a triage tick if an AI key is present.
- **Every 30 seconds.** The actions queue.
- **Every minute.** Heartbeat. Writes a liveness marker plus a row in a `heartbeats` table, and prunes heartbeat history to seven days.
- **Every 30 minutes.** RSS content feed ingestion. Needs no AI key.
- **Daily.** The brief, at a time configured in settings. A helper converts a stored "HH:MM" string into a cron expression, so the schedule is user data rather than a constant.
- **Per connector.** Each connector declares its own cron.

Boot order in `main()` is intentional: start HTTP listeners first so the webhook is reachable, then ensure accounts, then backfill any account with a null cursor, then seed feeds, then heartbeat, then connector boot ticks, then schedule. The listener goes first because the initial backfill can run long and you do not want to be unreachable while it does.

The binary also takes one-shot flags for operations work: probe, re-triage the whole backlog, re-apply labels from existing triage without any AI calls, generate today's brief on demand, run one outreach mirror pass, seed and ingest feeds once. Every long-running loop should have a way to run exactly one iteration from the command line.

---

## 4. Gmail triage

The classifier is the highest-volume AI call in the system, so most of its design is about bounding cost.

**Batching.** Ten emails per tick, body truncated at 4000 characters. A backlog drains across successive ticks rather than in one burst. Cost and latency stay bounded no matter how far behind the queue gets.

**Structured output.** The model is given a tool with a zod-derived input schema and told to call it. Output shape is enforced by the schema, not by parsing prose.

**Seven categories, ranked.** In the code they are `action_needed`, `reply_needed`, `client`, `fyi`, `operatoros`, `newsletter`, `spamish`, ordered highest signal first. A thread takes the top ranked category among its messages, so one real message keeps an entire thread out of the spam bucket. The resulting label applies to the whole thread in Gmail, not the single message.

The ranked-rollup rule is the part people miss. Classify messages, label threads, and let the highest signal win.

**Two runtime inputs get injected into the prompt.**

- A **roster context** built from a `vault_entities` table, sorted by tier. Those entities are synced out of the Obsidian vault, so the knowledge layer is what tells the classifier who matters. If the vault has not synced, it falls back to a hardcoded roster.
- **Standing notes**, read from a settings key. My own accumulated guidance, and the prompt says to follow it over the defaults when the two conflict. Correcting the classifier is editing one text field, not editing code.

A comment in the roster builder records a real optimization: dropping notes for lower tiers cut the prompt from roughly 5600 tokens per call to roughly 1900. At one call per ten emails, forever, that is the difference between a system you keep running and one you turn off.

**Notification dedupe** uses a six hour window, so ten emails from one source do not become ten pings.

**Prompt rules that ended up mattering.** Machine-generated third-party mail is never marked as needing action or a reply. Cold outbound and recruiting spam is spam-ish no matter how personalized it is. Confidence has to be stated honestly. Summaries are one direct sentence with no filler.

One account is excluded from sync by default: the outbound automation mailbox, which belongs to a separate, older, single-purpose email agent built on a different framework. It runs on the same box and is treated as untouchable. Two agents writing to the same mailbox is a bug waiting to happen.

---

## 5. The chat agent

Built on the Claude Agent SDK. Four files: the agent, the model, the system prompt, the tools.

- The working directory is set to the vault path.
- No inherited settings. Partial message streaming on, for token-by-token UI.
- Two in-process MCP servers created at runtime, one for vault, one for email. Tools are defined in the same codebase they serve, with no separate process to run.
- Tools are an explicit allowlist. Vault gets search, read, list. Email gets list threads plus five propose tools.
- `Write`, `Edit`, and `Bash` are explicitly disallowed.

The source comment is the clearest statement of the pattern:

> `list_threads` is the only direct read. The `propose_*` tools never touch Gmail. They insert `proposed` rows into the actions table for the Approvals panel.

The system prompt then reinforces it in language: the agent must say an action is queued for approval, never that it is done.

The prompt also encodes a **three-layer retrieval order** over the vault: read the hot file first, then the index or a map of content, then specific pages. Plus a rule to cite the pages used, and to say so plainly when the vault does not know something.

There is a separate one-line module whose only export is the model id. The comment on it says it exists so the UI badge can never lie about which model answered. Small thing, and exactly right.

The chat route runs on the Node runtime with a five minute max duration, streams over SSE, and persists conversations, messages, and agent runs, recording tool calls with output capped at 4000 characters.

---

## 6. The nightly consolidation loop

A second agent, same SDK runtime, different tool grant. This one can write to the vault.

Four phases in the prompt:

1. **Orient.** Read the hot file and the index.
2. **Gather signal.** Recent emails, recent chat turns, agent runs, the latest brief, recently changed pages.
3. **Consolidate.** Surgical page updates. Resolve contradictions. Create new pages only for genuinely new entities.
4. **Prune and index.** Rewrite the hot file as a roughly 500 word current-state cache. Refresh the index.

Two guardrails keep it from running away:

- A minimum interval of one hour between completed runs.
- A lock with a 30 minute time to live, so a crashed run does not block the next one forever.

Runs are recorded with token and cost fields. It is triggered from the UI or a CLI script, not from cron.

The notable priority call: my own chat turns with the agent are treated as the highest-priority, most authoritative signal, above emails and above existing pages. If I said it in conversation, that is the current truth.

---

## 7. Model tiering

Three jobs, three models, chosen by volume and by whether a human reads the output.

- **Triage.** A small fast model. High volume classification, so speed and cost dominate.
- **Daily brief.** A mid model. Runs once a day and gets read carefully, so quality of synthesis is worth paying for.
- **Chat.** The frontier model. Low volume, interactive, and the reasoning is the product.

Subagent calls elsewhere in the setup pin a mid-tier model explicitly rather than inheriting the frontier default, and fan-out is capped at roughly twenty subagents.

---

## 8. Resilience

**Circuit breakers.** Each core loop (triage, actions, brief, content) has one. Three consecutive failures pauses that loop for the rest of the process lifetime and writes a notification row. The system tells you it stopped instead of quietly retrying forever.

**One deliberate exemption.** Gmail incremental sync opts out of the shared breaker and owns its own resilience. The reasoning is in the code: one quiet account with an expired cursor should not be able to latch the entire mailbox set.

**Degraded mode is explicit.** With no AI key, the worker logs that AI jobs are disabled and runs as pure Gmail sync. The mail keeps flowing. A missing key is a reduced feature set, not a crash.

**The connector plane.** Integrations are a registry, not a pile of if-statements. A connector declares an id, a label, the environment keys it needs, an optional cron and tick, an optional boot tick, an optional breaker opt-out, and an optional long-lived HTTP listener. If any declared key is missing, the connector is skipped at boot. Adding an integration is adding a file to a registry.

Registered connectors, by function: an inbound webhook receiver for mail delivery events with signature verification, a read-only mirror of the server's own container platform, an outreach analytics mirror, and a pure SQL geocode fill that reads from a reference table and makes zero external calls.

**Host metrics come from the OS, not the API.** The server monitoring panel reads CPU, memory, disk, and uptime straight off `/proc`, because the container platform's REST API does not expose live metrics. Inventory and health come from the API, per-container usage from `docker stats`, and the whole snapshot upserts into one settings row rather than getting its own tables.

---

## 9. The daily brief

Runs on the configured daily cron, respects a settings kill switch, upserts one row per local date, and drops a notification.

What it assembles:

- Emails still marked as needing action or a reply over the last seven days, not just today, capped at 40 rows and ordered by priority.
- Pending proposed actions, capped at 25.
- Open unread worker alerts from the last week. Breaker trips and sync failures.
- Active leads and deals filtered to in-flight pipeline states only.

The stated intent, from the source comment: what needs me, whether my systems are healthy, and where the pipeline stands. Deliberately not a news feed. The content radar is a different panel.

Two implementation details worth copying:

- A **sanitize pass** on model output that strips em dashes, en dashes, and double hyphens, because the model emits them despite the instruction. Style enforcement belongs in code.
- A **rate table** keyed by model family prefix, used to label the cost of each run. You cannot manage a token bill you never display.

---

## 10. Voice

Self-hosted, not a vendor API. Two routes proxy to a Speaches server behind OpenAI-compatible endpoints: one for speech synthesis, one for transcription. A small ONNX TTS model, a small faster-whisper STT model, mp3 out, a 2000 character cap on input. Both routes return a clean 503 when the environment is not configured.

Voice is the piece most people assume needs a big vendor. It does not.

---

## 11. Deployment

The dashboard is never deployed. It runs locally with a dev command that I run myself.

The worker deploys with a script:

1. Bundle the workspace packages and the ORM into a single output file. Only true npm runtime dependencies stay external.
2. Sync the bundle, a runtime-only `package.json`, and the process manager config to the server.
3. Install production dependencies on the box.
4. Reload the process by name and save the process list.
5. Health check, then tail the last twenty log lines.

No monorepo on the server, no pnpm on the server, by design. The box gets a file and a manifest.

Process config sets a memory ceiling that triggers a restart, exponential backoff between restarts, production node env, and a fixed timezone.

> [!WARNING]
> The real lesson from this pipeline: the runtime manifest has to **merge** the workspace packages' own npm dependencies, not just strip the workspace entries. Stripping without merging removed the Postgres driver and crash-looped the worker in production. If you bundle a monorepo down to one file, audit what the bundled packages depended on.

Quality gates after any change: typecheck and lint from the repo root. Not optional, not a separate decision.

---

## 12. Operations runbooks

Runbooks live as skills, so the debugging procedure is loaded on demand instead of remembered.

The mail sync runbook, in order:

1. Check the sync state table. Is the heartbeat under two minutes old, are per-account cursors advancing, are cron lock keys stuck.
2. Check the process list and logs for crash loops, auth grant failures, or rate limit spam.
3. Check rate limits.

The Gmail limits it has to respect are written into the runbook: ten messages maximum per batch metadata fetch, five simultaneous calls maximum per account, back off five seconds plus jitter on a 429, wait a full minute on a 403, and remember each account has its own quota. The documented fix for repeated 429s is smaller batches and added delay in code. Not a restart.

---

## 13. Schema and data

26 tables under 14 applied migrations. The groups:

- **Mail.** accounts, threads, emails, triage.
- **Agent.** conversations, messages, agent runs.
- **Ops.** actions, notifications, heartbeats, sync state, daily briefs, events.
- **Knowledge.** vault entities, clients.
- **Pipeline.** leads, outreach campaigns and snapshots, deals, outbound emails.
- **Content.** feeds, items, angles, hooks, scripts.
- **Reference.** a city centroid table used for offline geocoding.

Two rules, both written down: never edit an applied migration, generate a new one; and read the generated SQL before applying it.

---

## 14. Security posture, stated honestly

The project rules carry an explicit accepted-risk note rather than a vague claim of being secure.

- The system is **single tenant.** Exactly one principal. There is no user model and no owner column on any table.
- The dashboard **binds to loopback** and is not network exposed.
- The only public surface is one webhook endpoint on the worker, with signature verification.
- Automated scanners flag the update and delete by id routes as broken access control. Under a single-principal model those are documented as accepted-risk false positives.

And the tripwire, which is the part that makes the whole note credible:

> [!IMPORTANT]
> Before the dashboard is ever served on a public URL, it must first get a real auth layer at the app boundary covering every route, plus an ownership model if it ever goes multi-user.

Writing down the condition that invalidates your security model is worth more than writing down the model.

---

Built by OperatorOS | [operatoros.ai](https://operatoros.ai)
Follow [@daviss.dev](https://instagram.com/daviss.dev) and [@os.operator](https://instagram.com/os.operator) on Instagram.
