---
name: stack-map
description: >
  Map a repo against the ten-layer build stack (design, code, framework, database, automation,
  source control, deploy, decisions, memory, integrations). Reports which layers are present, which
  are missing, and the next command for each gap. Use when the user says "stack map", "map the stack",
  "what's missing in this stack", "audit the stack", "which layers do we have", or when starting
  work in an unfamiliar repo and the stack is unclear.
argument-hint: "[path]"
allowed-tools: Read, Glob, Grep, Bash(ls:*), Bash(cat:*), Bash(git:*)
---

# Stack Map

Read a repo and report it against the ten layers a build goes through, in the order they happen.
Facts only. If a layer cannot be detected from files on disk, say "not detected" and give the
command that would add it. Never guess that a layer exists because the project "probably" has it.

## Arguments

- **path** (optional): the repo to map. Defaults to the current working directory.

## Phase 1: Read the repo

Read these if they exist. Do not read source files beyond them unless a layer is ambiguous.

- `package.json` (dependencies, devDependencies, scripts, packageManager)
- `pnpm-lock.yaml`, `package-lock.json`, or `yarn.lock` (which package manager)
- `next.config.*`, `tsconfig.json`, `tailwind.config.*`, `components.json` (shadcn)
- `supabase/` folder, `supabase/config.toml`, any `*.sql` migrations
- `wrangler.jsonc`, `wrangler.toml`, `open-next.config.ts`, `Dockerfile`, `docker-compose*.yml`, `vercel.json`
- `.github/workflows/*.yml`
- `.env.example` (variable names only, never values)
- `CLAUDE.md`, `.claude/` (skills, agents, settings), `.mcp.json`
- `README.md` and `docs/` for mentions of n8n, Obsidian, Mem0, Composio, TypeSafe, MCP
- `git remote -v` for the hosting provider

## Phase 2: Detect each layer

Use the signals below. Mark each layer **present**, **partial**, or **not detected**, and name the file that proves it.

1. **Design.** Any of: `design/` folder, Figma or Framer links in the README, exported mockups in `docs/`. Usually not detected from code alone. Say so.
2. **Code.** `CLAUDE.md` or `.claude/` means Claude Code is set up. `AGENTS.md` or `.codex/` means Codex. Neither means the agent layer is not configured for this repo.
3. **Framework.** `next` in dependencies, plus `next.config.*`. Note the version. `components.json` means shadcn/ui. `tailwindcss` in dependencies.
4. **Database.** `@supabase/supabase-js` or `@supabase/ssr` in dependencies, `supabase/` folder, `SUPABASE_` variables in `.env.example`. `@neondatabase/serverless` or `DATABASE_URL` pointing at Neon means Neon. `pg`, `drizzle-orm`, or `prisma` means plain Postgres through an ORM.
5. **Automation.** `n8n` mentioned in README or docs, webhook routes under `app/api/` that reference n8n, `N8N_` variables. Rarely in the app repo. If not detected, say automation is probably external and ask where it lives.
6. **Source control.** `.git/` present, remote on github.com, `.github/workflows/` with at least one workflow. Note whether CI deploys or only validates.
7. **Deploy.** `wrangler.jsonc` plus `@opennextjs/cloudflare` means Cloudflare Workers. `Dockerfile` plus a deploy script means a VPS. `vercel.json` or `.vercel/` means Vercel. Nothing means not detected.
8. **Decisions.** `@typesafe-ai/sdk` or `typesafe-sdk` in dependencies, `TYPESAFE_API_KEY` in `.env.example`.
9. **Memory.** `mem0ai` in dependencies or `MEM0_API_KEY`. An Obsidian vault is outside the repo. Check the README for a vault path. If nothing, not detected.
10. **Integrations.** `.mcp.json` or MCP servers in `.claude/settings.json` means MCP. `composio-core`, `@composio/core`, or `COMPOSIO_API_KEY` means Composio.

## Phase 3: Report

Print exactly this shape. Keep each line short. No tables.

```
Stack map: <repo name> (<path>)

01 Design         not detected      no design files in the repo
02 Code           present           CLAUDE.md, .claude/skills (4)
03 Framework      present           next 16.3.8, tailwindcss 4.2.2, shadcn (components.json)
04 Database       present           @supabase/ssr 0.12.4, supabase/migrations (3)
05 Automation     not detected      ask where the n8n workflows live
06 Source control present           github.com/<org>/<repo>, CI validates only (.github/workflows/ci.yml)
07 Deploy         present           Cloudflare Workers via @opennextjs/cloudflare 1.20.8
08 Decisions      not detected      pnpm add @typesafe-ai/sdk
09 Memory         not detected      pnpm add mem0ai, or point the README at the vault
10 Integrations   partial           .mcp.json (2 servers), no Composio

Present 5, partial 1, not detected 4.

Next commands, in build order:
- 05: document the n8n workflows in docs/automations.md, or create the account in the client's name
- 08: pnpm add @typesafe-ai/sdk && echo "TYPESAFE_API_KEY=" >> .env.example
- 09: pnpm add mem0ai && echo "MEM0_API_KEY=" >> .env.example
```

## Quality rules

- Every "present" line names the file or dependency that proves it, with the version when one exists.
- "Not detected" is a finding, not a failure. Not every project needs every layer. Say which layers a project of this type usually skips.
- Never print a value from any env file. Variable names only.
- Never recommend a tool the stack does not name. The ten layers and their picks are fixed. The user swaps tools, not the skill.
- No emojis. No markdown tables. No invented versions.
