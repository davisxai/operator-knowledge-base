# The one-line prompts

One line per repo. Paste it into Claude Code after the install line above it. Swap the words in brackets for your own.

Every prompt assumes Claude Code is open in an empty folder made for the piece. Claude writes the code, renders frames in a headless browser, and encodes an MP4 with FFmpeg. Nothing here calls a video model.

---

## lemo-opuscar

Install first:

```bash
claude plugin marketplace add lemomo-ai/lemo-opuscar
claude plugin install lemo-opuscar@lemolab
```

Prompt:

```text
Make a 40-second film in the isometric infographic style about [how my product works]. Calm male narrator. Show me the storyboard first.
```

Not sure which style:

```text
/lemo-opuscar:lemo-opuscar
```

---

## awesome-opus5-5-videos and opus-video-prompts

No install. Open a prompt file in the repo, copy the block under Prompt, then:

```text
Render this as a single HTML file in this folder, every frame drawn by code, no video model. When it is done, tell me how to record it.

[paste the prompt block here]
```

---

## three.js

No install for a single HTML file. Copy `one-file-scene.html` from this folder into your project, then:

```text
Read one-file-scene.html. Keep the import map, the bloom pass, and the ?t= frame control. Replace the bars with [a product shot of my app, floating in a dark studio, slow camera orbit]. Add a chrome ground plane so it reflects.
```

---

## mcp-for-blender

Install first:

```bash
claude mcp add blender uvx mcp-for-blender
uvx mcp-for-blender setup
```

Open Blender, restart Claude Code, then:

```text
In Blender, build [a solar panel on a tilted roof], add materials and a three-point light rig, frame it with a 50mm camera, and render a 1920x1080 still to renders/panel.png.
```

---

## react-three-rapier

Install in a React project:

```bash
npm install three @react-three/fiber @react-three/rapier
```

Prompt:

```text
Build a Galton board with @react-three/rapier: 12 rows of pins, 560 balls dropped one at a time, bins at the bottom. Label the bins with counts as the balls land. The result should settle into a bell curve on its own.
```

---

## react-postprocessing

Install in a React project:

```bash
npm install @react-three/postprocessing
```

Prompt:

```text
Add an EffectComposer to this scene with Bloom, DepthOfField, Noise and Vignette. Keep every effect off by default and expose a flag for each, so I can turn them on one at a time and compare.
```

---

## pixelfx

Install first:

```bash
claude plugin marketplace add patch-gg/pixelfx
claude plugin install pixelfx@pixelfx
```

Prompt:

```text
Make a 12-second loop in pixelfx: a campfire at night with fireflies, light rain starting at second six, lightning at second nine. Render it as an MP4.
```

Export for a game engine instead:

```text
Export the fire and weather categories as sprite sheets for Godot.
```

---

## ClaudeAnimationBase

Install first:

```bash
git clone --depth=1 https://github.com/JohnHeibel/ClaudeAnimationBase.git
cd ClaudeAnimationBase && npm install && claude
```

Prompt (the repo's own, with your subject):

```text
Read ANIMATION_GUIDE.md, then make a 15-second video of Clawd [explaining what a webhook is to a confused friend]. Storyboard first.
```

---

## librosa

Install first:

```bash
pip3 install librosa
```

Prompt:

```text
Write beats.py: load track.mp3 with librosa, run beat_track and onset_detect, and write beats.json with every beat time in seconds and the BPM. Then update index.html so every scene change lands on the nearest beat.
```

---

## video-shotcraft

Install first:

```bash
git clone --depth=1 https://github.com/Vincentwei1021/video-shotcraft.git
ln -sfn "$(pwd)/video-shotcraft" ~/.claude/skills/video-shotcraft
```

Prompt (the repo's own):

```text
Use video-shotcraft to make a promo for my product.
```

Pick the shots yourself:

```text
Use the spotlight-hero-card and exploded-view shot cards to present [the dashboard page].
```

---

Built by OperatorOS | operatoros.ai
