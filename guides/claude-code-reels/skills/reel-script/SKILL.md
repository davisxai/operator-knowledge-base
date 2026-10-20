---
name: reel-script
description: Write a short-form video script as script.json, one line per visual beat, ready to voice in ElevenLabs and time to the word. Use when the user says "write the script", "script this reel", "draft the voiceover", or has a topic and a style.md and wants the words. Enforces hook first, one idea per line, a 60 second cap, and a single CTA.
---

# Reel script

You write the words of a reel in the exact format `scripts/build_vo.py` reads. Every line you write becomes a scene, so write in beats, not paragraphs.

## Inputs

- The topic, and who it is for.
- `style.md` from the teardown, if one exists. Match its structure and pacing.
- The CTA keyword and what the viewer gets for commenting it.

## The format

```json
{
  "voice_id": "the user's ElevenLabs voice id",
  "model": "eleven_v4",
  "speed": 1.0,
  "segs": [
    ["s01", "The hook, one sentence."],
    ["s02", "The promise. Six steps."],
    ["h02", 0.9],
    ["s03", "One. The first step."]
  ]
}
```

- `["sNN", "text"]` is spoken. Keys run in order.
- `["hNN", seconds]` is silence. Put one after any line shorter than about 2.5 seconds that needs its own scene, and before the CTA if the last step needs room to land.

## Process

1. **Hook first.** The first line is a claim the viewer did not expect, said in under three seconds. No greeting, no "in this video".
2. **The promise.** Second line names the payoff and its size ("Six steps."). Hold it with a silence entry so the number can land.
3. **One line per beat.** Each step gets one or two lines. If a line needs two visuals, split it.
4. **Concrete nouns.** Name the tool, the file, the command. "Load HyperFrames" beats "install the right tool".
5. **One CTA.** The last line only. Keyword in quotes in the caption, spoken plainly in the script.
6. **Read it out loud.** Cut every word you would not say to a friend across the table.

## Rules

- Total under 60 seconds. At normal pace that is about 140 to 150 words.
- No statistics you cannot source. If a number is not real, drop the number and keep the claim.
- No line that only restates the visual. The voice and the screen should each carry something.
- Credit the people whose tools or ideas you are teaching, by name.
- Write `script.json` to the project root, then print the lines with an estimated duration for each so the user can check pacing before spending voice credits.
