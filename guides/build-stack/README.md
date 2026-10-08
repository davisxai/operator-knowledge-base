# The Build Stack

> Follow [@daviss.dev](https://instagram.com/daviss.dev) and [@os.operator](https://instagram.com/os.operator) on Instagram for more guides like this.

---

### From an idea to a live app, in the order a build happens.

Ten layers, one tool each, and where two tools fit, the line for which one and when. This is the stack my company ships on, with the setup commands, the docs that matter, and the config files pulled from my own repos. It is not a review and it is not a ranking.

Every command here was run on October 8, 2026. Every price and limit links to the vendor's own page.

---

## What you'll get

→ Ten sections, one per layer, each with the pick, the alternative, the split between them, the exact setup, and the docs that matter
→ One script that scaffolds the first four layers into a fresh repo, tested on Next.js 16.4
→ A doctor script that checks your machine for every tool on the list and prints the install step for anything missing
→ A Claude Code skill, `/stack-map`, that reads any repo and reports which layers are present and which are not
→ The config files from my production deploy: `wrangler.jsonc`, `open-next.config.ts`, the CI workflow, the project `CLAUDE.md`, the env template
→ What each layer costs at the free tier and at the first paid tier, from the vendors' own pricing pages

---

## Prerequisites

- A Mac or Linux shell. Windows works through WSL.
- Node.js 22 and pnpm. `npm install -g pnpm` if you do not have it.
- Git and a GitHub account.
- A Claude plan at Pro or above for Claude Design and Claude Code. The free plan does not include either.
- Docker, only if you plan to self-host Supabase or n8n.

Run the doctor first. It tells you what is already on the machine.

```bash
git clone https://github.com/davisxai/operator-knowledge-base.git
bash operator-knowledge-base/guides/build-stack/scripts/stack-doctor.sh
```

---

## Contents

1. [The ten layers](#1-the-ten-layers)
2. [Scaffold the first four in one command](#2-scaffold-the-first-four-in-one-command)
3. [01 Design: Claude Design // Framer](#3-01-design-claude-design--framer)
4. [02 Code: Claude Code // Codex](#4-02-code-claude-code--codex)
5. [03 Framework: Next.js](#5-03-framework-nextjs)
6. [04 Database: Supabase // Neon](#6-04-database-supabase--neon)
7. [05 Automation: n8n](#7-05-automation-n8n)
8. [06 Source control: GitHub](#8-06-source-control-github)
9. [07 Deploy: Cloudflare](#9-07-deploy-cloudflare)
10. [08 Decisions: Jev](#10-08-decisions-jev)
11. [09 Memory: Obsidian // Mem0](#11-09-memory-obsidian--mem0)
12. [10 Integrations: MCP // Composio](#12-10-integrations-mcp--composio)
13. [What the stack costs](#13-what-the-stack-costs)
14. [Troubleshooting](#14-troubleshooting)
15. [Quick reference](#15-quick-reference)
16. [Sources](#16-sources)

---

## 1. The ten layers

A build has ten jobs. Each one gets a tool. Seven of them make the app. Three of them make the agent inside the app.

```
  THE APP
  01 DESIGN         Claude Design // Framer    the layout, the deck, the site
        |
  02 CODE           Claude Code // Codex       the agent that writes and runs the code with you
        |
  03 FRAMEWORK      Next.js                    pages, logins, server code, one project
        |
  04 DATABASE       Supabase // Neon           data, auth, files
        |
  05 AUTOMATION     n8n                        everything on a trigger or a schedule
        |
  06 SOURCE         GitHub                     every change, reviewed, undoable
        |
  07 DEPLOY         Cloudflare                 where it goes live

  THE AGENT
  08 DECISIONS      Jev                        typed decisions, no generated text
  09 MEMORY         Obsidian // Mem0           what the agent keeps
  10 INTEGRATIONS   MCP // Composio            how the agent touches other apps
```

Where a layer lists two tools, the first is my pick and the second is the one to reach for when the job changes shape. The split is stated in each section. Not every project needs every layer. A marketing site needs 01, 03, 06, 07. A product with an agent in it needs all ten.

> [!NOTE]
> The tools I run in production today: Claude Design, Claude Code, Next.js, Supabase, n8n, GitHub, Cloudflare, Jev, Obsidian, and MCP. Framer, Codex, Neon, Mem0, and Composio are the alternatives. I document them from their own docs and say so in each section.

---

## 2. Scaffold the first four in one command

Layers 02, 03, 04, and 06 come out of one script. It creates a Next.js app with TypeScript and Tailwind, adds the Supabase client, runs the shadcn/ui init, drops in a validate-only CI workflow, a project `CLAUDE.md` for Claude Code, and a `.env.example`, then makes the first commit.

```bash
bash operator-knowledge-base/guides/build-stack/scripts/new-stack.sh my-app
cd my-app
cp .env.example .env.local
```

What it ran, in order:

1. `pnpm dlx create-next-app@latest` with the App Router, `src/` directory, and the `@/*` import alias
2. `pnpm add @supabase/supabase-js @supabase/ssr`
3. `pnpm dlx shadcn@latest init --defaults`
4. Copied [templates/ci.yml](templates/ci.yml) into `.github/workflows/` and added a `typecheck` script
5. Copied [templates/CLAUDE.md](templates/CLAUDE.md) and [templates/env.example](templates/env.example)
6. `git commit`

Tested on October 8, 2026. The result was Next.js 16.4.0, Tailwind 4, and a green `pnpm lint` and `pnpm typecheck`.

To see where any existing repo stands against the ten layers, install the skill and run it inside the repo:

```bash
mkdir -p ~/.claude/skills/stack-map
curl -o ~/.claude/skills/stack-map/SKILL.md https://raw.githubusercontent.com/davisxai/operator-knowledge-base/main/skills/stack-map/SKILL.md
claude
```

Then type `/stack-map`. It reads config files and lockfiles only, never source, and prints one line per layer with the file that proves it. Details in [skills/stack-map](../../skills/stack-map/).

---

## 3. 01 Design: Claude Design // Framer

**The job.** The layout before the code. Slide systems, mockups, carousels, one-pagers, interactive prototypes.

**My pick: Claude Design.** The last three carousels on @daviss.dev were built in it, including the one that sent you here. Prompt in, design out. The hand-off to Claude Code is direct because both live in the same Claude account, and a mockup made in Design can be implemented by Code in the same project.

**Reach for Framer when the thing is a marketing site.** The canvas is also the host. CMS, localization, A/B testing, and a custom domain on the Basic plan. The site ships from where you design it.

**Get started with Claude Design**

1. You need Claude Pro, Max, Team, or Enterprise. Claude Design is in beta and on by default on Pro, Max, and Team. [Pricing](https://claude.com/pricing).
2. Open [claude.ai/design](https://claude.ai/design), or pick a design template from the Artifacts tab in any conversation, or ask for one inside Claude Code.
3. Bring a design system in once, from code or a design file, and every prompt after that inherits it.

**Get started with Framer**

1. Sign up at [framer.com](https://www.framer.com/). The free plan publishes to a Framer subdomain with no card.
2. Basic is $10 a month billed annually and adds a custom domain. Pro is $30 a month billed annually and adds staging and branching. [Pricing](https://www.framer.com/pricing/), read October 8, 2026.
3. Start from [Build your first site](https://www.framer.com/academy/lessons/build-your-first-site) in Framer Academy.

**Best uses, in the vendors' own words**

- Claude Design: shareable interactive prototypes for feedback and user testing, product mockups handed to Claude Code for implementation, branded assets and social graphics, one-pagers and proposals, slide decks
- Framer: marketing and landing sites, CMS-driven content like blogs and FAQs, localized sites, sites a non-developer will edit after launch

**Docs**

- Claude Design: [get started](https://support.claude.com/en/articles/14604416-get-started-with-claude-design), [prototypes and UX tutorial](https://academy.claude.com/tutorials/using-claude-design-for-prototypes-and-ux), [presentations and slide decks tutorial](https://academy.claude.com/tutorials/using-claude-design-for-presentations-and-slide-decks), [product page](https://claude.com/product/design), [announcement](https://www.anthropic.com/news/claude-design-anthropic-labs)
- Framer: [help center](https://www.framer.com/help/), [academy](https://www.framer.com/academy/lessons/build-your-first-site), [pricing](https://www.framer.com/pricing/), [updates](https://www.framer.com/updates), [plugin developer docs](https://www.framer.com/developers/)

> [!TIP]
> **Design the system before the deck.** Two colors, one accent, one display face, one body face, one type scale. Give Claude Design that as the first prompt and reuse it on every piece. The twelve slides behind this guide share one system, which is why they read as one post.

---

## 4. 02 Code: Claude Code // Codex

**The job.** The agent that writes and runs the code with you, in your repo, with your tools.

**My pick: Claude Code.** My whole company runs through it. On October 8, 2026 my global Claude Code directory holds 50 skill folders and 11 agents, the agency repo adds 16 project skills, 9 hook rules block or warn on dangerous commands, and MCP servers connect it to three Gmail accounts, Slack, Cloudflare, and shadcn. Every guide in this repo was written and tested from a Claude Code session.

**Reach for Codex when the work is a pile of separate tasks you want done at once.** Each task runs in its own cloud sandbox against the GitHub repo and comes back as a pull request to review. Claude Code builds with you in your environment. Codex takes delegated tasks away and brings back PRs. I document Codex from OpenAI's own pages. It is not in my daily stack.

**Get started with Claude Code**

```bash
curl -fsSL https://claude.ai/install.sh | bash
claude --version
cd my-app
claude
```

Homebrew works too: `brew install --cask claude-code`. Log in with your Claude account on first run. Then add the three files that pay back most:

1. A project `CLAUDE.md`. Stack, commands, rules, under a page. Template at [templates/CLAUDE.md](templates/CLAUDE.md).
2. One skill. A `SKILL.md` in `.claude/skills/<name>/` for the job you repeat. The playbook is in [claude-code-skills-starter-kit](../claude-code-skills-starter-kit/).
3. One MCP server. Section 12 has the commands.

**Get started with Codex**

```bash
npm install -g @openai/codex
codex
```

Codex is included with ChatGPT Plus at $20 a month and above. It runs as a CLI, an IDE extension, a desktop and web app, and a cloud agent. [Docs](https://developers.openai.com/codex), [releases](https://github.com/openai/codex/releases).

**Best uses, in Anthropic's own words**

- Writing tests for untested code, fixing lint errors project-wide, resolving merge conflicts, updating dependencies
- Building features and fixing bugs from plain-language descriptions across many files
- Creating commits and pull requests through git, including in CI
- Connecting external tools over MCP
- Running several agents in parallel on different parts of one task

**Docs**

- Claude Code: [overview](https://code.claude.com/docs/en/overview), [quickstart](https://code.claude.com/docs/en/quickstart), [MCP](https://code.claude.com/docs/en/mcp), [changelog](https://code.claude.com/docs/en/changelog), [pricing](https://claude.com/pricing)
- Codex: [docs](https://developers.openai.com/codex), [quickstart](https://developers.openai.com/codex/quickstart), [pricing](https://developers.openai.com/codex/pricing), [GitHub](https://github.com/openai/codex)

> [!TIP]
> **The project CLAUDE.md is the highest-return file in the repo.** Stack, commands, and rules, nothing else. Every session reads it first. Mine says "never run pnpm dev" because I run it myself in a split terminal, and that one line has saved more interruptions than any other.

---

## 5. 03 Framework: Next.js

**The job.** The app. Pages, logins, API routes, and the server code that talks to the database, in one project.

**My pick: Next.js, App Router, TypeScript, Tailwind, shadcn/ui.** [operatoros.ai](https://operatoros.ai) runs on Next.js 16. So does my internal studio dashboard and the [open source operator dashboard](https://github.com/davisxai/operatoros), which you can clone and run on seeded demo data with no credentials. Single tool, no split.

**Get started**

```bash
pnpm create next-app@latest my-app --yes
cd my-app
pnpm dlx shadcn@latest init --defaults
```

The `--yes` flag takes the defaults: TypeScript, Tailwind, ESLint, App Router, Turbopack, the `@/*` alias, and an `AGENTS.md` for coding agents. Node.js 20.9 or newer. The current release is 16.4.0. Or run the scaffold in section 2, which does this plus the database client, CI, and `CLAUDE.md`.

**Best uses, in the Next.js docs' own framing**

- Full-stack React apps that render on the server and the client in one framework
- Server Components and Server Actions for data without a separate API layer
- File-system routing with `layout.tsx`, `page.tsx`, and `route.ts` conventions
- Cache Components for fast first loads on personalized pages
- Projects where a coding agent does part of the work, through the bundled `AGENTS.md` and the Next.js devtools MCP

**Docs**

- [Docs home](https://nextjs.org/docs), [installation](https://nextjs.org/docs/app/getting-started/installation), [16.4 release post](https://nextjs.org/blog/next-16-4)
- [shadcn/ui for Next.js](https://ui.shadcn.com/docs/installation/next), [Tailwind for Next.js](https://tailwindcss.com/docs/installation/framework-guides/nextjs)

> [!TIP]
> **Next.js 16 stopped running the linter inside `next build`.** Lint is its own script now. The CI workflow in [templates/ci.yml](templates/ci.yml) runs `lint` and `typecheck` as two parallel jobs on every push and pull request, so nothing lands unlinted.

---

## 6. 04 Database: Supabase // Neon

**The job.** Data, auth, and files.

**My pick: Supabase.** Postgres, auth, file storage, realtime, and edge functions behind one dashboard. I self-host it on my own server through Coolify. Fourteen containers: db, auth, rest, kong, storage, studio, meta, supavisor, analytics, edge-functions, minio, vector, realtime, and imgproxy. The pattern for the box is in [stacks/self-hosted-stack.md](../../stacks/self-hosted-stack.md).

**Reach for Neon when all you need is Postgres.** Serverless, scales to zero after five minutes idle, and every branch is a copy-on-write clone of the database, so a pull request can get its own. Ten branches on the free plan. I document Neon from its own docs. My databases run on Supabase.

**Get started with hosted Supabase**

1. Create a project at [supabase.com](https://supabase.com). The free plan gives 500 MB of database, two active projects, and pauses a project after one week without activity. Pro is $25 a month and does not pause. [Pricing](https://supabase.com/pricing).
2. Copy the project URL and anon key into `.env.local`. Names are in [templates/env.example](templates/env.example).
3. In the app: `pnpm add @supabase/supabase-js @supabase/ssr`, then follow the [Next.js quickstart](https://supabase.com/docs/guides/getting-started/quickstarts/nextjs).

**Get started with self-hosted Supabase**

Supabase's own quick start on a Linux box:

```bash
curl -fsSL https://supabase.link/setup.sh | sh
cd supabase-project && sh run.sh start
```

That pulls the Docker stack at `self-hosted/v0.8.2` and starts it. `sh run.sh secrets` prints the keys. I installed mine through Coolify's service catalog instead, which handles the same compose file plus the reverse proxy and certificates. Either way, the Supabase CLI is for local development, not for running the self-hosted stack. [Self-hosting with Docker](https://supabase.com/docs/guides/self-hosting/docker).

**Get started with Neon**

```bash
npx neon@latest init
```

Or sign up at [neon.com](https://neon.com), create a project, and put the connection string in `DATABASE_URL`. The free plan is permanent: 100 compute-hours a month per project, 1 GB of storage per project, ten branches. The Launch plan is pay-as-you-go with no monthly minimum. [Pricing](https://neon.com/pricing).

**Best uses, in the vendors' own words**

- Supabase: Postgres with auto-generated REST and GraphQL APIs, auth including passkeys, file storage, edge functions, self-hosting for full data control
- Neon: dev and test branches on production-shaped data, ephemeral CI branches that delete themselves, point-in-time restore, backends for agents

**Docs**

- Supabase: [docs](https://supabase.com/docs), [getting started](https://supabase.com/docs/guides/getting-started), [Next.js quickstart](https://supabase.com/docs/guides/getting-started/quickstarts/nextjs), [self-hosting](https://supabase.com/docs/guides/self-hosting), [Docker steps](https://supabase.com/docs/guides/self-hosting/docker), [pricing](https://supabase.com/pricing), [changelog](https://supabase.com/changelog)
- Neon: [docs](https://neon.com/docs), [signing up](https://neon.com/docs/get-started/signing-up), [branching](https://neon.com/docs/introduction/branching), [scale to zero](https://neon.com/docs/introduction/scale-to-zero), [pricing](https://neon.com/pricing), [changelog](https://neon.com/docs/changelog)

> [!TIP]
> **The anon key is public by design. Row Level Security is what protects the rows.** Turn RLS on for every table that holds user data before the first deploy, and keep the service role key on the server only. The env template separates the two so the public one never ends up in a server-only slot.

> [!TIP]
> **If you are on the hosted free plan and the project is a side build, expect the pause.** One week quiet and it stops. Restoring is one click in the dashboard, but every request fails until you do. My studio project paused twice in a month before I moved it. Either keep a cron hitting it, pay for Pro, or self-host.

---

## 7. 05 Automation: n8n

**The job.** Everything that runs on a trigger or a schedule, between the tools on this list.

**My pick: n8n.** A visual workflow builder with code nodes, an AI Agent node, and hundreds of integrations. In client work it runs in the client's own account from day one, so they own it when the engagement ends. On my own box it is one container behind the reverse proxy, bound to loopback, HTTPS at the proxy. That layout is in [stacks/self-hosted-stack.md](../../stacks/self-hosted-stack.md). Single tool, no split.

**Get started with n8n Cloud**

1. Sign up at [n8n.io](https://n8n.io). The trial needs no card and includes 1,000 executions.
2. Starter is 20 euros a month billed annually for 2,500 executions. Pro is 50 euros a month for 10,000. [Pricing](https://n8n.io/pricing/), read October 8, 2026.
3. Build the first workflow from a Webhook trigger, add one action node, and call it from the app.

**Get started self-hosted**

n8n's docs point to Docker Compose with a reverse proxy, because n8n only accepts HTTPS. The compose file and `.env` are in the [Docker Compose guide](https://docs.n8n.io/hosting/installation/server-setups/docker-compose/). Then:

```bash
sudo docker compose up -d
```

The Community Edition is free to self-host under n8n's Sustainable Use License, which permits internal use and modification and restricts reselling n8n itself as a hosted service.

**Best uses, in n8n's own words**

- Onboarding automation, ticket enrichment, lead and CRM workflows
- Natural language to API calls
- Traceable AI agents and RAG workflows, through the AI Agent node with a chat model and tools

**Docs**

- [Docs](https://docs.n8n.io), [Docker install](https://docs.n8n.io/hosting/installation/docker/), [Docker Compose](https://docs.n8n.io/hosting/installation/server-setups/docker-compose/), [AI Agent node](https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.agent/), [pricing](https://n8n.io/pricing/), [GitHub](https://github.com/n8n-io/n8n)

> [!TIP]
> **Build the workflow in the account that will own it.** Credentials do not travel with an exported workflow. Moving a client's automation from your account to theirs later means re-entering every API key and reconnecting every OAuth app. Start in their account and that migration never happens.

---

## 8. 06 Source control: GitHub

**The job.** Every change to every file, reviewed before it merges, undoable after.

**My pick: GitHub.** Every repo, including this one and the [open source dashboard](https://github.com/davisxai/operatoros). CI runs lint and typecheck as two parallel jobs on every push and pull request. It validates and never deploys. The workflow in [templates/ci.yml](templates/ci.yml) is the one from my production repos. Single tool, no split.

**Get started**

```bash
brew install gh
gh auth login
cd my-app
gh repo create my-app --private --source=. --push
```

The free plan has unlimited public and private repos, unlimited collaborators on private repos, and 2,000 Actions minutes a month on private repos. Actions on public repos are unlimited on standard runners. Team is $4 per user a month. [Pricing](https://github.com/pricing), read October 8, 2026.

Add the CI workflow if you did not use the scaffold:

```bash
mkdir -p .github/workflows
cp operator-knowledge-base/guides/build-stack/templates/ci.yml .github/workflows/ci.yml
```

It expects `lint` and `typecheck` scripts in `package.json`. `create-next-app` gives you `lint`. Add `"typecheck": "tsc --noEmit"`.

**Best uses, in GitHub's own framing**

- Pull-request review, the GitHub flow
- CI through Actions
- Issues and Projects for tracking, with table, board, and roadmap views
- Dependabot for dependency and security updates

**Docs**

- [Hello World](https://docs.github.com/en/get-started/start-your-journey/hello-world), [GitHub flow](https://docs.github.com/en/get-started/quickstart/github-flow), [Actions](https://docs.github.com/en/actions), [Actions limits](https://docs.github.com/en/actions/reference/limits), [gh CLI](https://cli.github.com/), [pricing](https://github.com/pricing)

> [!TIP]
> **CI validates, the box deploys.** CI never holds a production credential and never touches the server. If your CI can deploy, your CI can be compromised into deploying. The full four-layer pattern, local gate, CI, deploy script, post-deploy checks, is in [stacks/deploy-pattern.md](../../stacks/deploy-pattern.md).

---

## 9. 07 Deploy: Cloudflare

**The job.** Where the app goes live. One account holds the Worker that runs it, the DNS, object storage, a small SQL database, and the domain itself.

**What I run.** My studio dashboard runs on Cloudflare Workers through the OpenNext adapter. Workers Builds watches the GitHub repo and builds and deploys every push to `main`. Cloudflare Access sits in front until the app has its own login. The two config files in `templates/` are the ones from that deploy with the app name swapped: [wrangler.jsonc](templates/wrangler.jsonc) and [open-next.config.ts](templates/open-next.config.ts). Versions on the day of writing: Next.js 16.3.8, `@opennextjs/cloudflare` 1.20.8, wrangler 4.147.0.

**Two ways onto Workers.** Cloudflare's docs now recommend vinext, a Vite plugin that reimplements the Next.js API, as the default for new Next.js apps on Workers. It is in beta. OpenNext is the path for an existing app, and the one I have in production. Pick by situation:

- New app, nothing deployed yet: vinext
- Existing Next.js app, or you want the exact setup I run: OpenNext

**Get started, new app with vinext**

```bash
pnpm create cloudflare@latest my-app --framework=next
cd my-app
pnpm exec wrangler dev
pnpm exec wrangler deploy
```

Adding vinext to an existing Next.js 16 app is `pnpx vinext check` for the compatibility report, then `pnpx vinext init`. [Next.js on Workers](https://developers.cloudflare.com/workers/framework-guides/web-apps/nextjs/).

**Get started, existing app with OpenNext**

```bash
pnpm add @opennextjs/cloudflare wrangler
cp operator-knowledge-base/guides/build-stack/templates/wrangler.jsonc .
cp operator-knowledge-base/guides/build-stack/templates/open-next.config.ts .
pnpm exec opennextjs-cloudflare build
pnpm exec wrangler deploy --dry-run --outdir /tmp/dry
```

Edit `name` in `wrangler.jsonc` first. The dry run prints the bundle size. Then connect the repo in the dashboard: Workers and Pages, Create, Import a repository. Build command `pnpm exec opennextjs-cloudflare build`, deploy command `pnpm exec opennextjs-cloudflare deploy`. Runtime variables and secrets go in the dashboard under Settings, not in the config file. `keep_vars: true` in the template stops a deploy from wiping them. [Workers Builds](https://developers.cloudflare.com/workers/ci-cd/builds/), [OpenNext on Cloudflare](https://opennext.js.org/cloudflare).

**The free plan.** 100,000 requests a day, 10 ms of CPU per invocation, up to 100 Workers, 64 MiB uncompressed per Worker on every plan with no compressed limit. Paid starts at $5 a month with 10 million requests included. R2 object storage: 10 GB a month free, no egress fees. D1: 5 GB and 5 million row reads a day free. Registrar sells domains at cost. [Workers pricing](https://developers.cloudflare.com/workers/platform/pricing/), [limits](https://developers.cloudflare.com/workers/platform/limits/), read October 8, 2026.

**Best uses, in Cloudflare's own framing**

- Full-stack Next.js on Workers, APIs at the edge
- R2 for files, with zero egress charges
- D1 for a small SQL database next to the Worker
- Registrar plus DNS, DNSSEC in one click

**Docs**

- [Workers get started](https://developers.cloudflare.com/workers/get-started/guide/), [Next.js framework guide](https://developers.cloudflare.com/workers/framework-guides/web-apps/nextjs/), [OpenNext guide](https://developers.cloudflare.com/workers/framework-guides/web-apps/opennext/), [opennext.js.org/cloudflare](https://opennext.js.org/cloudflare), [Workers Builds](https://developers.cloudflare.com/workers/ci-cd/builds/), [pricing](https://developers.cloudflare.com/workers/platform/pricing/), [limits](https://developers.cloudflare.com/workers/platform/limits/), [R2 pricing](https://developers.cloudflare.com/r2/pricing/), [D1 pricing](https://developers.cloudflare.com/d1/platform/pricing/), [Registrar](https://developers.cloudflare.com/registrar/)

> [!WARNING]
> **Deploy from GitHub, not from a laptop that holds `.env.local`.** The OpenNext build bakes every local env file into the Worker script. Workers Builds never sees `.env.local` because it is gitignored, so GitHub-driven deploys are clean. A `wrangler deploy` from your machine would ship the service role key inside the bundle.

> [!TIP]
> **The Worker name in the dashboard must match `name` in `wrangler.jsonc`** or the build fails. Set it once in the template before you connect the repo.

---

## 10. 08 Decisions: Jev

**The job.** The yes-or-no, pick-one, and score-this decisions inside an agent. Routing, scoring, risk gates. Text goes in, a decision with a probability comes out, and no text is generated.

**My pick: Jev, TypeSafe AI's System One model.** Three question types: Choice picks from a list of up to 255 options, Score grades against a rubric, Noul answers whether a statement is true. All three return a probability. TypeSafe states 70 to 500 ms per decision, $0.042 per million input tokens, and output free. Jev is in early access. The full install, the three question types, confidence thresholds, and five runnable pattern scripts are in [jev-setup-and-patterns](../jev-setup-and-patterns/). Single tool, no split.

**Get started**

1. Create an account at [typesafe.ai](https://typesafe.ai/) and a key at [console.typesafe.ai/keys](https://console.typesafe.ai/keys).
2. Install the SDK.

```bash
pip install typesafe-sdk
# or
npm install @typesafe-ai/sdk
```

3. Put the key in `TYPESAFE_API_KEY`. Both SDKs read it.
4. Optional, and the way I use it: let Claude Code write the calls.

```bash
claude plugin marketplace add typesafe-ai/skills
claude plugin install typesafe@typesafe-ai
```

**Best uses, as TypeSafe names the patterns**

- Intent routing: classify a message and route it to the handler
- Confidence-gated routing: act above a threshold, send to a human below it
- Speculative fan-out: ask many questions in one call and let code decide what is relevant
- Composite scoring: several rubrics into one score
- Tool-call risk gates, my addition: score an agent's proposed action before it runs

**Docs**

- [Docs](https://docs.typesafe.ai/), [quickstart](https://docs.typesafe.ai/introduction/quickstart), [patterns](https://docs.typesafe.ai/patterns), [launch post](https://typesafe.ai/blog/introducing-system-one-models-and-jev)

> [!TIP]
> **Write the decision spec before the call.** The labels, the rubric, the threshold, and what happens below it. The template is [decision-spec.md](../jev-setup-and-patterns/templates/decision-spec.md) in the Jev guide. A decision model is only as good as the question you hand it.

---

## 11. 09 Memory: Obsidian // Mem0

**The job.** Where the agent keeps what it learned.

**My pick: Obsidian.** My company's memory is a folder of markdown. On October 8, 2026 the vault holds 303 markdown files. Agents write most of them, every page opens with frontmatter that a validator checks, and a consolidation agent runs over it nightly. Obsidian is the reader and the editor. The personal license is free without limits. The design in full is in [ai-os/vault.md](../../ai-os/vault.md), and a copy-and-run starter vault with the schema, the templates, and five Claude Code skills is in [agent-vault-starter](../agent-vault-starter/).

**Reach for Mem0 when the product has many users who each need their own memory.** A hosted memory API, scoped per `user_id`, that compresses chat history into facts the agent can search. One builder who reads the memory: markdown. Many users who never see it: an API. I document Mem0 from its own docs.

**Get started with Obsidian**

1. Download from [obsidian.md](https://obsidian.md/). Free for personal use. Sync is $4 a user a month billed annually, Publish is $8 a site a month billed annually, and a commercial license is $50 a user a year. [Pricing](https://obsidian.md/pricing).
2. A vault is a folder. Point Obsidian at the folder your agent writes to.
3. Turn on Bases for table and card views over frontmatter. Obsidian 1.14 added a kanban view. [Bases](https://obsidian.md/help/bases).
4. Obsidian 1.12 and later ship a command line. Settings, General, Command line interface. It drives the running app rather than running headless. [CLI](https://obsidian.md/help/cli).

Or build the agent-maintained version in one command:

```bash
bash operator-knowledge-base/guides/agent-vault-starter/scripts/new-vault.sh my-vault
```

**Get started with Mem0**

```bash
pip install mem0ai
# or
npm install mem0ai
```

Get a key at [app.mem0.ai](https://app.mem0.ai), no card required. Every call carries a `user_id`. The Hobby plan is free with 10,000 add requests and 1,000 retrievals a month. Starter is $19 a month. [Pricing](https://mem0.ai/pricing), read October 8, 2026.

**Best uses**

- Obsidian: a team or a solo builder who reads and edits what the agent writes, Bases views over structured frontmatter, plain files that any tool can open
- Mem0, in its own words: memory that persists across sessions per user, compressing history to cut tokens and latency

**Docs**

- Obsidian: [help](https://obsidian.md/help), [Bases](https://obsidian.md/help/bases), [CLI](https://obsidian.md/help/cli), [pricing](https://obsidian.md/pricing), [changelog](https://obsidian.md/changelog/)
- Mem0: [docs](https://docs.mem0.ai/), [platform quickstart](https://docs.mem0.ai/platform/quickstart), [pricing](https://mem0.ai/pricing), [GitHub](https://github.com/mem0ai/mem0), [changelog](https://docs.mem0.ai/changelog)

> [!TIP]
> **Split memory by who reads it.** If a human will ever open it, markdown in a folder with a schema. If only the product reads it, an API scoped per user. Mixing the two produces a vault nobody reads and an API nobody can audit.

---

## 12. 10 Integrations: MCP // Composio

**The job.** How the agent touches Gmail, Slack, GitHub, and your CRM.

**My pick: MCP for my own accounts.** The Model Context Protocol is the open standard for connecting an agent to external systems. One server per app, plugged into Claude Code or any client that speaks it. On my machine today: three Gmail accounts, Slack, Cloudflare, and shadcn. The current spec revision is dated July 28, 2026.

**Reach for Composio when your users connect their own accounts.** Composio handles the OAuth flow, token storage, and refresh for over a thousand toolkits behind one API key, so an agent in your product can act in a user's Gmail or CRM without you writing an OAuth integration per app. Your accounts: MCP. Your users' accounts: Composio. I document Composio from its own docs.

**Get started with MCP in Claude Code**

```bash
# a remote server over HTTP
claude mcp add --transport http claude-code-docs https://code.claude.com/docs/mcp

# a local server that runs as a subprocess
claude mcp add playwright -- npx -y @playwright/mcp@latest

claude mcp list
```

Scopes: the default adds the server to this project only, `--scope user` adds it to every project on the machine, and `--scope project` writes it to `.mcp.json` so it ships with the repo. Servers that need OAuth are added the same way and authenticated inside a session with `/mcp`. Each connected server takes space in the context window, so remove the ones you stop using with `claude mcp remove <name>`. Find servers in the [registry](https://registry.modelcontextprotocol.io/), which is in preview. The servers I install first in a new setup are listed in [claude-agents-guide](../claude-agents-guide/README.md#mcp-integrations-worth-installing-first).

**Get started with Composio**

```bash
curl -fsSL https://composio.dev/install | sh
composio login
composio search "send an email"
composio link gmail
```

The Hobby plan is free with 100,000 tool calls and 50,000 triggers a month. Pro is $29 a month. [Pricing](https://composio.dev/pricing), read October 8, 2026.

**Best uses**

- MCP: your own data and tools inside the agent you run, with one config file per project
- Composio, in its own words: agents that take action in users' apps, OAuth managed end to end, triggers from those apps back into the agent

**Docs**

- MCP: [introduction](https://modelcontextprotocol.io/introduction), [spec](https://modelcontextprotocol.io/specification/2026-07-28), [registry](https://registry.modelcontextprotocol.io/), [Claude Code MCP quickstart](https://code.claude.com/docs/en/mcp-quickstart), [Claude Code MCP reference](https://code.claude.com/docs/en/mcp)
- Composio: [docs](https://docs.composio.dev/), [CLI](https://docs.composio.dev/docs/cli), [pricing](https://composio.dev/pricing), [GitHub](https://github.com/composiohq/composio), [changelog](https://docs.composio.dev/reference/changelog)

> [!TIP]
> **Keep the server list short.** Every MCP server loads its tool definitions into every session. Three servers you use daily beat twelve you connected once. Audit with `claude mcp list` and remove what has gone quiet.

---

## 13. What the stack costs

At the free tier, from each vendor's pricing page on October 8, 2026.

- **Claude Pro, $20 a month ($17 billed annually):** Claude Design and Claude Code. The one subscription the stack needs.
- **Framer:** free on a Framer subdomain. $10 a month billed annually for a custom domain.
- **Codex:** included with ChatGPT Plus at $20 a month. Optional.
- **Next.js, shadcn/ui, Tailwind:** free, open source.
- **Supabase:** free, 500 MB, two projects, pauses after a week idle. $25 a month for Pro. Self-hosted: the cost of the box.
- **Neon:** free, 1 GB per project, ten branches. Pay-as-you-go after that.
- **n8n:** free self-hosted. 20 euros a month billed annually on Cloud.
- **GitHub:** free, 2,000 Actions minutes a month on private repos.
- **Cloudflare Workers:** free, 100,000 requests a day. $5 a month for Paid.
- **Jev:** $0.042 per million input tokens, output free. No monthly fee.
- **Obsidian:** free. $4 a month for Sync if you want it on two devices.
- **Mem0:** free, 10,000 adds a month. $19 a month for Starter.
- **MCP:** free, it is a protocol.
- **Composio:** free, 100,000 tool calls a month. $29 a month for Pro.

A builder shipping one product with an agent in it can run every layer for the price of Claude Pro plus whatever the server costs. My own box is one fixed monthly fee for a VPS that runs Supabase, n8n, and the marketing site, and the numbers for that are in [stacks/self-hosted-stack.md](../../stacks/self-hosted-stack.md).

---

## 14. Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| Every Supabase request fails with a connection error on a side project | Hosted free project paused after a week idle | Restore it in the dashboard. Move to Pro, self-host, or keep a scheduled request hitting it |
| Workers Builds fails before the build step | Worker name in the dashboard does not match `name` in `wrangler.jsonc` | Set `name` in the template to the dashboard name, push again |
| `opennextjs-cloudflare build` fails with a missing `server/middleware.js` | Next 16.3.8 leaves the proxy bundle out of the standalone folder | The `buildCommand` in [templates/open-next.config.ts](templates/open-next.config.ts) copies it. Remove the `cp` when upstream fixes it |
| A service key shows up in the Worker bundle | Built from a machine that holds `.env.local` | Deploy from GitHub through Workers Builds. Use `wrangler deploy --dry-run` locally only |
| `pnpm build` passes but CI fails on lint | Next 16 no longer lints inside `next build` | Keep `lint` as its own script. The CI template runs it as a separate job |
| `create-next-app` stops at a prompt inside a script | Running without `--yes` or without a TTY | Pass `--yes`, or set `CI=1` for the run. The scaffold does the first |
| n8n loads over HTTP and refuses to run | n8n only serves over HTTPS | Put it behind the reverse proxy from the Compose guide, or use n8n Cloud |
| First Neon query after a break takes a few hundred milliseconds | Scale to zero after five minutes idle, mandatory on the free plan | Expected. Paid plans can keep compute on |
| `claude mcp list` shows a server as "needs authentication" | OAuth server added but not authorized | Start `claude`, run `/mcp`, pick the server, authenticate in the browser |
| `/stack-map` reports a layer as not detected that you know exists | The proof file is outside the repo or named differently | Automation and memory usually live elsewhere. Point the README at them, or add the dependency the skill looks for |

---

## 15. Quick reference

**Install, every layer**

```bash
# 02 Code
curl -fsSL https://claude.ai/install.sh | bash
npm install -g @openai/codex

# 03 Framework
pnpm create next-app@latest my-app --yes
pnpm dlx shadcn@latest init --defaults

# 04 Database
pnpm add @supabase/supabase-js @supabase/ssr
curl -fsSL https://supabase.link/setup.sh | sh        # self-host
npx neon@latest init

# 05 Automation
sudo docker compose up -d                              # from the n8n compose guide

# 06 Source control
brew install gh && gh auth login
gh repo create my-app --private --source=. --push

# 07 Deploy
pnpm create cloudflare@latest my-app --framework=next  # new app
pnpm add @opennextjs/cloudflare wrangler               # existing app
pnpm exec opennextjs-cloudflare build
pnpm exec wrangler deploy --dry-run --outdir /tmp/dry

# 08 Decisions
pip install typesafe-sdk
npm install @typesafe-ai/sdk

# 09 Memory
pip install mem0ai
npm install mem0ai

# 10 Integrations
claude mcp add --transport http <name> <url>
claude mcp add <name> -- npx -y <package>
curl -fsSL https://composio.dev/install | sh
```

**The files in this folder**

- `scripts/stack-doctor.sh`: what is installed, what is missing, how to install it
- `scripts/new-stack.sh`: Next.js, Supabase client, shadcn, CI, CLAUDE.md, env example, first commit
- `templates/CLAUDE.md`: project instructions for Claude Code
- `templates/env.example`: every variable the ten layers use, by layer
- `templates/ci.yml`: lint and typecheck in parallel, validates only
- `templates/wrangler.jsonc`: the Worker config from my production deploy
- `templates/open-next.config.ts`: the OpenNext config, with the Next 16.3.8 workaround
- `../../skills/stack-map/`: the skill that reads a repo against the ten layers

**The ten layers in one line each**

- 01 Design: Claude Design for layouts and decks, Framer when the thing is a site
- 02 Code: Claude Code builds with you, Codex takes delegated tasks and returns PRs
- 03 Framework: Next.js, App Router, shadcn/ui
- 04 Database: Supabase for the whole backend, Neon when you only need Postgres
- 05 Automation: n8n, in the account that will own it
- 06 Source control: GitHub, CI validates and never deploys
- 07 Deploy: Cloudflare Workers, vinext for new apps, OpenNext for existing ones
- 08 Decisions: Jev, typed decisions with a probability, no generated text
- 09 Memory: Obsidian when a human reads it, Mem0 when only the product does
- 10 Integrations: MCP for your accounts, Composio for your users' accounts

---

## 16. Sources

All read October 8, 2026.

- Claude Design: https://claude.com/product/design, https://support.claude.com/en/articles/14604416-get-started-with-claude-design, https://claude.com/pricing
- Framer: https://www.framer.com/pricing/, https://www.framer.com/help/, https://www.framer.com/developers/changelog
- Claude Code: https://code.claude.com/docs/en/quickstart, https://code.claude.com/docs/en/overview, https://code.claude.com/docs/en/changelog, https://code.claude.com/docs/en/mcp-quickstart
- Codex: https://developers.openai.com/codex, https://github.com/openai/codex/releases, https://www.npmjs.com/package/@openai/codex
- Next.js: https://nextjs.org/docs/app/getting-started/installation, https://nextjs.org/blog/next-16-4
- Supabase: https://supabase.com/pricing, https://supabase.com/docs/guides/self-hosting/docker, https://supabase.com/changelog
- Neon: https://neon.com/pricing, https://neon.com/docs/introduction/branching, https://neon.com/docs/introduction/scale-to-zero
- n8n: https://n8n.io/pricing/, https://docs.n8n.io/hosting/installation/docker/, https://docs.n8n.io/hosting/installation/server-setups/docker-compose/, https://github.com/n8n-io/n8n
- GitHub: https://github.com/pricing, https://docs.github.com/en/actions/reference/limits, https://cli.github.com/
- Cloudflare: https://developers.cloudflare.com/workers/platform/pricing/, https://developers.cloudflare.com/workers/platform/limits/, https://developers.cloudflare.com/workers/framework-guides/web-apps/nextjs/, https://developers.cloudflare.com/workers/framework-guides/web-apps/opennext/, https://developers.cloudflare.com/workers/ci-cd/builds/, https://developers.cloudflare.com/r2/pricing/, https://developers.cloudflare.com/d1/platform/pricing/
- Jev: https://docs.typesafe.ai/introduction, https://docs.typesafe.ai/patterns, https://typesafe.ai/blog/introducing-system-one-models-and-jev
- Obsidian: https://obsidian.md/pricing, https://obsidian.md/help/bases, https://obsidian.md/help/cli, https://obsidian.md/changelog/
- Mem0: https://docs.mem0.ai/platform/quickstart, https://mem0.ai/pricing, https://github.com/mem0ai/mem0
- MCP: https://modelcontextprotocol.io/introduction, https://modelcontextprotocol.io/specification/2026-07-28, https://modelcontextprotocol.io/registry/about, https://code.claude.com/docs/en/mcp-quickstart
- Composio: https://docs.composio.dev/docs/cli, https://composio.dev/pricing, https://github.com/composiohq/composio
- My own numbers: skill, agent, and hook counts from the Claude Code directories on this machine; the Supabase container list from the server inventory; the vault file count from the live vault; the Cloudflare deploy from the studio repo's runbook. All on October 8, 2026.

---

Built by OperatorOS | [operatoros.ai](https://operatoros.ai)
Follow [@daviss.dev](https://instagram.com/daviss.dev) and [@os.operator](https://instagram.com/os.operator) for production-grade AI guides.
