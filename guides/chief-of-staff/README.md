# Chief of Staff Agent

> Follow [@davis.mcm](https://instagram.com/davis.mcm) and [@operatoros](https://instagram.com/operatoros) on Instagram for more guides like this.

---

### The ECC chief-of-staff agent, with the rest of the setup it needs to run.

[ECC](https://github.com/affaan-m/ECC) (formerly everything-claude-code) is Affaan Mustafa's open source collection of agents, skills, commands, and hooks for Claude Code. MIT licensed, 280,119 stars on 2026-10-15. One of its agents is [`chief-of-staff.md`](https://github.com/affaan-m/ECC/blob/main/agents/chief-of-staff.md), contributed by GitHub user [tomochang](https://github.com/tomochang) in [PR #280](https://github.com/affaan-m/ECC/pull/280), merged on 2026-02-27.

The agent triages your email and Slack, sorts every message into one of four tiers, drafts replies in your tone, and runs a checklist after every send so nothing you promised falls through.

The agent is one file. It points at a tone file, three memory files, four slash commands, a scheduling script, and a follow-through hook that live in the author's own setup. This guide is the rest of the setup: every one of those pieces as a working file, plus the steps to wire them together.

---

## What you'll get

→ Both install paths for the agent: the full ECC plugin, or the single agent file

→ `SOUL.md`, `relationships.md`, `preferences.md`, and `todo.md` as filled templates you edit

→ `/today`, `/mail`, `/slack`, and `/schedule-reply` as Claude Code slash commands that work with the gog CLI or a Gmail MCP server

→ The PostToolUse follow-through hook, tested, with the `settings.json` block

→ `calendar-suggest.js`, a zero-dependency script that turns busy blocks into free slots in your timezone

→ The daily routine and the edits that make it yours

---

## Contents

1. [What the agent does](#1-what-the-agent-does)
2. [The pieces and what each one does](#2-the-pieces-and-what-each-one-does)
3. [Install the agent](#3-install-the-agent)
4. [Connect Gmail, Calendar, and Slack](#4-connect-gmail-calendar-and-slack)
5. [Set up the working folder](#5-set-up-the-working-folder)
6. [The follow-through hook](#6-the-follow-through-hook)
7. [calendar-suggest.js](#7-calendar-suggestjs)
8. [Daily use](#8-daily-use)
9. [Make it yours](#9-make-it-yours)
10. [Quick reference](#10-quick-reference)
11. [Sources](#11-sources)

---

## 1. What the agent does

### Four tiers

Every message lands in exactly one tier. The agent checks them in this order and stops at the first match.

- **skip:** Auto-archived, shown as a count. Senders like `noreply`, `notification`, and `alert`, mail from `@github.com`, `@slack.com`, `@jira`, and `@notion.so`, bot messages, and channel joins and leaves.
- **info_only:** One-line summary. Emails you are CC'd on, receipts, group chatter, `@channel` and `@here` announcements, file shares with no question.
- **meeting_info:** Cross-referenced with your calendar. Anything with a Zoom, Teams, Meet, or WebEx link, a date with meeting context, a room share, or an `.ics` attachment. The agent fills in missing links.
- **action_required:** A draft reply. Direct questions, `@mentions` waiting on you, scheduling requests, explicit asks.

### Drafts with Send, Edit, Skip

For each action_required message the agent reads the sender's section in `relationships.md` and your tone rules in `SOUL.md`. If the message is about scheduling, it gets free slots from `calendar-suggest.js` instead of guessing. Then it shows the draft with three choices: `[Send] [Edit] [Skip]`. Nothing goes out until you pick Send.

### Follow-through after every send

The agent file lists seven steps to finish after every message you send:

1. **Calendar:** `[Tentative]` events for proposed dates, updated meeting links
2. **Relationships:** the interaction appended to the sender's section
3. **Todo:** upcoming events updated, completed items marked
4. **Pending responses:** follow-up deadlines set, resolved items removed
5. **Archive:** the processed message removed from the inbox
6. **Triage files:** LINE and Messenger draft status updated
7. **Git commit and push:** the knowledge files versioned

The design idea in the file: put the checklist in a hook, so it arrives as a system message the moment a send happens, instead of in a prompt the model has to remember. Section 6 is that hook.

### The output

The agent's briefing format, as the file describes it:

```
# Today's Briefing: [Date]

## Schedule (N)
## Email: Skipped (N), auto-archived
## Email: Action Required (N)
### 1. Sender <email>
Subject, Summary, Draft reply
[Send] [Edit] [Skip]
## Slack: Action Required (N)
## Triage Queue
- Stale pending responses: N
- Overdue tasks: N
```

---

## 2. The pieces and what each one does

The agent file references these by name. I searched the ECC repo for each one on 2026-10-15. Only the agent file ships there, along with its translated copies. ECC does have a `SOUL.md` at its root, but that one describes ECC as a project. It is not the tone file the agent means.

Everything below ships in this folder.

- **[templates/SOUL.md](templates/SOUL.md)** Your tone rules. Who you are, how you write, how formal to be with each kind of contact, how to write scheduling replies, and the hard rules a draft must never break. Every draft is written against it.
- **[templates/relationships.md](templates/relationships.md)** One section per person: email, company, tone tag (`formal`, `casual`, `friendly`), timezone, context, preferences, and a dated interaction log the agent appends to after each send.
- **[templates/preferences.md](templates/preferences.md)** Working hours, meeting defaults, triage overrides (senders to always skip, always flag, never archive), the channels you use, and follow-up timing.
- **[templates/todo.md](templates/todo.md)** Upcoming events, pending responses with follow-up dates, tasks, and what got done this week. The agent's memory between sessions.
- **[commands/today.md](commands/today.md)** `/today`. Every channel plus calendar plus the triage queue, in one briefing.
- **[commands/mail.md](commands/mail.md)** `/mail`. Email only. Takes an optional Gmail query.
- **[commands/slack.md](commands/slack.md)** `/slack`. Mentions and DMs only. Takes an optional time window.
- **[commands/schedule-reply.md](commands/schedule-reply.md)** `/schedule-reply "Reply to Priya about the review call"`. Finds the thread, pulls your busy blocks, runs the slot script, drafts the reply.
- **[hooks/follow-through.js](hooks/follow-through.js)** The PostToolUse hook. Fires after a send and hands the agent the seven-step checklist.
- **[hooks/settings.json](hooks/settings.json)** The block that registers the hook.
- **[scripts/calendar-suggest.js](scripts/calendar-suggest.js)** Free-slot math. Busy blocks in, open times out, timezone and daylight saving handled in code.

The agent file names `private/relationships.md`. This setup keeps all three memory files in `private/`, and `SOUL.md` at the root, so the paths in the agent file and the commands line up.

---

## 3. Install the agent

You need [Claude Code](https://code.claude.com/docs) and Node.js 18 or newer. Pick one path.

### Path A: the full ECC plugin

This installs the whole ECC collection, chief-of-staff included. The ECC README gives two ways to do it. Choose one, not both. The README is explicit that stacking install methods duplicates skills, commands, and hooks.

The guided setup:

```bash
npx ecc-universal@2.2.3 setup
```

The ECC README recommends `setup` for Claude Code. If you also want ECC in Codex or Kimi Code in the same pass, it offers the multi-harness wizard instead:

```bash
npx ecc-universal@2.2.3 install --guided
```

Or Claude Code's native plugin commands, run inside Claude Code:

```
/plugin marketplace add https://github.com/affaan-m/ECC
/plugin install ecc@ecc
```

The plugin slug is `ecc@ecc`. Start a new session and run `/plugin list` to confirm it is enabled. ECC's README lists the official sources (the GitHub repo, the `ecc-universal` npm package, and the `ecc@ecc` slug) and warns against third-party mirrors.

### Path B: just the agent file

If you only want the chief of staff, copy the one file into your user agents folder:

```bash
mkdir -p ~/.claude/agents
curl -fsSL https://raw.githubusercontent.com/affaan-m/ECC/main/agents/chief-of-staff.md \
  -o ~/.claude/agents/chief-of-staff.md
```

Read it once before you use it. It is about 160 lines.

Either way, run `/agents` inside Claude Code and confirm chief-of-staff is listed.

---

## 4. Connect Gmail, Calendar, and Slack

The commands work with either Gmail option below. They check for `gog` first and fall back to a Gmail MCP server.

### Gmail and Calendar with gog

The agent file's own fetch commands use `gog`, a Google Workspace CLI. It now lives at [openclaw/gogcli](https://github.com/openclaw/gogcli) (MIT). Install and authorize it the way its README shows:

```bash
brew install openclaw/tap/gogcli
gog auth credentials set ~/Downloads/client_secret_*.json
gog auth add you@gmail.com --services gmail,calendar
export GOG_ACCOUNT=you@gmail.com
gog auth doctor --check
```

The credentials file is a Desktop OAuth client from your own Google Cloud project. The gogcli quickstart walks through creating it. Then test:

```bash
gog gmail search "is:unread" --max 5
gog calendar events --today --all --json
```

### Gmail with an MCP server

If you already run a Gmail MCP server in Claude Code, the commands use its search, read, and send tools. Nothing else to install. The hook recognizes any MCP tool whose server or tool name contains `gmail` or `mail` and whose tool name contains `send`, so a tool like `mcp__gmail__send_gmail_message` or `mcp__gmail__send_email` counts. Draft tools do not.

For calendar, use a calendar MCP server, or install gog for calendar only.

### Slack

The agent file's Slack calls (`conversations_search_messages`, `channels_list`, `conversations_history`, `conversations_add_message`) are the tool names of [korotovsky/slack-mcp-server](https://github.com/korotovsky/slack-mcp-server). Posting is off by default in that server. Set `SLACK_MCP_ADD_MESSAGE_TOOL` to `true`, or to a comma-separated list of channel IDs, so Send works.

Any Slack MCP server with a tool name containing `send`, `post`, `reply`, or `add_message` triggers the hook.

Slack is optional. `/today` and `/mail` run on email and calendar alone.

---

## 5. Set up the working folder

The agent reads its files relative to where you start Claude Code, so it gets its own folder. That folder is also a git repo, because step 7 of the follow-through commits to it.

```bash
git clone https://github.com/davisxai/operator-knowledge-base.git
cd operator-knowledge-base/guides/chief-of-staff

COS=~/chief-of-staff
mkdir -p "$COS/private" "$COS/scripts" "$COS/.claude/commands" "$COS/.claude/hooks"

cp templates/SOUL.md "$COS/"
cp templates/relationships.md templates/preferences.md templates/todo.md "$COS/private/"
cp scripts/calendar-suggest.js "$COS/scripts/"
cp commands/*.md "$COS/.claude/commands/"
cp hooks/follow-through.js "$COS/.claude/hooks/"
cp hooks/settings.json "$COS/.claude/settings.json"

cd "$COS" && git init && git add -A && git commit -m "Chief of staff setup"
```

The result:

```
~/chief-of-staff/
├── SOUL.md                     tone rules
├── private/
│   ├── relationships.md        one section per person
│   ├── preferences.md          hours, defaults, triage overrides
│   └── todo.md                 events, pending responses, tasks
├── scripts/
│   └── calendar-suggest.js     free-slot math
└── .claude/
    ├── commands/               /today /mail /slack /schedule-reply
    ├── hooks/
    │   └── follow-through.js   the post-send checklist
    └── settings.json           registers the hook
```

> [!IMPORTANT]
> `private/` holds names, emails, and notes about real people. Push this repo to a private remote only.

Then fill in the templates. Replace every example entry with your own:

1. **SOUL.md.** Your name, role, signature, timezone. Rewrite "How I write" until it sounds like you. Paste one real reply you were happy with as the example.
2. **private/preferences.md.** Working hours, meeting length, buffer, the senders you always skip, and the ones you never want archived.
3. **private/relationships.md.** Start with the ten people you email most. Email, tone tag, timezone, one line of context. The agent adds the interaction lines.
4. **private/todo.md.** Clear the examples. Leave the headings. The agent fills it.

Commit again when you are done.

---

## 6. The follow-through hook

### What it does

Claude Code runs PostToolUse hooks right after a tool call succeeds. The hook gets the call as JSON on stdin: `tool_name`, `tool_input`, `tool_response`, and the session fields. [follow-through.js](hooks/follow-through.js) checks whether that call was a send:

- **Bash** running `gog gmail send` or `gog gmail drafts send` (`mail` and `email` work as aliases for `gmail`). It reads the subcommand words, so a search for the word "send" does not count.
- **A Gmail MCP send tool**, as described in section 4.
- **A Slack MCP post tool:** `send`, `post`, `reply`, or `add_message` in the tool name.

When it was a send, the hook prints this shape to stdout:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "An email was just sent to sam@example.com (gog CLI).\nBefore moving on to anything else, complete the chief-of-staff follow-through checklist:\n1. Calendar: ...\n...\n7. Git commit and push: ..."
  }
}
```

Claude Code places `additionalContext` next to the tool result, so the checklist is in front of the agent the moment the message goes out. For every other tool call, the hook exits 0 with no output, and nothing changes.

### Register it

[hooks/settings.json](hooks/settings.json) goes in `.claude/settings.json` in the working folder. Section 5 already copied it. If the folder had a settings file already, merge the `PostToolUse` entry into it.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "^Bash$|^mcp__.*(send|post|add_message|reply).*",
        "hooks": [
          {
            "type": "command",
            "command": "node",
            "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/follow-through.js"],
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

The matcher is a regular expression on the tool name. It sends every Bash call and any MCP tool with a send-like name to the script, and the script makes the final call. Setting `args` runs the hook in exec form, which the Claude Code docs recommend for any hook that uses a path placeholder like `${CLAUDE_PROJECT_DIR}`.

### Test it

From the working folder, pipe in a fake send and a fake search:

```bash
echo '{"hook_event_name":"PostToolUse","tool_name":"Bash","tool_input":{"command":"gog gmail send --to sam@example.com --subject hi --body ok"}}' \
  | node .claude/hooks/follow-through.js

echo '{"hook_event_name":"PostToolUse","tool_name":"Bash","tool_input":{"command":"gog gmail search \"please send\""}}' \
  | node .claude/hooks/follow-through.js; echo "exit $?"
```

The first prints the JSON above. The second prints nothing and `exit 0`.

To make the checklist harder to pass over, change the output to `"decision": "block"` with the checklist as `"reason"`. Claude Code then shows it as feedback on the tool result instead of as added context.

---

## 7. calendar-suggest.js

The agent file's rule: calendar math, timezones, and free-slot calculation belong in a script, not in the model. [calendar-suggest.js](scripts/calendar-suggest.js) is that script. Node 18 or newer, no dependencies.

It reads busy blocks as JSON from a file or stdin. It accepts the output of `gog calendar events --json` directly, Google Calendar event objects (`start.dateTime` or `start.date` for all-day), Google free/busy responses, or a plain list:

```json
[
  { "start": "2026-10-19T09:30:00-04:00", "end": "2026-10-19T10:50:00-04:00" },
  { "start": "2026-10-19T13:00:00-04:00", "end": "2026-10-19T14:00:00-04:00" }
]
```

Run it:

```bash
gog calendar events --days 7 --all --max 250 --json \
  | node scripts/calendar-suggest.js --tz America/New_York --hours 09:00-18:00 --duration 30 --days 5 --pick 3
```

Output:

```
Free slots for a 30 min meeting (America/New_York, 09:00-18:00)
Mon 2026-10-19: 09:00-09:30, 11:00-13:00, 15:00-18:00
Tue 2026-10-20: no free slot
Wed 2026-10-21: 09:00-10:00, 17:30-18:00
Thu 2026-10-22: 09:00-18:00
Fri 2026-10-23: 09:00-18:00

Suggested:
  2026-10-19T09:00:00-04:00 to 2026-10-19T09:30:00-04:00
  2026-10-21T09:00:00-04:00 to 2026-10-21T09:30:00-04:00
  2026-10-22T09:00:00-04:00 to 2026-10-22T09:30:00-04:00
```

The options:

- **`--busy FILE`** Read busy blocks from a file instead of stdin.
- **`--tz ZONE`** IANA timezone for your hours and the output. Defaults to the system zone.
- **`--hours HH:MM-HH:MM`** Working hours. Default `09:00-18:00`.
- **`--duration MIN`** Meeting length. Default 30.
- **`--days N`** Working days to search. Default 5.
- **`--from YYYY-MM-DD`** First day. Default today.
- **`--weekends`** Include Saturday and Sunday.
- **`--buffer MIN`** Gap kept before and after each busy block.
- **`--step MIN`** Slot starts round up to this grid. Default 15, so a meeting ending at 10:50 frees you at 11:00.
- **`--pick N`** Suggest N start times, one per day, for the draft.
- **`--json`** Machine-readable output for the agent.

All-day events block the whole day. Events marked free (`transparency: transparent`) and cancelled events are ignored. Times already past today are skipped.

---

## 8. Daily use

Open Claude Code in the working folder:

```bash
cd ~/chief-of-staff
claude
```

**Morning.** Run `/today`. Read the schedule and the triage queue first. Then go down the action_required list and answer each draft with Send, Edit, or Skip. After each Send, the hook fires and the agent works through the follow-through before it shows you the next draft.

**During the day.** `/mail` when the inbox builds up. `/slack` after a meeting block. Both take an argument: `/mail from:client.com newer_than:2d` or `/slack last 2 hours`.

**When someone asks for time.** `/schedule-reply "Reply to Priya about the review call"`. You get a draft with two or three real slots in her timezone, and after Send, tentative holds on your calendar for each one.

**End of day.** The follow-through has already committed your knowledge files after each send. `git log --oneline` in the working folder shows what changed and when.

---

## 9. Make it yours

- **Tone.** Every draft that sounds wrong is a missing rule in `SOUL.md`. Add the rule, not a correction in chat. The next session reads the file. It does not remember the chat.
- **Triage rules.** The four tiers live in the agent file. Your exceptions live in `private/preferences.md` under Triage overrides. Add a sender there the second time the agent misfiles them.
- **Channels.** The agent file also names LINE (through a Matrix bridge) and Messenger (through Chrome and Playwright). Add a fetch step for each to `/today` the same way the Slack step is written. If you only use email, delete the Slack step from `/today`.
- **The checklist.** The seven steps are the `CHECKLIST` array at the top of `follow-through.js`. Drop step 6 if you only triage email and Slack. Change step 7 if you would rather commit once at the end of the day.
- **Permissions.** Each command's `allowed-tools` pre-approves the read-only calls (search, read, calendar list, the slot script). Send is left out on purpose, so in the default permission mode Claude Code asks before every send. That prompt is a second Send button. Add `Bash(gog gmail send *)` to a command's `allowed-tools` only once you trust the drafts.
- **Model.** The agent file sets `model: sonnet` in its frontmatter. Change it in your copy if you want a different model for triage.
- **Tools.** The agent file's `tools:` line lists Read, Grep, Glob, Bash, Edit, and Write. The commands fetch mail and Slack in the main session and pass the messages to the agent, so it does not need MCP tools. If you want the agent to call your MCP servers itself, remove the `tools:` line from your copy so it inherits every tool.

> [!TIP]
> **Start with `/mail` for a week before `/today`.** One channel makes it easy to see which rule in `SOUL.md` or `preferences.md` produced each draft. Add Slack once email drafts need few edits.

> [!TIP]
> **Write relationship notes as facts.** "Prefers mornings, wants a written recap after calls" gives the agent something to act on. Adjectives about a person do not.

> [!TIP]
> **Keep the memory files short.** The agent reads all three on every run. Move finished items in `todo.md` to git history instead of letting the file grow.

---

## 10. Quick reference

**Commands**

- **`/today`** All channels, calendar, triage queue
- **`/mail [query]`** Email only
- **`/slack [window]`** Slack mentions and DMs
- **`/schedule-reply "<who and what>"`** Scheduling reply with real slots

**Files in the working folder**

- **`SOUL.md`** Tone rules
- **`private/relationships.md`** People, tone tags, interaction log
- **`private/preferences.md`** Hours, defaults, triage overrides
- **`private/todo.md`** Events, pending responses, tasks
- **`scripts/calendar-suggest.js`** Free slots
- **`.claude/hooks/follow-through.js`** Post-send checklist
- **`.claude/settings.json`** Hook registration
- **`~/.claude/agents/chief-of-staff.md`** The agent (Path B)

**Install**

```bash
npx ecc-universal@2.2.3 setup                      # Path A, guided
curl -fsSL https://raw.githubusercontent.com/affaan-m/ECC/main/agents/chief-of-staff.md \
  -o ~/.claude/agents/chief-of-staff.md             # Path B
brew install openclaw/tap/gogcli                    # Gmail and Calendar CLI
```

Path A native, inside Claude Code: `/plugin marketplace add https://github.com/affaan-m/ECC`, then `/plugin install ecc@ecc`.

**Checks**

```bash
gog auth doctor --check
node scripts/calendar-suggest.js --help
echo '{"hook_event_name":"PostToolUse","tool_name":"Bash","tool_input":{"command":"gog gmail send --to a@example.com"}}' | node .claude/hooks/follow-through.js
```

---

## 11. Sources

- ECC by Affaan Mustafa, MIT, 280,119 stars on 2026-10-15: https://github.com/affaan-m/ECC
- The agent file: https://github.com/affaan-m/ECC/blob/main/agents/chief-of-staff.md
- PR #280 by tomochang, "feat(agents): add chief-of-staff communication triage agent", merged 2026-02-27: https://github.com/affaan-m/ECC/pull/280
- ECC install section (guided setup, native plugin commands, the `ecc@ecc` slug): https://github.com/affaan-m/ECC#install-ecc
- gogcli, the gog CLI: https://github.com/openclaw/gogcli
- korotovsky/slack-mcp-server: https://github.com/korotovsky/slack-mcp-server
- Claude Code hooks reference (PostToolUse input, `additionalContext`, matchers, exec form): https://code.claude.com/docs/en/hooks
- Claude Code slash commands and skills (command files, frontmatter, `$ARGUMENTS`): https://code.claude.com/docs/en/slash-commands
- The list of files ECC does not ship comes from a search of the ECC repo tree and code on 2026-10-15.
