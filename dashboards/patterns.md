# Dashboard Patterns

The stack I actually use, and the patterns underneath it.

Everything here comes from two builds. One is a production agent orchestration dashboard that ran more than 160 API routes, 36 panels, 16 overview widgets, one Zustand store, and a server sent events layer. The other is the small teaching build in [mission-control.md](mission-control.md).

The framework spine is identical in both. That is not a coincidence. It is the point.

## Contents

- [The stack](#the-stack)
- [Component source: shadcn, and only shadcn](#component-source-shadcn-and-only-shadcn)
- [Design tokens](#design-tokens)
- [Layout patterns](#layout-patterns)
- [Realtime and data patterns](#realtime-and-data-patterns)
- [Principles that show up in both builds](#principles-that-show-up-in-both-builds)

---

## The stack

This is not aspirational stack talk. It is what is in the lockfile.

- **Framework** Next.js 16, App Router
- **UI** React 19, TypeScript 5.7
- **Runtime** Node 22 or newer, enforced by a version check script that runs before dev, build, lint, typecheck, and test
- **Styling** Tailwind CSS 3.4 plus `tailwindcss-animate`, with CSS custom properties as the token layer
- **Components** shadcn/ui on Radix primitives, `class-variance-authority` for variants, `clsx` and `tailwind-merge` behind a `cn()` helper
- **Icons** lucide-react, exclusively
- **Motion** Framer Motion, one shared easing curve across the whole app
- **Theming** next-themes, dark default, light option, nothing else
- **Charts** Recharts for cost and token analytics
- **Node graphs** `@xyflow/react` for flow and architecture views, `reagraph` for the knowledge graph view
- **State** Zustand with `subscribeWithSelector`. One store, not many
- **Validation** Zod
- **Logging** pino on the server, a thin client wrapper in the browser
- **Testing** Vitest with jsdom for units, Playwright end to end against a production build

### The data layer is the one thing that changes

- **Production single operator app** better-sqlite3 with a raw `schema.sql` and a hand rolled migration runner. WAL journaling, `synchronous = NORMAL`, `foreign_keys = ON`, and `busy_timeout = 5000` so concurrent Next.js route handlers do not trip over each other.
- **Anything you teach a stranger to deploy** Supabase Postgres with Drizzle. No SQLite, no raw SQL.

A local first app that one person runs gets an embedded file database. A thing other people deploy gets managed Postgres. Pick by who operates it, not by what is trendy.

> [!TIP]
> Split the schema in two. Put the founding tables in a plain `schema.sql`. Put everything added after launch in a migrations file applied on module load and tracked in a `schema_migrations` table. In the production build that was 9 tables in SQL and 34 more in migrations.

One more detail that saves a build failure. Skip schema initialization during the production build phase so the build never needs a live database. That is also why you never import the database at the top level of a component module.

---

## Component source: shadcn, and only shadcn

Standing rule. shadcn is the component source. No hand rolled primitives. No scraping component marketplace sites.

What that looks like in practice:

- **`components.json` is committed and configured.** RSC on, TSX on, base color neutral, CSS variables on, icon library lucide. Aliases map `@/components`, `@/components/ui`, `@/lib`, `@/lib/utils`, `@/hooks`.
- **The `ui/` folder stays small.** The shipped product held 11 files there. Primitives get added by the CLI when a screen needs them. They do not get pre installed as a kit.
- **Primitives get edited, not wrapped.** `Card` was cut down to a `rounded-2xl` div with two project utility classes and three exports. `Button` kept the CVA structure, swapped every color for project tokens, added a `success` variant and four icon sizes. You own the file. Change the file.
- **Composition happens above `ui/`.** Domain components live in `components/dashboard/`, `components/panels/`, `components/layout/`. Nothing domain specific leaks into `ui/`.
- **Radix packages appear individually** in the lockfile. `react-slot`, `react-tabs`, `react-dialog`, `react-tooltip`. That is the signature of CLI added components rather than a blanket install.
- **shadcn is wired as an MCP server** so an AI coding agent can search and view registry items directly instead of guessing at component APIs.

For a dashboard specifically, start from a whole shadcn block rather than individual primitives:

```bash
npx shadcn@latest add dashboard-01
```

That is a sidebar, KPI cards, a chart, and a data table in one command.

> [!NOTE]
> I use the raw block instead of a batteries included dashboard starter template on purpose. The starter hides the data layer, and the data layer is the entire lesson.

---

## Design tokens

Four structural colors. Black, white, dark gray, light gray. Color is reserved for meaning, never decoration.

- Surfaces and borders are CSS variables mapped into Tailwind. Primary, secondary, tertiary, hover, active, elevated, sunken for surfaces. Subtle, default, strong, focus for borders.
- Light surfaces run `#FFFFFF` down to `#EBEBEB`. Dark surfaces sit around `#1a1a1a` with `#111111` sunken and `#222222` hover. Never pitch black.
- **Cherry red `#d2042d` is the AI accent. Blue 600 is the human accent.** That split is enforced as two paired token scales, each with subtle, muted, border, and strong steps. So "an agent did this" is a color you can read at a glance.
- Status colors are green and red at 10 to 20 percent alpha with a matching text color, not solid fills.

Two lessons in that setup.

First, semantic color pairs beat a rainbow. If your dashboard shows both human and machine activity, encode the difference in the token layer once. Then every panel gets it for free.

Second, namespace your token variables with a short prefix. Pick it thinking it will outlive the product name, because it will. Renaming what users see is a commit. Renaming every internal identifier is a risk you will decline, and then you live with the fossil.

---

## Layout patterns

### Route shape

One catch all route rendered the entire dashboard, with a server side allowlist gating it.

```
app/
  [...panel]/
    page.tsx            server component, checks slug, calls notFound()
    dashboard-shell.tsx client shell that actually renders
  (marketing)/
    layout.tsx          separate route group, separate layout
```

`page.tsx` is an async Server Component. It reads the slug and calls `notFound()` unless the slug is in a `KNOWN_PANELS` set or belongs to a plugin panel registered at runtime.

> [!WARNING]
> The allowlist is a real bug fix, not theory. Without it, every unknown top level URL rendered the dashboard shell with HTTP 200. Search engines read that as a soft 404 and the site would not index. Thirty three slugs were enumerated by hand and kept in sync with the shell router and the nav rail item IDs.

### Shell composition

Nav rail on one side. Header bar on top. Optional live feed drawer. Content router in the middle. Global overlays mounted at the shell level.

The URL is the source of truth for the active panel. It syncs one way into the Zustand store on every pathname change. Legacy slugs redirect. Navigation timing is instrumented on both the pathname change and the store change.

The shell also runs a nine step boot sequence with visible labeled steps: auth, capabilities, config, connect, agents, sessions, projects, memory, skills. Each step flips to done when its fetch resolves. `bootComplete` flips only when all nine are done. It is a loading state that tells you what it is loading.

### Widget grid

The overview panel is not a fixed layout. It is a catalog plus a user ordered list.

- **`WIDGET_CATALOG`** is a flat array of descriptors. Each has `id`, `label`, `description`, `category`, `modes`, `defaultSize`, and `component`.
- **`WIDGET_COMPONENTS`** is a plain string to component map. Adding a widget is one catalog entry plus one map entry.
- **Sizes map to grid spans, not pixel widths.** On a 12 column grid: `md` is `col-span-4`, `lg` is `col-span-8`, `full` is `col-span-12`, and `sm` narrows only at the `xl` breakpoint.
- **Layout is a persisted array of widget IDs** in the store. Drag and drop reordering sits behind a customizing toggle, with a hidden widgets tray for anything available but not placed.
- **Layout is filtered against the current mode on every render.** A stored layout holding a widget that is invalid for the current mode degrades instead of crashing.

### The data prop pattern

This one is worth copying verbatim. Every widget receives one `DashboardData` object containing:

- Raw payloads. System stats, database stats, provider stats.
- Per source `loading` booleans. One per fetch, not one for the page.
- Collections. Sessions, logs, agents, tasks.
- Connection state.
- Callbacks. `navigateToPanel`, `openSession`.
- **Pre computed derived values.** Memory percent, disk percent, active sessions, error count, online agents, running tasks, per status task counts, merged recent logs, and health objects shaped as `{ value, status: 'good' | 'warn' | 'bad' }`.

The parent computes once. Widgets render. No widget does its own math. No widget fetches anything.

That is what makes widgets reorderable, hideable, and deletable without fear. A widget that only renders is a widget you can move.

Fetching in the parent is a fan out of independent promises. Each has its own `.catch(() => {})` and its own `.finally()` that clears only its own loading flag. One dead endpoint degrades one card instead of blanking the dashboard.

---

## Realtime and data patterns

This is the most transferable part of the production build.

```
  a route handler mutates the database
                 |
                 v
      eventBus.broadcast(type, data)
                 |
        +--------+--------+
        |                 |
        v                 v
  GET /api/events    webhook sender
  (SSE stream)       (HMAC signed, retried with backoff)
        |
        v
  EventSource in the browser
        |
        v
  one Zustand store
        |
        v
  every panel that cares re-renders
```

### The server event bus

A module scoped `EventEmitter` singleton with one method, `broadcast(type, data)`, returning a `{ type, data, timestamp }` envelope.

Stash the instance on `globalThis`. That is six lines and it is the detail most implementations miss. Without it, hot module reload in development quietly creates a second emitter and half your subscribers stop receiving events.

Event types are a closed TypeScript union, namespaced by entity. Twenty seven of them in the production build: `task.created`, `task.updated`, `task.status_changed`, `agent.created`, `agent.status_changed`, `run.created`, `run.completed`, `chat.message`, `notification.created`, `security.event`, and so on.

**Every database mutation broadcasts.** That single rule is what makes everything downstream work. The UI and the outbound webhooks read from one source of truth instead of two.

### The SSE route

`GET /api/events` is a `ReadableStream` over `text/event-stream`, with `runtime = 'nodejs'` and `dynamic = 'force-dynamic'`.

- Auth is checked before the stream opens, with a role requirement.
- An immediate `connected` ack tells the client the pipe is live.
- Events carrying a workspace ID that does not match the viewer get dropped.
- A heartbeat comment frame every 30 seconds survives proxy idle timeouts.
- Cleanup is registered in `start()` and called from `cancel()`, plus an `abort` listener on the request signal. `cancel()` does not always fire on a network drop.
- `X-Accel-Buffering: no` stops nginx from buffering the stream. `Cache-Control: no-cache, no-transform` stops everything else.

> [!WARNING]
> Those last three bullets are where most SSE implementations quietly break in production. It works on localhost, then a reverse proxy buffers the stream and the dashboard goes silent with no error anywhere.

### The client hook

`useServerEvents()` opens an `EventSource` and dispatches each message through a switch into Zustand actions.

Reconnect is exponential backoff with jitter. The base doubles per attempt, caps at 30 seconds, adds up to 50 percent random jitter, and gives up after 20 attempts with a logged error. Connection state gets written back into the store so the rest of the UI can react to it.

### Polling is the fallback, not the default

`useSmartPoll(callback, intervalMs, options)` is a visibility aware polling hook. It pauses when the tab is hidden and fires immediately on return. The options are the interesting part:

- `pauseWhenSseConnected` turns polling off entirely while the realtime stream is healthy
- `pauseWhenConnected` and `pauseWhenDisconnected` do the same against a WebSocket
- `backoff` widens the interval up to a multiplier when the callback reports no new data
- An initial fetch always fires on mount regardless of the pause options, so components bootstrap even when realtime is already up

Realtime is primary. Polling is the safety net. The safety net knows when to stay out of the way.

### Other server side patterns worth naming

- **Webhooks** HMAC signed delivery with exponential backoff and jitter, subscribed to the same event bus.
- **Scheduler** one background job runner covering backups, agent sync, webhook retry, session pruning, task dispatch, and recurring spawns. Every job gated behind a settings flag.
- **Token pricing** a per model cost table across roughly 40 models and several providers, with an override for flat rate subscription plans. Cost display stays honest for both metered API use and a fixed monthly plan.
- **Plugin registry** module scoped registries for integrations, categories, nav items, panels, tool providers, migrations, and an auth resolver. Plugins register by importing and calling `init()`. Pure TypeScript, zero dependencies. The panel registry is what lets the route allowlist accept slugs it did not know at build time.
- **Framework adapters** one interface with five methods (register, heartbeat, reportTask, getAssignments, disconnect) and per framework implementations for CrewAI, LangGraph, AutoGen, the Claude Agent SDK, and a generic fallback. All of them broadcast lifecycle events onto the same bus. A shared conformance test runs every adapter against the interface, and that test is what makes the abstraction real.
- **Runs as a first class resource** a versioned run API with filtering by agent, status, task, and time. Writes require an agent ID, a status, and a start time. Cost, provenance, and steps default rather than erroring. Every response carries a protocol version header.

### Expose the same capability three ways

The dashboard was one client of its own API, not the only one. A zero dependency CLI and an MCP server shipped alongside it, both wrapping the same REST endpoints the browser used.

That means nothing in the system was reachable only by clicking. If you are building software that agents operate, this is the pattern that matters most. The agent gets the same surface as the human.

---

## Principles that show up in both builds

- **Own your components.** shadcn's premise is that the code lands in your repo. Use it as intended. Edit primitives down, retokenize them, extend them. Do not wrap them and do not accumulate them.
- **Every mutation is an event.** Realtime is not bolted on later. Broadcasting from the write path is what lets the UI, the webhooks, and any future consumer share one truth.
- **Derive once, render many.** Pre compute in the container. Hand widgets a finished object.
- **Fetch independently, fail independently.** Parallel fetches, per source loading flags, swallowed errors. One dead endpoint degrades one card.
- **Name the data before the design.** Both builds start from tables, not from a layout.
- **State the limits.** Free tier edges, seed data versus real telemetry, what this is not. The credibility of your real claims depends on the disclaimed ones.
- **Disposable builds stay disposable.** A recording prop and a durable system are separate repos with separate lifecycles. Write that down as a decision so they never merge by accident.

---

Built by OperatorOS | [operatoros.ai](https://operatoros.ai)

Follow [@daviss.dev](https://instagram.com/daviss.dev) and [@os.operator](https://instagram.com/os.operator) on Instagram.
