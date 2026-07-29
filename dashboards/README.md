# Dashboards

Dashboard builds from the content. Mission controls for AI agents, ops views, panels that show what a system is actually doing.

Most dashboard tutorials are a design exercise. This section is not. The lesson here is one sentence:

> A dashboard is a database with persistent memory, displayed properly.

The front end is the window. The database is the thing. If you get that backwards you end up with a page that looks like a command center and does nothing, where refreshing changes nothing, because there is nothing behind it.

## Index

- **[mission-control.md](mission-control.md)** The agent mission control build. What it shows, the three tables behind it, and the full path from a free shadcn block to a live URL that agents write into on their own.
- **[patterns.md](patterns.md)** The stack and the patterns. Next.js, shadcn, the data layer, layout, realtime, and the reasoning behind each choice. Pulled from a production agent dashboard that ran more than 160 API routes and 36 panels.

## Which one you want

Start with `mission-control.md` if you have never shipped a dashboard. It is the honest minimum that still counts as real. Five panels, three tables, free tiers, one afternoon.

Read `patterns.md` when the small version works and you want to know what the grown up version looks like. Widget catalogs, a server event bus, SSE with a polling fallback, and the layout rules that keep a 36 panel app from turning into mud.

> [!NOTE]
> The two builds share a framework spine on purpose. Same Next.js, same React, same Tailwind, same shadcn. The data layer is where they diverge, and the reasoning for that split is in both files.

## What you need

- Node 20 or newer
- A free GitHub account
- A free Supabase account
- A free Vercel account
- An AI coding environment if you want one, though nothing here requires it

Total cost to build and ship the tutorial version is zero, plus roughly $12 a year if you want a custom domain.

---

Built by OperatorOS | [operatoros.ai](https://operatoros.ai)

Follow [@daviss.dev](https://instagram.com/daviss.dev) and [@os.operator](https://instagram.com/os.operator) on Instagram.
