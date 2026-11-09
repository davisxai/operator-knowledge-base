# find-skills: The Skill That Installs Skills

> Follow [@os.operator](https://instagram.com/os.operator) on Instagram for more guides like this.

A setup guide for find-skills by Vercel Labs: the Claude Code skill that searches the skills.sh directory and installs other skills on your approval. Not a tool review. Install, mechanics, and the setup I run.

## What you'll get

→ The one-command install for find-skills, project or global
→ How the search, rank, approve, install flow works under the hood
→ A tested install script you can run as is
→ Five copy-paste prompts to put it to work on day one
→ The Skills CLI commands worth knowing: find, add, use, update
→ A quick reference card for daily use

---

## The problem

Adding skills to Claude Code by hand is the same loop every time. Search GitHub for something that might exist. Open the repo. Read enough to trust it. Copy the link. Run the install. Then do it again for the next one. The skills ecosystem passed a million published skills, and the manual loop does not scale past the three or four you already know about.

## Why this changes things

> [!NOTE]
> **One prompt replaces the search.** You describe the task in plain words inside Claude Code. The skill queries the skills.sh directory for you.

> [!NOTE]
> **Every match comes with evidence.** Results carry install counts and the source repo, so you judge a skill the way you judge a package: by who ships it and who uses it.

> [!NOTE]
> **Approval stays with you.** Nothing lands on disk until you say yes. The skill proposes, you decide.

> [!NOTE]
> **The toolbox maintains itself.** Once installed, skill discovery becomes something Claude does mid-task, not a chore you batch on weekends.

## How it actually works

### 1. The ask

find-skills activates when you ask Claude Code things like "find a skill for X", "is there a skill that can do X", or "how do I do X" where X is a common task. You do not invoke it by name. The skill's own description tells Claude when to fire it.

### 2. The search and rank

The skill checks the [skills.sh leaderboard](https://skills.sh) first for a well-known match, then runs the Skills CLI search:

```bash
npx skills find [query] [--owner <owner>]
```

skills.sh indexes the open agent skills ecosystem. As of November 9, 2026, the directory's All Time tab counts 1,295,047 skills. Matches come back ranked, and the skill weighs install counts and source reputation when it proposes one.

### 3. Approve and install

The skill presents what it found, with numbers. You approve one, and it installs through the same CLI:

```bash
npx skills add <owner/repo> --skill <name>
```

The skill lands in `.claude/skills/` in your project. No restart needed.

## The anatomy

A skill is a folder with a SKILL.md: frontmatter that tells the agent when to use it, then instructions. This is the actual frontmatter of find-skills:

```markdown
---
name: find-skills
description: Helps users discover and install agent skills when they ask
  questions like "how do I do X", "find a skill for X", "is there a skill
  that can...", or express interest in extending capabilities.
---
```

That description field is the whole trigger mechanism. Claude reads it and decides when the skill applies.

## Use cases by role

<details>
<summary><strong>For developers</strong></summary>

Mid-build, you hit a domain you have no process for: test coverage, accessibility, performance profiling. Ask "find a skill for integration testing" and keep working while the search runs. The proposed skill arrives with install counts, so you are not gambling on the first GitHub result.

</details>

<details>
<summary><strong>For operators and founders</strong></summary>

You run Claude Code for business work, not engineering. Ask for skills around document processing, research workflows, or reporting. The directory's top skills skew practical: the top ten includes document and design skills, not just code tooling.

</details>

<details>
<summary><strong>For designers and content work</strong></summary>

The design cluster is one of the strongest on the directory. A search for design work surfaces skills like frontend-design by Anthropic and web-design-guidelines by Vercel Labs, both past 800K installs at this writing. Ask for the task ("find a skill for mobile app design"), approve the match, and the guidelines ride along in every later prompt.

</details>

## The compounding effect

Week one, find-skills is a shortcut: two or three installs you would have hunted for manually. A month in, your project carries a toolbox shaped by the work you actually do, because every skill got added at the moment a real task needed it. Three months in, the loop inverts. You stop tracking the ecosystem. When a task needs a capability, the capability gets found, vetted by numbers, and installed in the same conversation.

## Install it

1. **Check the prerequisite.** The Skills CLI runs on Node.js:

```bash
node -v
```

2. **Install find-skills into your project.** From the project root:

```bash
npx skills add vercel-labs/skills --skill find-skills -a claude-code -y
```

Add `-g` to install globally so every project gets it. Or run the tested script in this folder:

```bash
bash scripts/install.sh
```

3. **Verify it landed:**

```bash
npx skills ls
```

You should see find-skills in the list, and the folder at `.claude/skills/find-skills/`.

4. **Use it.** Open Claude Code and ask for a real task:

```
Find a skill for mobile app design.
```

5. **Approve the match.** Claude proposes what it found with install counts and the source repo. Say yes to the one you want. It installs into `.claude/skills/` in the same conversation.

6. **Keep the set current:**

```bash
npx skills update
```

Five more starter prompts are in [templates/first-prompts.md](templates/first-prompts.md).

## Pro tips

> [!TIP]
> **Install it globally if you work across repos.** `-g` puts it at the user level, so skill discovery works in every project without a per-repo install.

> [!TIP]
> **Name the domain and the task.** "Find a skill for React performance profiling" beats "find me something useful." The search is keyword-based, and a vague query returns a vague match.

> [!TIP]
> **Read a skill before you approve it.** A skill is instructions your agent will follow. Open the repo, read the SKILL.md, then say yes. Install count measures popularity, not quality: a signal, not a review.

> [!TIP]
> **Try before installing.** `npx skills use <owner/repo>@<skill>` generates a prompt for using a skill once without adding it to your project.

> [!TIP]
> **Scope searches to sources you trust.** `npx skills find [query] --owner vercel-labs` limits results to one GitHub owner.

> [!TIP]
> **Audit occasionally.** `npx skills ls` shows what is installed. Remove what you stopped using with `npx skills remove`. A lean skill set keeps the agent's context lean too.

## Quick reference

```bash
# install find-skills (project)
npx skills add vercel-labs/skills --skill find-skills -a claude-code -y

# install globally
npx skills add vercel-labs/skills --skill find-skills -a claude-code -y -g

# install as real files instead of symlinks
npx skills add vercel-labs/skills --skill find-skills -a claude-code -y --copy

# search the directory yourself
npx skills find [query] [--owner <owner>]

# try a skill without installing
npx skills use <owner/repo>@<skill>

# list / update / remove
npx skills ls
npx skills update
npx skills remove
```

- Skill source: [vercel-labs/skills](https://github.com/vercel-labs/skills), the find-skills folder
- Directory and leaderboard: [skills.sh](https://skills.sh)
- Installed location: `.claude/skills/find-skills/` (project) or `~/.claude/skills/` (global)
- Standing: #1 on the skills.sh all-time leaderboard, 4,274,742 installs of a 1,295,047-skill directory (November 9, 2026)

## Sources

- [vercel-labs/skills on GitHub](https://github.com/vercel-labs/skills), the skill's SKILL.md and the repo README
- [skills.sh](https://skills.sh), leaderboard and search API, pulled November 9, 2026

---

Built by OperatorOS | [operatoros.ai](https://operatoros.ai)
Follow [@os.operator](https://instagram.com/os.operator) for production-grade AI guides.
Skill credited to Vercel Labs.
