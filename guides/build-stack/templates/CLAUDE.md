# CLAUDE.md

Project instructions for Claude Code. Edit the stack block to match this app, keep the rules.

## Stack

- **Framework:** Next.js (App Router), TypeScript, Tailwind. Components from shadcn/ui, icons from lucide-react.
- **Database:** Supabase (Postgres, auth, storage). Client in `src/lib/supabase/`. Types generated with `supabase gen types`.
- **Automation:** n8n, in the client's own account. Webhooks documented in `docs/automations.md`.
- **Source control:** GitHub. CI lints and typechecks only. Deploys happen from the box or from Workers Builds, never from CI.
- **Deploy:** Cloudflare Workers through the OpenNext adapter, built by Workers Builds from `main`.
- **Decisions:** Jev for routing, scoring, and risk gates. Calls live in `src/lib/decisions/`.
- **Memory:** per-user memory through Mem0 if the product needs it. Team knowledge lives in the Obsidian vault, not in this repo.
- **Integrations:** MCP servers for my own accounts, Composio for end users' accounts.

## Commands

```bash
pnpm dev          # local server, the human runs this in a split terminal
pnpm lint
pnpm typecheck
pnpm build
```

## Rules

- Never run `pnpm dev`. The human runs it.
- Never commit `.env`, `.env.local`, or any credential. `.env.example` is the only env file in git.
- Prefer shadcn/ui and radix over hand-rolled components.
- Read the official docs before using an unfamiliar API. Do not guess at signatures.
- Keep changes minimal. Touch only what was asked. No speculative abstractions.
- After finishing a task, run lint and typecheck before reporting done.
- Client-owned accounts. Every third-party account is created in the client's name. We get admin access to build and hand ownership back at the end.
