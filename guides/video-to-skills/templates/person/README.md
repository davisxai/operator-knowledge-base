# One folder per person

`pull.py` creates this layout for you. Copy it by hand only if you are adding a transcript you already have.

```
people/
    <name>/
        raw/            the talk as downloaded (audio by default, video with --video), or SOURCE.txt pointing at a local file
        transcript/     transcript.md (timestamped blocks), segments.json (every cue), meta.json (title, channel, URL, length, source, word count)
        analysis/       analysis.md and notes.md, written by /video-to-skills
```

The skills the pack generates do not live here. They install to `~/.claude/skills/<name>-script/`, `<name>-ideate/`, and `<name>-validate/`, so they work from any project.

Your own voice file lives outside every person folder, at `~/.claude/skills/voice-dna/SKILL.md`. One copy. Every pack reads it.

## Adding a transcript you already have

Put it at `people/<name>/transcript/transcript.md`. Timestamps in square brackets at the start of each block help the analysis cite its evidence, but the skill runs without them. Then:

```
/video-to-skills <name>
```
