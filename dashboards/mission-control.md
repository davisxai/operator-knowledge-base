# Build a Mission Control for Your Agents

A dashboard that shows what your AI agents are running, what it cost, and what is scheduled next. The agents write their own rows into it. Nobody updates it by hand.

Free tiers the whole way. Three tables. Five panels. One afternoon.

## Contents

- [The problem with the demos](#the-problem-with-the-demos)
- [What it shows](#what-it-shows)
- [The three tables](#the-three-tables)
- [Stage 0: name the data](#stage-0-name-the-data)
- [Stage 1: scaffold the fake version](#stage-1-scaffold-the-fake-version)
- [Stage 2: understand the split](#stage-2-understand-the-split)
- [Stage 3: give it memory](#stage-3-give-it-memory)
- [Stage 4: make it act, then make it self feeding](#stage-4-make-it-act-then-make-it-self-feeding)
- [Stage 5: ship it](#stage-5-ship-it)
- [Stage 6: harden it](#stage-6-harden-it)
- [The bill](#the-bill)
- [Honest limits](#honest-limits)
- [Where to go next](#where-to-go-next)

---

## The problem with the demos

You have seen the videos. A dark screen, a glowing sidebar, four cards with numbers, a chart that curves upward. Somebody calls it their AI command center.

Refresh it. Nothing changes. Close it and reopen it. Same numbers.

It is a hardcoded page on localhost. There is no database. There is nothing behind it, so there is nothing to remember. It looks like a command center because a command center is easy to draw.

The diagnosis is simple. People treat a dashboard as a design problem when it is a database problem.

> A dashboard is a database with persistent memory, displayed properly.

The front end is the window. The database is the actual thing. That is why this guide spends most of its length on three tables and about two minutes on the layout.

I am not going to debunk anybody. I am going to build the real version of the exact thing people fake.

---

## What it shows

Five panels. Every one of them reads from the database.

- **Now running.** In progress runs with elapsed time.
- **Run history.** Recent runs, status, tokens, cost, one line summary.
- **Schedules and loops.** Scheduled jobs, next run time, interval, on and off toggle.
- **Spend.** KPI cards for tokens and dollars, today and all time, derived from the runs table.
- **Quick actions.** Trigger a run, stop a run, retry a failed one.

That is a mission control. Not a generic analytics page. Something specific enough that the numbers on it mean something to you.

---

## The three tables

- **`agents`** Who runs. Name, kind, description.
- **`runs`** What happened. Agent reference, status, started at, finished at, tokens, cost, summary.
- **`schedules`** What is next. Agent reference, cadence, next run at, enabled.

Three tables. That is the entire data model, and it is enough to make all five panels real.

Here is the whole system:

```
   an agent finishes a job
             |
             v
   +--------------------+
   |  Stop hook fires   |   runs a small script
   +--------------------+
             |
             |  INSERT INTO runs
             v
   +--------------------+
   |  Supabase Postgres |   agents / runs / schedules
   +--------------------+
             ^
             |  SELECT, on the server
             v
   +--------------------+
   |  Next.js app       |   Server Components read
   |                    |   Server Actions write
   +--------------------+
             |
             v
        your browser
```

No API routes. No client side data fetching. No websockets. Not yet.

---

## Stage 0: name the data

No editor. Write down two lists.

1. The panels you want on screen.
2. The tables that would have to exist for those panels to be true.

If a panel has no table behind it, it is decoration. Cut it or add the table.

This is the step everyone skips, and skipping it is why the fake dashboards exist. They started from a layout.

---

## Stage 1: scaffold the fake version

Yes, on purpose. Build the fake one first so you can watch it become real.

```bash
npx create-next-app@latest mission-control --typescript --tailwind
cd mission-control
npx shadcn@latest init
npx shadcn@latest add dashboard-01
npm run dev
```

Open `localhost:3000`. Sidebar, KPI cards, a chart, a data table. Roughly two minutes.

Every number on that screen is hardcoded. This is the fake version. It is also your baseline, and the rest of this guide is replacing it piece by piece.

> [!NOTE]
> I use the raw `dashboard-01` block instead of a full dashboard starter template because the starter hides the data layer. The data layer is the whole lesson.

---

## Stage 2: understand the split

This is the one concept you have to actually learn. It is also the reason a dashboard is not a marketing site.

- **Server Components** run on the server. They can read the database directly. Their code never reaches the browser. In the App Router they are the default.
- **Client Components** run in the browser and handle interaction. You opt in with `"use client"` at the top of the file.
- **Server Actions** are server functions you can call straight from a button or a form. No API route in between.

For a self contained dashboard, that combination means you need zero API routes. Server Components fetch. Server Actions mutate. `revalidatePath` refreshes the page.

---

## Stage 3: give it memory

Create a Supabase project. Then define the three tables with Drizzle.

```ts
// src/lib/schema.ts
export const runStatus = pgEnum("run_status", ["queued", "running", "done", "failed"]);

export const agents = pgTable("agents", {
  id: uuid("id").primaryKey().defaultRandom(),
  name: text("name").notNull(),
  kind: text("kind"),
  description: text("description"),
  createdAt: timestamp("created_at").defaultNow(),
});

export const runs = pgTable("runs", {
  id: uuid("id").primaryKey().defaultRandom(),
  agentId: uuid("agent_id").references(() => agents.id),
  status: runStatus("status").notNull().default("queued"),
  startedAt: timestamp("started_at").defaultNow(),
  finishedAt: timestamp("finished_at"),
  tokens: integer("tokens").default(0),
  costUsd: numeric("cost_usd").default("0"),
  summary: text("summary"),
});

export const schedules = pgTable("schedules", {
  id: uuid("id").primaryKey().defaultRandom(),
  agentId: uuid("agent_id").references(() => agents.id),
  cadence: text("cadence"),
  nextRunAt: timestamp("next_run_at"),
  enabled: boolean("enabled").default(true),
});
```

### The two connection strings

Supabase gives you two. Picking the wrong one is the single most common first dashboard failure.

```bash
# .env.local  (never commit this)
DATABASE_URL=postgresql://...pooler...:6543/postgres   # app queries, pooled
DIRECT_URL=postgresql://...:5432/postgres              # migrations only, direct
# no NEXT_PUBLIC_ on either. these are secrets.
```

```ts
// src/lib/db.ts
import { drizzle } from "drizzle-orm/postgres-js";
import postgres from "postgres";

// The transaction pooler does not support prepared statements.
const client = postgres(process.env.DATABASE_URL!, { prepare: false });
export const db = drizzle(client);
```

> [!WARNING]
> If you skip `{ prepare: false }` the app will work locally and fail in production against the pooler. The error message will not tell you why.

### Read it from a Server Component

Push the schema, seed a few rows, then render.

```tsx
// src/app/dashboard/page.tsx
import { desc } from "drizzle-orm";
import { db } from "@/lib/db";
import { runs } from "@/lib/schema";

export const dynamic = "force-dynamic"; // do not prerender a data page at build time

export default async function Dashboard() {
  const recent = await db.select().from(runs).orderBy(desc(runs.startedAt));
  return <RunHistory runs={recent} />;
}
```

That is the moment it stops being fake. The numbers now come from somewhere. Change a row, refresh, the screen changes.

---

## Stage 4: make it act, then make it self feeding

### Writing from the UI

```ts
// src/app/actions.ts
"use server";
import { eq } from "drizzle-orm";
import { revalidatePath } from "next/cache";
import { db } from "@/lib/db";
import { runs } from "@/lib/schema";

export async function retryRun(id: string) {
  // Check auth here, every time. Server Actions are reachable by direct request.
  await db.update(runs).set({ status: "queued" }).where(eq(runs.id, id));
  revalidatePath("/dashboard");
}
```

Wire that to a button. Quick actions panel done.

### Writing from an agent

This is the whole point of the build.

```ts
// scripts/log-run.ts  (an agent runs this when a job ends)
await db.insert(runs).values({ agentId, status: "done", tokens, costUsd, summary });
```

Wire that script to a Claude Code Stop hook. The hook fires when an agent finishes a job. The script inserts the row. You never touch it.

One real row, generated by an agent, with nobody typing. That single row is the entire difference between this and the demos.

> [!TIP]
> Keep the scope here small on purpose. Seeded data for the panels plus one genuine write back beats five half wired integrations. Reading session logs, cron control, MCP tooling: all of that can wait until the basic loop works.

---

## Stage 5: ship it

Local, server, and production are the same ladder. The code is identical at every rung. Only five things change: which database it points at, which secrets it uses, who can reach it, the domain, and whether HTTPS is on.

**Local.** `npm run dev`, dev database, secrets in `.env.local`. Only you can see it.

**Your own server.** `next build` then `next start` on a rented box. Keep it alive with pm2 or systemd. Put nginx or Caddy in front for HTTPS. You own the upkeep.

**Production, the easy path.** Push to GitHub, connect Vercel. You get a preview URL per branch, merges to main go live, and the domain and HTTPS are handled. Environment variables are set per environment.

Take the Vercel path first. Move to your own box later if you have a reason.

---

## Stage 6: harden it

Short list. Do all of it.

- Separate your dev and prod databases. Do not point local development at production data.
- Never commit `.env`. `create-next-app` gitignores it already. Commit `.env.example` with the keys and no values.
- `NEXT_PUBLIC_` is the exposure switch. It inlines the value into the browser bundle at build time. Secrets never get that prefix.
- Use generated migrations against production, not `db:push`. Push is a local prototyping tool. It alters tables with no history and no way back.
- Check auth inside every Server Action, not only in the layout. Actions are reachable by direct request.
- Run `npm run build` locally before you deploy. Turn on error monitoring.

---

## The bill

- Next.js, React, Tailwind, shadcn/ui, Drizzle: open source, $0
- Supabase: $0 on the free tier. 500 MB database, 5 GB egress, two projects. Free projects pause after 7 days idle. $25 a month for Pro when you outgrow it.
- Vercel: $0 on Hobby, which is personal use only. $20 a month for Pro if it is commercial.
- Domain: roughly $12 a year, optional.

Total to build and ship: $0, plus a domain if you want one.

---

## Honest limits

What this is not:

- **Seed data is not real telemetry.** Until every panel is fed by a write back, most of what you see is data you inserted yourself. Be honest with yourself about which panels are live.
- **This is a starting point, not an observability platform.** No tracing, no alerting, no retention policy, no eval scoring. Those are real disciplines and this is not them.
- **Supabase free projects pause after 7 days idle.** If you build this and walk away, it will be asleep when you come back.
- **Vercel Hobby is personal use only.** If this becomes a client facing tool you are on a paid plan.
- **The transaction pooler has real tradeoffs.** No prepared statements is the one that bites first. There are others.

Naming what it is not is what makes the claim about what it is worth anything.

---

## Where to go next

Everything below is the growth path from the three table version. Each step is a pattern from a production agent dashboard, written up in [patterns.md](patterns.md).

1. Add an event bus singleton pinned to `globalThis` and broadcast on every mutation.
2. Add an SSE route reading from that bus, with a heartbeat, per tenant filtering, and abort cleanup.
3. Add a client `EventSource` hook with backoff and jitter reconnect, dispatching into one store.
4. Convert polling to visibility aware polling that pauses while SSE is healthy.
5. Split the overview into a widget catalog plus a persisted layout array.
6. Route panels through one catch all route with a server side slug allowlist, so unknown URLs return a real 404.

Do them in that order. Each one only makes sense once the one before it is working.

---

Built by OperatorOS | [operatoros.ai](https://operatoros.ai)

Follow [@daviss.dev](https://instagram.com/daviss.dev) and [@os.operator](https://instagram.com/os.operator) on Instagram.
