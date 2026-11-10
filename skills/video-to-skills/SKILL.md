---
name: video-to-skills
description: Turn one long video (a talk, a podcast episode, a lecture, a keynote) into an analysis and a three-skill pack for that person: script, ideate, validate. Reads people/<name>/transcript/transcript.md, writes people/<name>/analysis/analysis.md, then installs <name>-script, <name>-ideate, and <name>-validate in ~/.claude/skills/. Use when the user says "tear this talk apart", "build the pack for <name>", "video to skills <name>", or after pull.py has filled a person folder.
argument-hint: [person-folder-name]
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(ls *), Bash(wc *), Bash(mkdir *), Bash(cp *)
---

# Video to skills

One person's long video in. An analysis of how they teach, plus three skills that put it to work on the user's own content, out.

The output is never a summary. A summary is one page you read once. The pack is three commands the user runs every week.

## Step 1: Find the folder

`$ARGUMENTS` is the person folder name (for example `hormozi`). Look for it in this order and stop at the first hit:

1. `people/$ARGUMENTS/transcript/transcript.md`
2. `$ARGUMENTS/transcript/transcript.md`
3. Any `**/$ARGUMENTS/transcript/transcript.md` under the current directory

If nothing matches, say so and give the command that creates it:

```
python3 scripts/pull.py <name> <youtube-url>
```

Read `transcript/meta.json` next to it for the title, channel, URL, length, and word count. Set `NAME` to the person's display name (ask if the folder name is not obviously a person, for example `q3-keynote`), and `SLUG` to the folder name.

## Step 2: Find the user's voice

The pack writes the user's content in the person's structure, so every pack skill reads the user's own voice file first. Look for `~/.claude/skills/voice-dna/SKILL.md`.

- Found: note the path. Read its Anti-voice section now, you need it in Step 4.
- Not found: tell the user, point them at the voice-dna template in the guide, and continue. The pack still installs. Each skill will ask for three writing samples on its first run until the file exists.

## Step 3: Read the whole transcript

A two-hour talk is roughly 20,000 words. Read all of it, in order, in passes of about 400 lines. Do not sample. Do not skip the last third, the close is where most speakers put the rule they care about.

As you read, keep `analysis/notes.md` open and append evidence as you find it, one line per find, in this shape:

```
[1:12:04] FRAMEWORK  "the three things I look at are ..."
[0:08:30] NUMBER     "we went from 1.2 to 4 million in eleven months"
[0:41:10] RULE       "never discount, add instead"
[0:03:15] OPENER     "I'm going to show you the thing that ..."
[0:55:00] REPEAT     third time he comes back to pricing
```

Tags: FRAMEWORK, STEP, NUMBER, RULE, OPENER, TRANSITION, CLOSE, REPEAT, PHRASE, QUESTION (a question he asks and answers himself), STORY. Timestamps come from the transcript blocks, never from memory.

## Step 4: Write the analysis

Write `analysis/analysis.md` from the notes, following `${CLAUDE_SKILL_DIR}/analysis-spec.md` section by section. Read that file before writing. The rules that matter most:

- Every pattern claim carries a verbatim quote and a timestamp. No quote, no claim.
- Normalize obvious caption errors when quoting (a misheard brand name), never invent words.
- A framework is written as the steps he actually gives, in his words, in his order. If he gives three steps, there are three steps. Do not round up to five.
- Recurring topics are ranked by how many separate times he returns to them. Count the returns from your REPEAT notes.
- Practices to adopt are written as actions for the user's business, each tied to the quote it came from. Where the action depends on the user's context, write the question instead of guessing.
- No markdown tables. `- **Key:** Value` bullets. No em dashes. Absolute dates.
- Anything the transcript cannot support is TBD, with one line on what is missing.

Delete `notes.md` only if the user asks. It is the evidence trail.

## Step 5: Build the pack

Three templates live in `${CLAUDE_SKILL_DIR}/templates/`: `script.md`, `ideate.md`, `validate.md`. For each one:

1. Read the template.
2. Replace every placeholder: `{{NAME}}`, `{{SLUG}}`, `{{SOURCE}}` (title plus URL from meta.json), `{{ANALYSIS}}` (the absolute path to analysis.md), `{{VOICE}}` (the absolute path to the user's voice file, or `~/.claude/skills/voice-dna/SKILL.md` if it does not exist yet).
3. Replace every `<!-- FILL: ... -->` block with real material from analysis.md. Quotes keep their timestamps. The filled skill has to work on its own in a fresh session that has not read the analysis, so each one carries its own distilled engine, and points at analysis.md only for depth.
4. Write it to `~/.claude/skills/{{SLUG}}-script/SKILL.md`, `~/.claude/skills/{{SLUG}}-ideate/SKILL.md`, `~/.claude/skills/{{SLUG}}-validate/SKILL.md`. Create the folders. Never overwrite an existing pack without saying so first.

Keep each filled skill under 300 lines. If the engine section runs long, cut to the strongest evidence, not the most.

## Step 6: Verify and report

```
ls ~/.claude/skills/ | grep <slug>-
```

Claude Code picks up new skills in the current session. If `~/.claude/skills/` did not exist when the session started, tell the user to run `/reload-skills`.

Report in this shape, nothing else:

- **Source:** title, channel, length, transcript source and word count.
- **Analysis:** `analysis/analysis.md`, with counts: frameworks, numbered claims, stated rules, recurring topics, practices to adopt, TBDs.
- **Pack:** the three commands, one line each on what the first run does.
- **First runs:** one concrete prompt per command, written for this person. For example `/hormozi-ideate my business is a two-person design studio for dental practices`.
- **Open:** every TBD and every question the analysis left for the user.

## Quality rules

- Never fabricate a quote, a number, a timestamp, or a framework step. The transcript is the only source.
- Never write a summary of the talk in place of the analysis. If a section reads like a book report, rewrite it as evidence.
- Never put the person's signature phrases into the pack as lines for the user to say. They go in the avoid list.
- Never skip the voice file check. A pack that imitates the person instead of serving the user is the failure mode this skill exists to prevent.
- Never run on a transcript under 1,500 words without saying the material is thin. The pack still installs, marked thin in each description.
- Do not editorialize about the person. Describe what they do and how, not whether you agree.
