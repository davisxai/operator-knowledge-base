# /video-to-skills

One long video in, three skills out. Reads the transcript a person folder holds, writes an evidence-based analysis of how that person teaches (frameworks, numbered claims, stated rules, what they keep coming back to, openers and closes, sentence shapes), then fills three skill templates with that material and installs them: `<name>-script`, `<name>-ideate`, `<name>-validate`. Every one of the three reads your own voice file first, so the output is their structure and your content.

The full workflow, from a YouTube URL to the installed pack, is in [guides/video-to-skills/](../../guides/video-to-skills/).

## Install

The skill has supporting files (the analysis spec and the three templates), so copy the folder, not just `SKILL.md`:

```bash
git clone https://github.com/davisxai/operator-knowledge-base.git
cp -r operator-knowledge-base/skills/video-to-skills ~/.claude/skills/
```

Or without cloning:

```bash
mkdir -p ~/.claude/skills/video-to-skills/templates
B=https://raw.githubusercontent.com/davisxai/operator-knowledge-base/main/skills/video-to-skills
curl -o ~/.claude/skills/video-to-skills/SKILL.md $B/SKILL.md
curl -o ~/.claude/skills/video-to-skills/analysis-spec.md $B/analysis-spec.md
curl -o ~/.claude/skills/video-to-skills/templates/script.md $B/templates/script.md
curl -o ~/.claude/skills/video-to-skills/templates/ideate.md $B/templates/ideate.md
curl -o ~/.claude/skills/video-to-skills/templates/validate.md $B/templates/validate.md
```

## Usage

After `pull.py` has filled `people/<name>/transcript/`:

```
/video-to-skills hormozi
```

It reads the whole transcript, writes `people/hormozi/analysis/analysis.md` (with `notes.md` as the evidence trail), and installs `hormozi-script`, `hormozi-ideate`, and `hormozi-validate` under `~/.claude/skills/`. The report lists the counts, the three commands, and a first prompt for each.

## Files

- **SKILL.md** the six steps: find the folder, find your voice file, read everything, write the analysis, fill the pack, verify.
- **analysis-spec.md** the eleven sections `analysis.md` has to contain, with the evidence rule for each.
- **templates/script.md** writes with their structure. Openers, skeleton, sentence shapes, closes, all quoted with timestamps, plus an avoid list of their signature phrases.
- **templates/ideate.md** maps what they keep coming back to onto your business, ranked by how often they returned to it.
- **templates/validate.md** checks a draft against the rules they state, their structural rules, their numbers (so you do not repeat one as yours), their phrases, and your own anti-voice list.

## Why it's built this way

The analysis is written before the pack, and the pack is filled from the analysis, never from the transcript directly. That is the only way the three skills stay consistent with each other and with the evidence. Every quote carries a timestamp so a wrong claim can be checked in thirty seconds. And the voice file check is Step 2, not an afterthought, because a pack that imitates the speaker instead of serving you is the failure this skill exists to prevent.

## Customize

The production version at OperatorOS runs the same analysis across a roster of creators and routes a topic to the strongest one. Start with one person. The skill does not care who it is: a keynote, a podcast episode, a course lecture, a sales call recording you have permission to study.
