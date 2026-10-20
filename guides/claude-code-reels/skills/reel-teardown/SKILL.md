---
name: reel-teardown
description: Tear apart reference reels and write the style down as a file Claude can build from. Use when the user drops in reels, shorts, or TikToks they like and says "study these", "tear these apart", "what makes these work", "match this style", or "write down the style". Runs the watch skill on each video, measures what is on screen instead of guessing, and writes style.md.
---

# Reel teardown

You turn a few reference videos into one `style.md` that every later build reads. The point is to copy how a reel is built, never what it says.

## Before you start

- The watch skill must be installed (`/plugin marketplace add bradautomates/claude-video`, then `/plugin install watch@claude-video`). If `/watch` is missing, stop and tell the user the two commands.
- Ask for two to five references. One video is a sample, not a style.

## Process

1. **Watch every reference.** Run `/watch <path or url>` on each one. For anything under 60 seconds, let it auto-scale the frames. If a section matters (the hook, the CTA), run it again with `--start` and `--end` for denser frames.
2. **Read every frame it lists.** Do not summarize from the transcript alone. Most of what makes a reel work is on screen and never said.
3. **Measure, then write.** For each reference, note:
   - **Format:** aspect ratio, length, where text sits relative to the Instagram safe frame (top 245px and bottom 225px are covered on a 1920px tall frame, and the right 160px from y 1180 down).
   - **Structure:** the beat map. One row per beat: timestamp, what is said, what is on screen. Mark the hook, the promise ("only N steps"), each step, the save or follow beat, and the CTA.
   - **Pacing:** the average time between visual changes, the shortest beat, the longest hold. Count from the frame timestamps.
   - **Typography:** families (serif, sans, mono), sizes relative to the frame, how many words per title, what gets emphasized and how (color, italic, weight).
   - **Color:** background, text, accent, and what the accent is used for.
   - **Motion:** how text enters (rise, type, pop, blur in), how scenes change (cut, push, slide), what loops (cursors, waveforms, floating logos).
   - **Recurring elements:** the device that carries the whole reel. A terminal, a phone, a progress bar, a numbered step bar.
   - **Audio:** voiceover or not, music under it, captions verbatim or key phrases only.
   - **CTA:** the exact mechanic (comment a keyword, save, follow) and how it is staged.
4. **Write `style.md`** in the project root with the sections in `templates/style.md` from the guide. Put the shared patterns first, then a short note per reference on what only that one does.
5. **Write the borrow and avoid list.** Borrow: structure, pacing, the kind of device, the CTA mechanic. Avoid: their words, their exact layouts, their assets, their logos. The new reel has to be yours.

## Rules

- Every claim in `style.md` comes from a frame or a timestamp. If you did not see it, do not write it.
- Numbers over adjectives. "New beat every 2.5 seconds" beats "fast paced".
- Keep `style.md` under 120 lines. It is read before every build.
- Tell the user the three things that make the references work, in plain words, after the file is written.
