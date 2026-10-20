---
name: reel-build
description: Build, review, and render a voiced reel as a HyperFrames composition where every animation is keyed to the exact word in the voiceover. Use when the user has script.json and a voice track and says "build the reel", "animate this", "make the scenes", "render it", or gives visual notes on a reel in progress. Runs the lint, check, snapshot, and render loop, and keeps the voice frozen until the visuals are approved.
---

# Reel build

You build the reel in `index.html` with HyperFrames and GSAP, review it with the user, and render it. Load the `hyperframes` skill first for the composition contract.

## Inputs

- `style.md` (from reel-teardown) for fonts, colors, pacing, motion.
- `assets/vo/vo.mp3` and `assets/vo/timing.json` (from `python3 scripts/build_vo.py`).
- The starter at `templates/starter/` if the project is new.

## Build

1. **One section per scene.** `<section class="clip" data-from="s03" data-to="s04">` names the first and last script line the scene covers. Run `python3 scripts/apply_timing.py` and it sets every window from the voice.
2. **Key every tween to a word.** `S("s03")` is when line s03 starts. `W("s03", 4)` is when its fifth word starts. Never hardcode seconds. When the voice changes, the whole reel re-times itself.
3. **One device carries the reel.** Pick the recurring element from `style.md` (a terminal, a phone, a step bar) and keep it consistent across scenes.
4. **Brand in variables.** Colors and fonts live in `:root`. A one-line change restyles every scene.
5. **Seek-safe motion only.** Finite repeats (`repeat: Math.max(0, Math.floor(window / cycle) - 1)`), no `Math.random` (use a seeded hash), never animate `.clip` itself, animate a child wrapper. Media sits directly under `#root`.
6. **Safe frame.** Content between y 450 and 1660 on a 1080 by 1920 frame. Keep keywords left of x 900 below y 1180.

## Review loop

1. `npx -y hyperframes lint` while editing. `npx -y hyperframes check` before any render. Zero errors.
2. `npx -y hyperframes snapshot --at 2,8,14,20 --no-end --output snaps` with one time per beat, read the contact sheet, and fix what you see before the user does.
3. Render a review cut: `npx -y hyperframes render --quality looks --fps 30 --output renders/review-v1.mp4`.
4. Take notes in plain English. Apply them, re-check, re-render the next version number.
5. **Do not re-voice during visual rounds.** Rewrite lines in `script.json` as you go, but regenerate the voice once, after the user says the visuals are done.

## Render

```bash
python3 scripts/build_vo.py          # once, after visuals are approved
python3 scripts/apply_timing.py
npx -y hyperframes check
npx -y hyperframes render --quality delivery --fps 60 --output renders/final-60fps.mp4
ffprobe -v error -show_entries stream=codec_type -of default=nw=1 renders/final-60fps.mp4
```

The last command must print both `video` and `audio`. Pull two or three frames with `ffmpeg -ss T -i file -frames:v 1 out.png` and look at them before calling it done.

## Rules

- Nothing holds the screen for under 2.5 seconds. `apply_timing.py` prints the offenders.
- Every frame is full. Real labels, real file names, real text. No grey placeholder bars.
- Each new reel gets new scene shapes. Do not reuse the last reel's layouts beat for beat.
