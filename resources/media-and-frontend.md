# Generation, Media, and Frontend

The local-first content stack, where to source images programmatically, and the frontend tools I build interfaces with.

Back to [resources](README.md).

## Generation and media

**[ComfyUI](https://github.com/comfyanonymous/ComfyUI)** GPL-3.0
- Node-graph runtime for open-weight image and video models. Workflow JSON is scriptable.
- Install this first if you install anything. Every new open-weight model ships a ComfyUI node before it ships anywhere else, and an agent can submit a job over HTTP on port 8188 and poll for it. Apple Silicon MPS support is first class. Do not install a second image UI on top of it.

**[Kokoro TTS](https://github.com/hexgrad/kokoro)** Apache-2.0
- 82M parameter text-to-speech model. Roughly 100ms latency on an M4, ranked first on the TTS Arena leaderboard as of January 2026.
- The default voiceover engine. Near-zero marginal cost per generation, which removes the recurring hosted-TTS bill for anything that does not need a specific cloned voice. Wrong tool for cloning. Install is small: `brew install espeak-ng ffmpeg`, then `pip3 install kokoro soundfile`.

**[F5-TTS](https://github.com/SWivid/F5-TTS)**
- Flow-matching TTS with voice cloning.
- The escalation path from Kokoro, and only when cloning is genuinely the requirement. Deferred here because it has not been.

**[Speaches](https://github.com/speaches-ai/speaches)**
- Self-hosted OpenAI-compatible speech server. Transcription via faster-whisper, speech via Kokoro and Piper.
- Running here behind the voice endpoints of a dashboard. Use it when you want the OpenAI audio API shape without the OpenAI bill and without audio leaving your machine. Anything that talks to the OpenAI audio API works against it unchanged.

**[faster-whisper](https://github.com/SYSTRAN/faster-whisper)**
- CTranslate2 reimplementation of Whisper.
- The transcription engine under most self-hosted setups. Start with a small model and only size up when accuracy actually fails, not preemptively.

**[Remotion](https://www.remotion.dev)**
- Video rendered from React components.
- The pick when the video is programmatic and repeatable: data-driven scenes, templated overlays, hundreds of variants. Not the pick for anything needing an editor's frame-by-frame judgment.

**[Excalidraw](https://excalidraw.com)**
- Hand-drawn style diagramming with an open JSON file format.
- Because `.excalidraw` is JSON, an agent can generate a full diagram directly with no drawing step. Use it for content visuals and explanation, not for precise architecture documentation.

**[supoclip](https://github.com/FujiwaraChoki/supoclip)** AGPL-3.0
- Self-hosted long-video to vertical-shorts cutter with captions and virality scoring. Docker and go.
- Install it only when you actually have long-form footage to cut. It is not a standing install. AssemblyAI is a hard dependency for transcription at roughly $0.12 per hour of audio.

**[Postiz](https://github.com/gitroomhq/postiz-app)** AGPL-3.0
- Self-hosted social scheduling with a REST API, a Node SDK, and an n8n node. Posts to Instagram, TikTok, YouTube, LinkedIn, X, and around nine more.
- You hold the platform OAuth tokens, so there is no SaaS lock-in. Budget calendar time for platform app review, not money. AGPL is the reason to keep an alternative benched: if you ever resell the stack to a client where AGPL is a legal blocker, this is the piece you swap.

**[STORM](https://github.com/stanford-oval/storm)** MIT
- Research-to-draft pipeline. Planner, question-asker, and curator produce cited long-form research. Co-STORM adds a human-in-the-loop mode.
- Cited research is a much better input to short-form content than asking a model to write from memory. Roughly $0.50 per article with a GPT-4-class model plus a search API key.

**[yt-dlp](https://github.com/yt-dlp/yt-dlp)** and **[FFmpeg](https://ffmpeg.org)**
- Video download and media processing.
- Utilities, not standing installs. Install on demand. Together they are the front half of every "watch this video and tell me what is in it" workflow: download, extract scaled frames, pull captions, hand it all to a model.

### Passed on

- **[Mixpost](https://mixpost.app)** Loses to Postiz on community size, platform coverage, and API depth. Revisit only if AGPL blocks a resale scenario.
- **Other image UIs** (InvokeAI, SwarmUI, Fooocus, AUTOMATIC1111) ComfyUI covers the same ground and has the only live node library for 2026-era models. A second image UI is pure overhead.
- **Separate video model installs** (Hunyuan Video, LTX-Video, Mochi) Already available inside ComfyUI via custom nodes. No separate install needed.
- **Music generation** (MusicGen, Stable Audio Open) Trivially added later as a Python package when a specific piece needs it. Not worth a standing install.
- **Short-video generators** (MoneyPrinterTurbo, ShortGPT) Useful as reference implementations. Do not ship either in production. A Remotion plus agent-orchestration stack does the job better.
- **ViralCutter** Windows only. Skipped outright.

> [!TIP]
> Order installs by payoff per hour, not by pipeline order. The sequence that worked: ComfyUI first because it has the biggest payoff and the longest install, Kokoro second because it is a tiny install with an instant win, then Playwright MCP, then Stagehand on top of it, then Postiz on a server rather than locally so staging is fast, then STORM, then a clipper on demand. Total steady-state paid dependency for that stack came in under $100 a month including model spend. Everything else is local or free OAuth.

## Image sourcing APIs

**[Unsplash API](https://unsplash.com/developers)**
- Free curated photography with a real API. 50 requests per hour on demo, 5,000 per hour in production after approval.
- The clear winner on baseline aesthetic quality among free tiers. Hotlinking and attribution are mandatory, so design the UI around that constraint before you build.

**[Lummi](https://www.lummi.ai)**
- AI-generated stock that is human-curated before publishing.
- The curation is the whole point: it removes the uncanny AI look that makes generated stock unusable. Library is small at roughly 20K images, 10 requests per minute standard, attribution with clickable links required.

**[The Met Collection API](https://metmuseum.github.io)** and **[Art Institute of Chicago API](https://api.artic.edu/docs)**
- Museum open-access APIs. Neither requires authentication.
- The underrated win. Combined they expose over a million high-resolution public domain objects at zero cost. For editorial, fine art, and classical aesthetics this beats paid stock outright. Wrong source for modern lifestyle imagery.

**[Are.na](https://www.are.na/developers)**
- Curation platform with a documented API.
- The closest thing to programmatic access to genuinely curated visual content. Content is user-curated rather than licensed, so copyright falls back to the original image. Use it for reference and mood, not for publishing.

**[FLUX](https://blackforestlabs.ai)** and **[Ideogram](https://ideogram.ai)**
- Image generation APIs.
- FLUX is the general-purpose pick on the combination of documentation, access, and output quality. Reach for Ideogram specifically when the image has to carry legible typography.

### Passed on

- **Behance API** Listed as undergoing technical migration since 2021 with no return date. Effectively dead.
- **Pinterest API** Built for advertisers and publishers, not image sourcing.
- **Cosmos.so, Savee.it** No public API at all.
- **Adobe Stock API** Restricted to enterprise customers and affiliates since November 2024. Real access barrier.
- **Midjourney** Highest ceiling, enterprise-only API access. Third-party wrappers violate their terms and risk account bans, so there is no safe workaround.
- **Pixabay, Openverse** Require too much filtering to be worth automating.

> [!NOTE]
> No aggregator API exists for curated aesthetic content. The practical answer is a thin multi-source wrapper. Unsplash plus Lummi plus a museum API plus one generator covers curated photography, curated AI stock, fine art, and on-demand generation. The stock and museum sources cost nothing.

## Frontend and UI

**[Next.js](https://nextjs.org)**
- React framework with the App Router and standalone output.
- Default for both marketing sites and internal dashboards here. Standalone output plus a container is what makes it deployable to a plain VPS instead of only a hosted platform.

**[Tailwind CSS](https://tailwindcss.com)**
- Utility-first CSS.
- Default styling layer. Worth knowing before you start: v3 arbitrary values do not translate to v4 tokens for free. Migrating a component library across that boundary means touching every class list, so pick the version before you write two hundred components.

**[shadcn/ui](https://ui.shadcn.com)**
- Copy-in React components built on Radix and Tailwind.
- The only component source in this setup. You own the code after install, which is the point and also the tradeoff: it is not a dependency you upgrade. Treat every component as yours from the moment it lands.

**[Radix UI](https://www.radix-ui.com)**
- Unstyled accessible primitives.
- What sits underneath shadcn. Reach for it directly when you need a primitive the registry does not carry. Never hand-roll a dialog, a popover, or a select.

**[Motion](https://motion.dev)**
- Animation library for React, formerly Framer Motion.
- Pick one shared easing curve for the entire product and use it everywhere, or your interface will feel like three different products. Respect reduced-motion globally and opt decorative elements out explicitly, rather than disabling motion component by component.

**[Zustand](https://github.com/pmndrs/zustand)**
- Small state store with selector subscriptions.
- Right size for a dashboard with one large store. Push server state in over server-sent events rather than polling REST, and keep the URL and the store in sync through one function so they cannot drift apart.

**[TanStack Query](https://tanstack.com/query) and [TanStack Table](https://tanstack.com/table)**
- Server state caching, and headless table logic.
- Query for anything fetched. Table when you need sorting, filtering, and virtualization without inheriting somebody else's design opinions.

**[Lucide](https://lucide.dev)**
- Icon set with a React package.
- The icon layer here, and the reason no emoji ever ships in a UI. Consistent stroke weight across several hundred icons is worth more than variety.

**[Recharts](https://recharts.org)**
- Composable React charts.
- Fine for dashboard analytics: cost by model, tokens by agent, usage over time. Not the pick for dense or unusual visualizations where you would end up fighting it.

**[React Flow](https://reactflow.dev)**
- Node-and-edge graph editor for React.
- The pick for pipeline builders and anything the user drags, connects, or edits. Not for large read-only graphs.

**[Reagraph](https://reagraph.dev)**
- WebGL network graph visualization for React, 2D and 3D, with clustering.
- The pick for large read-only knowledge graphs where React Flow would choke. Rendering is WebGL, so debugging looks nothing like normal DOM work.

**[Xterm.js](https://xtermjs.org)**
- Terminal emulator in the browser.
- Pair it with node-pty on the server when you want a real shell in a web UI. Import it dynamically. It is heavy and it needs a DOM, so it will break a server render.

---

Built by OperatorOS | [operatoros.ai](https://operatoros.ai)

Follow [@daviss.dev](https://instagram.com/daviss.dev) and [@os.operator](https://instagram.com/os.operator) on Instagram.
