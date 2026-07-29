# Build Your Own

Build order, what to skip, and the failure modes that actually showed up.

The system in this section took months. Most of that time went into things you do not have to repeat. This file is the compressed path.

---

## The order that works

Each stage is useful on its own. If you stop after any of them, you still have something that pays for itself. That is the test for whether the order is right.

### Stage 1: The contract, before any code

Write the rules file first. A markdown file that says what the system is, what it is not allowed to do, and how it writes.

Then the vault schema: the types, the required fields per type, the status vocabularies, the naming rules. See [vault.md](vault.md) for the full shape.

Zero infrastructure. Zero cost. This is the part everyone skips and then rebuilds later, because every downstream decision depends on it. If the frontmatter is not a validated contract, you cannot build views on top of it, you cannot sync entities to a database, and you cannot trust anything an agent wrote.

**Done looks like:** a schema file, one template per type, and the three root files (catalog, recency cache, log) existing even if nearly empty.

### Stage 2: The operating layer on your machine

A global rules file with a project registry and a skill registry inside it. Three to five skills. The permission deny list.

Start with skills for things you already do twice a week. The description field is the whole ballgame: write it as a list of literal phrases you would actually say, not as a summary of what the skill does.

**Done looks like:** you stop typing long prompts for your three most repeated tasks.

### Stage 3: Read-only mail sync

One process, one cron, one direction. Pull mail into a database. No AI, no writes back, no classification.

This is deliberately boring and it is the highest-risk-of-quitting stage, because it feels like it is not doing anything. It is doing the thing everything else needs: giving you a queryable corpus with cursors, per-account state, and a heartbeat.

**Done looks like:** a heartbeat row that updates every minute and per-account cursors that advance.

### Stage 4: Classification

Add a cheap model and a classification tool with a schema-enforced output. Batch it. Cap the body length. Label threads rather than messages, and let the highest-signal category in a thread win.

Inject two things into the prompt that live outside the code: a roster of who matters, and a free-text notes field of your own standing corrections. Both of those will change weekly. Neither should require a deploy.

**Done looks like:** your inbox has labels you did not apply, and correcting a mistake means editing a text field.

### Stage 5: The action queue

A table with a status column. Anything that wants to change the outside world inserts a `proposed` row. A human approves. A separate worker executes approved rows.

Build the approval UI before you build the second action handler. If approving is annoying, you will bypass it, and then you have an agent with unsupervised write access to your email.

**Done looks like:** an agent that says "queued for approval" and means it.

### Stage 6: The daily brief

One scheduled synthesis using a mid-tier model. What needs a human, whether the systems are healthy, where the work stands.

Pull from the tables you already have. Resist making it a news feed.

**Done looks like:** you read it before you open your inbox.

### Stage 7: The chat agent

An agent SDK session with an explicit tool allowlist, its working directory pointed at the vault, and write tools disabled. Reads the vault, proposes email actions, cites the pages it used.

**Done looks like:** you ask it something about your own business and it answers with citations you can click.

### Stage 8: The consolidation loop

The write-enabled agent, run on an interval, doing one bounded pass: orient, gather signal, consolidate, prune and index. Guarded by a minimum interval and a lock with a time to live.

This is last for a reason. An agent with write access to your knowledge base is only safe once the schema, the validation, the write rails, and the log all exist.

---

## What to skip

- **A custom UI framework.** Every component in the dashboard installs from a component registry. Hand-written components are limited to composition and wiring. Design is not where the value is here.
- **Direct networking between machines.** Two processes coordinating through a shared database is less code, less auth, and gives you an audit trail. Only reach for a tunnel when the latency actually matters.
- **A vector database, at first.** A catalog file with a one-line hook per page plus a recency cache answers most retrieval, at zero cost, with citations that are real file paths. Add embeddings when you can name the query that is failing.
- **Multi-tenancy.** If there is exactly one principal, say so out loud, skip the user model, and write down the condition under which that stops being true.
- **A big vendor voice API.** A self-hosted speech server behind OpenAI-compatible endpoints covers both directions with small models.
- **Auto-send, indefinitely.** Drafts are almost all of the value with almost none of the risk.

---

## Failure modes, from production

**The bundle stripped a dependency and crash-looped the service.** Bundling a monorepo down to one file means the runtime manifest has to merge the workspace packages' own npm dependencies, not just strip the workspace entries. Stripping without merging removed the Postgres driver. Audit what your bundled packages depended on.

**A circuit breaker latched the wrong thing.** Every core loop pauses after three consecutive failures. That is correct for most loops and wrong for mail sync, where one quiet account with an expired cursor would take down every account. One deliberate exemption, with the reasoning in a comment.

**The prompt rule did not hold.** There is a post-processing pass that strips em dashes out of model output because the model emits them anyway. If a constraint matters, put it in code. Prompts are guidance, not enforcement.

**The prompt got expensive without anyone noticing.** Dropping detail for low-priority roster entries cut the classifier prompt from roughly 5600 tokens per call to roughly 1900. At one call per ten emails, forever, that is the difference between a system you keep running and one you turn off. Display the cost somewhere you look.

**Capture outran the drain.** 44 unprocessed captures against a vault seven weeks old. Deferred structuring is the right design and it only works if the drain is scheduled and prioritized. Make draining priority one in your loop and make stale-inbox a lint check.

**Entity capture outran reasoning capture.** 76 person pages against 1 decision page. Facts about people accumulate on their own because every document mentions people. Decisions do not, because nothing forces you to write them down. If the reasoning layer is the point, it needs its own explicit prompt.

**Mail credentials expire quietly.** Refresh tokens expire after six months of inactivity. Push subscriptions expire every seven days and need renewal on a cron plus once on boot, so a restart recovers a missed window. Neither failure announces itself.

**Rate limits are per account.** Ten messages maximum per batch metadata fetch, five simultaneous calls maximum per account, back off five seconds plus jitter on a 429, wait a full minute on a 403. The fix for repeated 429s is smaller batches and added delay in code, not a restart.

**Two agents on one mailbox.** An older single-purpose agent already owned the outbound mailbox, so the newer system excludes that account from sync by default. Decide which system owns which surface, and write it down where both can see it.

---

## The tests that tell you it is working

Not benchmarks. Just the honest signals.

- The daily brief gets read before the inbox does.
- Correcting the classifier is editing a text field, not editing code.
- A cold session in a new terminal can find any repo and any procedure without being told.
- You can answer "what do I know about this" from your own notes with citations.
- Nothing the agent does to the outside world happens without a row you approved.
- When something breaks, the system tells you it stopped instead of retrying quietly.

---

## Start here

If you only do one thing this week: write the schema contract and the three root files. Catalog, recency cache, append-only log.

It costs nothing, it runs anywhere, and every later stage reads from it.

---

Built by OperatorOS | [operatoros.ai](https://operatoros.ai)
Follow [@daviss.dev](https://instagram.com/daviss.dev) and [@os.operator](https://instagram.com/os.operator) on Instagram.
