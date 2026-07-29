# MCP Servers, Knowledge, and Infrastructure

The servers that give an agent access to real systems, the tools that give it memory, and the infrastructure underneath.

Back to [resources](README.md).

## MCP servers

**[Playwright MCP](https://github.com/microsoft/playwright-mcp)** MIT
- Microsoft-maintained browser automation driven by the accessibility tree, not pixels.
- The base layer for anything browser-shaped. Fast and cheap because no vision model is in the loop. Persistent browser profiles carry login state, which is the only reason UI-only platforms are automatable at all. Install: `claude mcp add playwright npx @playwright/mcp@latest`.

**[Stagehand](https://github.com/browserbase/stagehand)** MIT
- Semantic `act`, `extract`, and `observe` calls layered on top of Playwright, with auto-caching so the second run skips the model call.
- Add it for any UI workflow you re-run on a schedule, because it survives UI drift. For one-shot automation Playwright MCP alone is enough. The `act` and `extract` calls bill LLM tokens, so it is not free to run.

**[shadcn MCP](https://ui.shadcn.com)**
- Component registry search and install commands, exposed as agent tools.
- The only component source in this setup. Hand-rolled primitives are banned here because the registry version is already accessible, tested, and themed. Ask the registry before you write a dialog.

**[google_workspace_mcp](https://github.com/taylorwilsdon/google_workspace_mcp)**
- Gmail, Calendar, Drive, and Docs over MCP. Install with `uv tool install workspace-mcp`.
- Run one server instance per mailbox, not one server that switches accounts. Each instance gets its own tool namespace and its own cached OAuth token, so which account you hit is unambiguous and visible in the transcript. Service accounts with domain-wide delegation looked like the clean path and did not work in the version tested.

**[Semgrep](https://semgrep.dev)**
- Static analysis with a Claude Code plugin.
- Good demonstration that static analysis belongs inside the agent loop rather than as a separate CI step. Use it as a pre-commit signal, not as a security guarantee.

### Passed on

- **[Browser-Use](https://github.com/browser-use/browser-use)** Real value for one-shot natural-language browser tasks. Playwright MCP plus Stagehand already covers roughly 90% of the work. Add later if a gap actually shows up.
- **[Skyvern](https://github.com/Skyvern-AI/skyvern)** Genuinely excellent at enterprise form flows and overkill below that scale. Revisit when a client has hundreds of near-identical forms to fill.

> [!TIP]
> Tier your automation deliberately. Dedicated MCP for the target app first. Browser automation second, for web apps with no dedicated server. Desktop control last, and only for native apps and cross-app workflows. Driving a web app through pixel clicks when an API exists is the most common waste in this whole category.

> [!NOTE]
> If you run many MCP servers, turn on tool search. When MCP tool descriptions exceed roughly 10% of the context window, tools load on demand instead of all being preloaded, cutting MCP context usage by up to 95%. Set `ENABLE_TOOL_SEARCH` to `auto` (the default), `auto:N` for a custom threshold, `true`, or `false`.

## Knowledge and memory

**[Obsidian](https://obsidian.md)**
- Local-first markdown notes with wikilinks and a plugin API.
- The knowledge layer here is a plain Obsidian vault that an agent maintains and a human reads. Choose it because the files stay useful without the app. Do not use it as a database: structured state belongs in Postgres.

**[Graphiti](https://github.com/getzep/graphiti)**
- Temporal knowledge graph for agent memory. Facts that change over time get versioned rather than overwritten.
- That versioning is the actual failure mode of flat markdown memory, which is what makes it worth the setup cost. The setup cost is a Neo4j backend. Cited P95 retrieval around 300ms in the 2026-04 pass. Ships a community MCP wrapper.

**[Mem0](https://github.com/mem0ai/mem0)**
- Simpler memory API than Graphiti, production-grade.
- Evaluate it when Graphiti feels heavy for what you are doing. AWS selected it as a memory provider for their agent SDK, so it is not a weekend project.

**[Joern](https://joern.io)** Apache-2.0
- Code Property Graph analysis. Merges AST, control flow graph, and program dependence graph into one queryable structure with a Scala query language.
- The gold standard for understanding code flow, used in real vulnerability research. No native LLM integration, which is exactly the gap.

**[FalkorDB](https://falkordb.com)**
- Lightweight fast graph database with an existing code-graph demo.
- The pick when Neo4j is more infrastructure than a code graph justifies.

**[tree-sitter](https://tree-sitter.github.io/tree-sitter/)**
- Incremental multi-language parser.
- The parsing layer under most code-aware tooling, including Aider's repo map. Use it when you need structure without dumping whole files into context.

**[Linear](https://linear.app)**
- Issue tracker with a well-built MCP server.
- Use it as the agent's write surface for work state. Every significant work item gets an issue, created by the same skill that did the work. That is what keeps the tracker honest.

### The three-layer memory architecture

```
  agent
    |
    +--> temporal memory (Graphiti / Mem0)      what changed, and when
    |
    +--> property graph (FalkorDB / Neo4j)      structure and relationships
    |
    +--> tree-sitter parse layer                fast incremental parsing

  all three exposed as MCP servers and queried on demand,
  instead of carried in context
```

> [!NOTE]
> The open gap, stated plainly: nothing combines code-property-graph structural understanding with temporal agent memory in one system built for AI coding assistants. A Joern MCP server does not exist. That is a real, unclaimed contribution if you want one.

## Automation and infrastructure

**[n8n](https://n8n.io)**
- Self-hostable workflow automation with several hundred integrations and a fair-code license.
- The default automation layer in client builds, because the client can own the instance from day one and see every run. Not the pick once the logic is complex enough to want a real codebase and tests.

**[Supabase](https://supabase.com)**
- Postgres with auth, storage, realtime, and a typed client.
- The default database for client work. Use the pooled connection from the app and the direct connection for migrations. Never migrate through the pooler. Free-tier session pooling caps clients around 15, so set a small connection pool max.

**[Drizzle ORM](https://orm.drizzle.team)**
- TypeScript ORM where schema and migrations are code.
- Good because the generated SQL is reviewable before it runs. One rule that has held every time: never edit an applied migration, create a new one.

**[better-sqlite3](https://github.com/WiseLibs/better-sqlite3)**
- Synchronous SQLite bindings for Node.
- Right choice for single-node apps with real query volume, in WAL mode. It is a native module, so a Node version bump breaks it and a macOS build will not run on Linux. Do not import it at module top level in a component, or your production build will try to touch a database that does not exist yet.

**[PM2](https://pm2.keymetrics.io)**
- Node process manager with restart policies, log management, and a saved process list.
- Fine for a single VPS. Set a memory restart ceiling and an exponential backoff restart delay so a crash loop does not pin the box. Not a substitute for containers when you need real isolation.

**[Coolify](https://coolify.io)**
- Self-hosted deployment platform, an open source alternative to hosted PaaS.
- Good app and service inventory over an API. Its REST API does not expose live host metrics, so read CPU, memory, and disk off `/proc` directly and pull container usage from `docker stats`.

**[Vercel](https://vercel.com)**
- Hosting built for Next.js.
- Default for marketing sites and anything that benefits from edge caching. Move to a plain VPS the moment the app needs a long-lived process, a persistent socket, or a native module.

**[Playwright](https://playwright.dev)**
- Browser automation and end-to-end testing.
- Use it for assertions about what a user actually sees. The single most valuable one I have written checks that the rendered page references a CSS asset and that the asset is served as `text/css`, which catches the classic standalone-build failure where the page deploys completely unstyled.

**[Vitest](https://vitest.dev)**
- Fast unit test runner for TypeScript.
- Default unit runner. Gate your background schedulers and webhook listeners behind a test-mode flag, or the suite hangs instead of failing and you lose an hour.

**[pnpm](https://pnpm.io)**
- Package manager with a content-addressed store and first-class workspaces.
- Pin the version in the `packageManager` field and let Corepack read it. `pnpm@latest` in a Dockerfile is how you get a surprise major version that changes how built dependencies are handled.

**[tsup](https://tsup.egoist.dev)**
- esbuild-powered TypeScript bundler.
- Good for bundling a monorepo worker into one file so the server needs no monorepo tooling at all. When you strip workspace dependencies out of the deployed manifest, merge their own npm dependencies in. Stripping without merging crash-loops the process on a missing driver.

**[Zod](https://zod.dev)**
- TypeScript-first schema validation.
- Use it at every boundary: API input, agent tool input, environment parsing. Derive tool schemas from it rather than hand-writing JSON Schema twice.

**[Resend](https://resend.com)**
- Transactional email API with delivery webhooks.
- Good for net-new outbound. Wrong tool for in-thread replies: use the Gmail API there or you break threading.

**[Svix](https://svix.com)**
- Webhook signature verification and delivery.
- Run the verification library on any inbound webhook you expose publicly. It is the cheapest real security control available on that surface.

**[IndexNow](https://www.indexnow.org)**
- Ping protocol telling search engines to recrawl specific URLs.
- Run it after every deploy. Bing, Yandex, DuckDuckGo via Bing, and Seznam participate. Google does not, so this supplements a sitemap rather than replacing one.

### Gmail API rate discipline

If you automate a mailbox, these are the numbers that actually bind. Measured, not documented.

- **Batch reads at 10 messages, not 25.** The documented batch ceiling is 100. Concurrency triggers 429s long before that. For full message bodies, drop to five per call.
- **Use metadata format when you only need headers.** Subject, from, and date cost materially less quota than full bodies. Most triage never needs the body.
- **Fetch threads, not messages.** A thread is one API call regardless of how many messages it holds.
- **Search is cheap, reads are expensive.** Search wide, read narrow. Paginate rather than pushing page size past 50.
- **Error handling is asymmetric.** A 429 means back off 5 seconds and retry. A 403 rate limit means wait 60 seconds. Treating them the same causes cascading failures. Repeated 429s mean smaller batches, not more retries.
- **Sends are a one-way door.** Require explicit human confirmation on every send, enforced through a permission rule rather than an instruction in a prompt.

---

Built by OperatorOS | [operatoros.ai](https://operatoros.ai)

Follow [@daviss.dev](https://instagram.com/daviss.dev) and [@os.operator](https://instagram.com/os.operator) on Instagram.
