# REA on Your Own App

> Follow [@davis.mcm](https://instagram.com/davis.mcm) and [@operatoros](https://instagram.com/operatoros) on Instagram for more guides like this.

---

### One MCP server that opens the binary. Point it at software you own and ask how a feature works.

[REA, Reverse Engineer Anything](https://github.com/morluto/rea) connects a coding agent to real analysis engines. Ask Claude Code how a feature works in a compiled app and it opens the binary, traces the code, and hands back the evidence. I read the README, the installation guide, the CLI guide, the guided prompts, the process capture guide, and the disclaimer on October 13, 2026. This is how to install it, what to ask first, and how to read what comes back.

Every claim here comes from the repo's own docs. Nothing is estimated.

---

## What you'll get

→ What REA is, what it returns for each kind of target, and which engines it needs

→ The one-command install, what setup changes, and how to check it worked

→ Your first three questions, written for your own app, with the CLI equivalents

→ How to read the evidence it hands back, and the six guided prompts

→ Process behavior: running an app, watching what it does, and comparing two runs

→ The line the repo draws, in its own words

---

## Prerequisites

- Node.js 22.x (22.19 or newer), 24.x (24.11 or newer), or 26 and up, with npm. The docs list 23, 25, and prereleases as unsupported.
- A coding agent that speaks MCP. Setup configures Claude Code, Claude Desktop, Codex, Cursor, Gemini CLI, Windsurf, Devin, OpenCode, Antigravity, GitHub Copilot CLI, Command Code, Qwen Code, VS Code, Grok Build, OMP, Pi, Hermes, Qoder, Factory Droid, Trae, ZCode, and DeepSeek Harness.
- For native binaries, one analysis engine: Hopper, Ghidra, or IDA. Setup can install Hopper with your approval. JavaScript, Electron, and .NET analysis need no engine.
- An app you own or are authorized to examine. Start with your own.

---

## Contents

1. [What REA is](#1-what-rea-is)
2. [The install](#2-the-install)
3. [The engines](#3-the-engines)
4. [The 22 targets](#4-the-22-targets)
5. [Your first three questions](#5-your-first-three-questions)
6. [Reading the evidence](#6-reading-the-evidence)
7. [Process behavior](#7-process-behavior)
8. [Software you own](#8-software-you-own)
9. [Why this week](#9-why-this-week)
10. [Sources](#10-sources)

---

## 1. What REA is

The README's own line: "See a feature in an app that you want in your own product? Ask your agent to investigate it with REA. It can inspect the app without its source code, explain how the feature works, show the evidence, and build a version for your project."

Mechanically, it is a local MCP server plus a CLI. Your agent calls REA through MCP to inspect a target and trace the relevant code. REA returns findings with their evidence. The agent uses them to ask follow-up questions, explain the behavior, or write and test an implementation. The CLI runs the same workflows from your terminal.

Analysis runs on your machine. The README's FAQ is direct about data: "REA analyzes targets locally. Your agent receives the tool results, and its model provider has its own data policy."

**What comes back.** For native code, pseudocode and assembly. For JavaScript and Electron apps, modules and their relationships. Every result "includes the evidence and limitations behind each conclusion."

**License.** MIT for REA's own code. Third-party engines keep their own licenses.

---

## 2. The install

One command:

```bash
npx rea-agents setup
```

Setup walks you through it. In order, per the installation guide:

1. **Choose your agents.** A multi-select of the clients it detected. Existing REA registrations are selected by default. Newly detected clients are listed but not selected, so nothing gets added without you picking it.
2. **Review the plan.** Before it writes anything, setup lists the exact configuration paths it will touch, the skill destinations, any external software it proposes to install, and the package manager commands. Hopper is a separate choice with its own approval.
3. **Approve.** Declining or pressing Ctrl-C makes no changes. Agent configuration writes preserve unrelated entries, create a `.rea.backup`, replace the file atomically, and verify the result.
4. **Restart the agents it names.** The completion message lists which ones. Quit Claude Desktop fully before approving, because a running app can overwrite the registration.

What setup installs: REA's MCP server registration for each selected client, pinned to the exact version that ran setup, plus a bundled workflow skill with investigation instructions in each client's personal skill directory.

**Script it.** Explicit clients skip the interactive selection, and `--dry-run` returns the plan without applying it:

```bash
npx rea-agents setup --client claude_code --dry-run
```

**Check it.** `rea doctor` reads host prerequisites and agent configuration without changing anything:

```bash
npx -y rea-agents@latest doctor
```

**Update it.** The README says to keep it current because releases are frequent. For an agent setup done through npx, rerun setup on the latest release and review its plan:

```bash
npx rea-agents@latest setup
```

For a global install (`npm install --global rea-agents`), `rea update` installs the exact resolved release into the npm prefix that owns the running package. `rea uninstall` removes only REA's own registrations and skill files. It leaves Hopper, Node, evidence files, and other MCP servers alone.

---

## 3. The engines

REA does the orchestration. For native binaries, a decompiler does the reading.

- **Hopper.** Separate commercial software with a free demo that has vendor-defined limits, a paid license optional. On macOS, approved setup downloads the official DMG, checks its published size and digest, validates the bundle, and installs it to `~/Applications/Hopper Disassembler.app`, then opens it so you can pick demo mode or activate a license. REA starts Hopper when an operation needs it. Complete the demo or license prompt once in the same user session before your first operation.
- **Ghidra.** REA connects to an installation you already have. It accepts Ghidra 12.1.x with the 64-bit JDK that release declares (current releases want JDK 21 or newer) on Linux and macOS, with an experimental Windows path. Extract Ghidra and install the JDK yourself, then point REA at them with `GHIDRA_INSTALL_DIR`. The adapter exposes 25 read-only operations: inventory, names, search, decompilation, assembly, calls, typed references, cross-references, function dossiers, recovered data types, and memory reads.
- **IDA.** Your existing installation, through the IDA adapter in the docs, with an optional native MCP bridge.
- **JADX and JEB** cover Android APKs and JEB projects.

Static JavaScript, Electron, and .NET inspection need none of these. The README: "Static JavaScript analysis needs no native analysis engine."

Pick one explicitly when more than one could handle the target:

```bash
rea analyze /absolute/path/to/program --provider hopper
```

Or set `REA_ANALYSIS_PROVIDER` once as a standing preference. In MCP, pass `provider_id` to `open_binary`.

---

## 4. The 22 targets

The README's "What you can analyze" table lists 22 targets on October 13, 2026, each with what REA returns and what it needs. In the README's order:

- **Native binaries.** Pseudocode, assembly, strings, symbols, calls and references. Needs Hopper, Ghidra or IDA.
- **Offline ELF layout.** Sections, segments, original symbols and relocations, static mitigation candidates. Needs pwntools on Linux x64.
- **Go binaries.** Embedded compiler version, modules, replacements and build settings. Built in, no Go installation required.
- **WASM artifacts.** Validation, sections, import and export forms, decoded WAT. Needs WABT 1.0.42.
- **EVM bytecode.** Dispatch selectors, byte offsets, inferred arguments and mutability. Linux x64.
- **SQLite databases.** Tables, columns, indexes, views, triggers and selected rows. Node 24.15 or newer, or 26 and up.
- **Recorded Linux crashes.** Raw notes, every recorded thread's registers and signals, mapping candidates. pwntools on Linux x64, optional GDB.
- **JavaScript and Electron.** Modules, imports, source maps, routes, IPC and native add-on relationships. Node and npm only.
- **Websites.** Page structure, scripts, network observations and requested screenshots. A Chrome-family browser.
- **Saved network captures.** Requests, responses, exposed payloads and source locations. HAR or Fiddler SAZ files.
- **.NET assemblies.** Metadata, CIL instructions, declared native dependencies and build comparisons. Static only, nothing extra.
- **Android APKs.** Manifest declarations, classes, decompiled methods and references. Headless JADX and a full JDK.
- **Android devices.** Devices, packages, processes, logs, dumps, screen captures, and file transfers. adb.
- **JEB projects.** Engine-backed project units, artifact digests and pseudo-code. A JEB client serving MCP.
- **Android resources.** Decoded manifest, string tables, locales and version facts. Apktool.
- **Flutter apps.** Dart snapshot hash, per-ABI library digests and engine build provenance. Static APK parsing.
- **Firmware.** Regions, extraction results and native-analysis handoffs. Binwalk or Unblob on Linux.
- **Recorded packets.** Selected fields, repeated values, filters and decode-as rules. TShark 4.x on Linux.
- **Packet summaries.** Endpoints, DNS, TLS SNI, protocol distribution and HTTP requests. tshark and capinfos.
- **Recorded logic signals.** Decoder annotations, sample ranges and diagnostics. sigrok-cli on Linux.
- **Packages and resources.** File inventories, digests, plists, Apple bundle anatomy and extracted resources.
- **Process behavior.** Terminal output, interactions, exit and filesystem observations, and run comparisons. Linux or macOS with a native PTY.

Static inspection reads the files without running the app. Runtime capture runs or interacts with the target under your user permissions, and each runtime guide describes its effects.

---

## 5. Your first three questions

The README's example prompt is the template. It reads: "Understand how search works in the Notes app, show me the evidence, and build a similar feature for my project." Swap in your own app and the feature you want to understand.

Run these against something you shipped. Your own binary, your own Electron build, your own APK.

**Question one, the shape of the thing.**

```text
Open /absolute/path/to/MyApp.app and tell me what it is: the modules, the entry points, and the strings that look like feature names. Show me the evidence.
```

The CLI equivalent for a native target, after an engine is configured:

```bash
rea analyze /absolute/path/to/MyApp.app --provider ghidra --json
```

For an Electron app, point at the extracted directory or the ASAR. No engine needed:

```bash
npx -y rea-agents@latest analyze-javascript-application /absolute/path/to/app --json > app-evidence.json
```

The docs warn that the complete evidence for a real application can be hundreds of megabytes (a 334 MB Obsidian evidence file, in their example), so save it and project a summary:

```bash
jq -c '{source: {kind: "inline", evidence: .}, view: {kind: "summary"}}' app-evidence.json > app-view.json
rea inspect-analysis-view app-view.json
```

**Question two, one feature end to end.**

```text
Understand how search works in MyApp. Find the function that handles the query, show me its pseudocode and the functions it calls, and list what you could not confirm.
```

The CLI commands that back it:

```bash
rea search /absolute/path/to/program "search" --provider ghidra --json
rea function /absolute/path/to/program main --provider ghidra --json
rea decompile /absolute/path/to/program 0x1000 --provider ghidra --json
rea xrefs /absolute/path/to/program 0x1000 --provider ghidra --json
rea trace /absolute/path/to/program "search" --provider ghidra --json
```

`function` returns a function dossier. `decompile` returns pseudocode. `xrefs` returns the cross-references. `trace` follows a feature from a search term into the relevant functions. `rea instructions` gives the assembly alone.

**Question three, two versions of your own app.**

```text
Compare build 1.4 and build 1.5 of MyApp. What changed in the search path, and does the evidence support the changelog?
```

This is the `compare_application_versions` guided prompt. Open each target, then `inspect_artifact` returns the graph and findings together.

---

## 6. Reading the evidence

REA's results carry their evidence inline. The guided prompts ask the agent to keep three things distinct: observations, inferences, and unknowns. Read the result in that order.

- **Observations** are what the engine read: pseudocode, strings, symbols, calls, references, byte ranges, file offsets.
- **Inferences** are what the agent concluded from them. The README's wording: "results include the evidence and limitations behind each conclusion."
- **Unknowns** are what it could not confirm. REA tracks these as residual unknowns, and one of the six prompts exists only to audit them.

**The six guided prompts.** REA exposes them through MCP's `prompts` capability. They suggest starting points using current tool names and do not run anything by themselves.

- `investigate_feature` traces a feature from discovery into function evidence. For a JavaScript or Electron directory it points straight at `analyze_javascript_application` and needs no `open_binary`.
- `compare_application_versions` compares two shipped artifacts, with optional static and runtime follow-up.
- `verify_reconstruction` evaluates a reconstruction specification against retained comparison evidence.
- `trace_crash` correlates a crash symptom with static paths and optional process capture evidence.
- `audit_residual_unknowns` audits the current unknowns and what resolved them.
- `prepare_bounded_process_capture` designs a bounded process experiment before you run one.

Ask Claude Code for any of them by name, or let the bundled skill pick. The README's FAQ on what the skill does: "The skill supplies investigation instructions for your agent."

**One habit that pays.** The disclaimer says it plainly: "Decompilation, reconstruction, heuristics, and AI-assisted analysis may be incomplete or incorrect." Read the pseudocode the conclusion points at before you build on it. The evidence is in the result for exactly this reason.

---

## 7. Process behavior

The last target on the list is the one that watches an app run. Process capture "runs one caller-selected command and records bounded evidence about its terminal behavior, scheduled interactions, process lifetime, and selected filesystem state."

It needs Linux or macOS with a working native PTY. On macOS it also needs Apple's Swift compiler through `xcrun`, which REA uses to compile a small process-inspection helper into a private temporary directory each run. It installs nothing.

**A first capture.** Save this as `scenario.json`:

```json
{
  "executable": "node",
  "arguments": ["-e", "console.log('ready')"],
  "timeout_ms": 5000
}
```

Run it and save the evidence:

```sh
rea capture-process ./scenario.json --json > capture.json
```

The result holds the terminal observations, the exit and settlement status, and the cleanup outcome. Swap in your own app's executable, add the interactions you want scripted, and name the filesystem paths you want snapshotted.

**Compare two runs.** This is the use the docs are built around: an authority build against a reconstruction.

```sh
rea compare-process-captures authority.json reconstruction.json
```

The comparison checks terminal, interaction, exit, filesystem, and process observations under a shared contract and reports differences with their locations. Both captures need the same working directory and observation paths, or it names the fields that differ and stops.

Two sentences from the guide to keep in mind. "This is not a sandbox." And: the command "runs with the current user's permissions and inherits the host environment." Run captures on your own software, in an environment you would run that software in anyway.

---

## 8. Software you own

The README's disclaimer line, verbatim: "REA is for lawful research, education, interoperability, software preservation, and analysis of software you own or are authorized to examine."

The project's [DISCLAIMER.md](https://github.com/morluto/rea/blob/main/DISCLAIMER.md) lists what it will not help with, including copying proprietary software or reproducing its protected code and assets, and circumventing DRM or license checks. It also notes that reverse engineering may be restricted in your jurisdiction or by the license of the software you analyze, and that you must legally obtain Hopper, IDA, and JEB under their own licenses.

That is why this guide starts with your own app. Everything above works there, and the evidence is yours to use.

---

## 9. Why this week

On the All-In Podcast episode of October 10, 2026, Chamath Palihapitiya said that IP and software were "effectively rendered worthless" after open source developers published replacements for Adobe's core products, and that once services go headless and connect through MCP, the value of software IP goes away.

The replacements he meant are ArtCraft: seven Adobe applications rebuilt in Rust by one developer, Brandon Thomas, with Claude Opus 5.5, first commit September 30, 2026. Photocraft, VectorCraft, FilmCraft, LightCraft, EffectCraft, DesignCraft, PrintCraft. The coverage describes them as clean-room: no Adobe source, no decompilation. Chamath's word "decompiled" was loose.

REA is the tool that actually opens a binary. The point of this guide is that the first binary you open should be your own.

---

## 10. Sources

All read October 13, 2026.

- Repo: https://github.com/morluto/rea
- README: https://github.com/morluto/rea/blob/main/README.md
- Installation and setup: https://github.com/morluto/rea/blob/main/docs/installation.md
- CLI and evidence: https://github.com/morluto/rea/blob/main/docs/cli.md
- Guided MCP prompts: https://github.com/morluto/rea/blob/main/docs/mcp-prompts.md
- Process capture: https://github.com/morluto/rea/blob/main/docs/process-capture.md
- Disclaimer: https://github.com/morluto/rea/blob/main/DISCLAIMER.md
- Chamath on All-In, clip via Fireside Alpha: https://x.com/firesidealpha/status/2108761607857992104
- ArtCraft coverage: https://www.notebookcheck.net/Photoshop-Premiere-more-Experienced-Rust-developer-recreates-Adobe-suite-with-AI-assistance-as-open-source.1419230.0.html and https://www.phoronix.com/news/Photocraft-Filmcraft-AI
- Every quoted line in this guide comes from those pages. Star counts move daily, so this guide names none. The repo page has the current number.

---

Built by OperatorOS | [operatoros.ai](https://operatoros.ai)
Follow [@davis.mcm](https://instagram.com/davis.mcm) and [@operatoros](https://instagram.com/operatoros) for production-grade AI guides.
