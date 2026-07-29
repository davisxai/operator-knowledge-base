# AI Coding and Agents

Coding agents, agent frameworks, and local inference engines. Verdicts come from two research passes plus daily use.

Back to [resources](README.md).

## The category thesis

The market fractured into four categories with a different leader in each. There is no single winner. As of mid-2026 the dominant pattern among senior engineers was multi-tool: an IDE-bound editor, plus a terminal-native agent, plus a cloud background runner.

```
  IDE editor          Cursor          you drive, it accelerates
  terminal agent      Claude Code     you delegate, it executes
  background runner   Codex           you review after the fact
  open source         Aider, Continue you own the whole loop
```

Two things held across both passes. MCP support is table stakes now, not a differentiator: tools without it are visibly behind. And context window became a real moat, because 1M tokens versus a practical 70k to 120k is decisive on monorepo reasoning.

## AI coding tools

**[Claude Code](https://claude.com/claude-code)**
- Terminal-native coding agent with skills, subagents, hooks, and MCP.
- The daily driver here, and the highest capability ceiling for deep engineering work. Wrong pick if you want visual diff review on every inline edit, or if model portability matters to you.

**[Cursor](https://cursor.com)**
- IDE built around inline Tab completion and visual diff review.
- The category benchmark for accelerating a human who is still driving. Weak on large refactors: practical context measured around 70k to 120k tokens in the 2026-06 pass, versus roughly 1M for terminal agents. Independent testing in that same pass put token consumption at roughly 5.5x Claude Code on identical tasks.

**[OpenAI Codex](https://github.com/openai/codex)**
- Coding agent built to run unattended in a cloud sandbox for hours or days.
- The pick when you want to review finished work instead of driving keystrokes. Tightest GitHub integration of the three leaders and the most mature sandbox security model. Weaker offline and air-gapped story, and less flexible for heavily customized team workflows.

**[Aider](https://aider.chat)**
- Git-first CLI pair programmer with an architect/editor model split and a tree-sitter repo map.
- Lowest hallucination rate in the category for refactors, and every AI edit auto-commits with a real message. Not the pick when you need the agent to run tests, debug failures, or chain multi-step fixes without you driving.

**[Continue](https://continue.dev)**
- Apache 2.0 IDE extension. True bring-your-own-model, self-hostable, inspectable.
- The pick for JetBrains, air-gapped work, or source-controlled AI quality gates: `.continue/checks/` markdown files run as GitHub status checks. Rougher than a purpose-built IDE, and multi-file coordination is weaker.

**[OpenCode](https://github.com/opencode-ai/opencode)**
- MIT Go TUI coding agent. 75+ model providers, LSP integration, SQLite session persistence.
- The one to watch. Less polished agentic execution than the leaders, but provider-agnostic is the right long bet: when model quality converges, the tool that lets you swap models freely wins.

**[Gemini CLI](https://github.com/google-gemini/gemini-cli)**
- Open source terminal agent with Google Search grounding and GitHub Actions integration for issue triage and PR review.
- Free with a personal Google account, and free is a price point that beats features for casual use. The rate-limited free tier interrupts heavy sessions.

**[Goose](https://github.com/block/goose)**
- Free Rust agent, MCP-first, with a recipes system for repeatable workflows and a background serve mode. Now under Linux Foundation governance.
- Good neutral infrastructure rather than a competing product. It is a jack of all trades, so code quality depends entirely on which model you bring. Not a quality floor.

**[Cline](https://github.com/cline/cline)**
- Coding agent across VS Code, Cursor, JetBrains, Zed, Neovim, and CLI, with per-step permission approval and browser automation.
- Strong if you want an IDE-first agent that asks before each step. CLI mode is newer and less mature than the terminal-native tools.

### Passed on

- **[Amazon Q Developer CLI](https://aws.amazon.com/q/developer/)** AWS-centric, low adoption, transitioning to a closed-source successor. Uncertain future. Revisit only if your whole stack is AWS and the successor lands well.

> [!WARNING]
> Roughly 43% of AI-authored changes across Codex, Claude, and Cursor required debugging in the 2026-06 research pass. The overhead is real regardless of which tool you pick. Budget review time, not just generation time.

## Agent frameworks

**[Claude Agent SDK](https://github.com/anthropics/claude-agent-sdk-typescript)**
- The Claude Code runtime as a library. In-process MCP servers, explicit tool allowlists, session resume, streaming.
- Use it when you want a Claude-shaped agent inside your own app with a tool surface you control by name. Not a multi-provider framework, so model portability is zero.

**[Mastra](https://mastra.ai)**
- TypeScript agent framework with tools, workflows, pluggable storage, and observability built in.
- Running in production here on an email agent. Good when you want a TypeScript-native agent service with real persistence. Its bundled output does not reliably load dotenv, so pass env explicitly through your process manager config.

**[LangGraph](https://github.com/langchain-ai/langgraph)**
- Graph-based state machines for agents. Nodes are functions, edges are conditional transitions.
- The most flexible control flow available, with durable execution, automatic resume from failure, and human-in-the-loop at any node. Overkill for a linear task a plain agent loop already handles.

**[CrewAI](https://github.com/crewAIInc/crewAI)**
- Role-based multi-agent orchestration. Roles, goals, backstories. Native MCP and A2A.
- Read the examples repo and port the planner/writer/editor structure into your own agents. Treat a runtime dependency as optional. The pattern is the asset, not the framework, and its ease of adoption is exactly why it gets over-adopted.

**[Microsoft Agent Framework](https://github.com/microsoft/agent-framework)**
- AutoGen and Semantic Kernel merged into one framework. v1.0 shipped 2026-04-07.
- The enterprise consolidation signal, and the right starting point on .NET or Python in a Microsoft shop. Start here instead of AutoGen.

**[smolagents](https://github.com/huggingface/smolagents)**
- Minimal agent library built on the CodeAgent pattern: the agent writes executable code instead of emitting JSON tool calls.
- Worth reading for the pattern on open-ended tasks. Not the choice when you need constrained, auditable, replayable tool calls.

**[Composio](https://composio.dev)**
- 1,000+ pre-built tool integrations with managed auth.
- Solves the last-mile problem of connecting an agent to real SaaS accounts, which is where agent projects usually die. Skip it when the two or three apps you need already have their own MCP servers.

### Passed on

- **[OpenAI Swarm](https://github.com/openai/swarm)** Educational only, superseded by the OpenAI Agents SDK. Do not start new projects on it.
- **[AutoGen](https://github.com/microsoft/autogen)** Maintenance mode, no new features. Use Microsoft Agent Framework, or the AG2 community fork if you need the original shape.

> [!NOTE]
> Honest self-assessment on where a terminal agent with subagents and skills is behind a real framework: formal multi-agent patterns (graph routing, hierarchical teams, group chat) are more sophisticated in LangGraph and CrewAI, visual workflow debugging does not exist in a terminal, and enterprise cloud deployment is more do-it-yourself. Graph-based orchestration is winning. Code-first is displacing config-first.

## Local inference

**[Ollama](https://ollama.com)** MIT
- Local model runner with an OpenAI-compatible REST API.
- Fastest path from nothing to a running local model, under five minutes. Single-user by design: no batching, and throughput collapses under concurrency. Never put it behind a production endpoint.

**[LM Studio](https://lmstudio.ai)**
- Same tier as Ollama, with a GUI for browsing and testing models.
- Use it when you want to compare models visually before committing. Same concurrency ceiling.

**[vLLM](https://github.com/vllm-project/vllm)**
- Production inference server. The default for serving open-weight models.
- Start here for anything multi-user. This is the boring correct answer.

**[SGLang](https://github.com/sgl-project/sglang)**
- Production inference server tuned for shared-prefix workloads.
- Benchmark it against vLLM before defaulting, especially for RAG, agents, and chatbots. The 2026-04 pass cited roughly a 29% throughput advantage on shared-context work. If your workload reuses long prefixes, this is worth an afternoon.

### Where open models actually stand

Snapshot from 2026-04. Re-verify before you act on it.

**At parity**
- **Raw code generation:** Qwen 2.5 Coder 32B at 88.4% HumanEval, DeepSeek Coder V2 at 90.2%.
- **Context length:** 128K is standard across Qwen, DeepSeek, and Yi-Coder. Codestral at 256K.

**Gap still holds**
- **Agentic coding:** best open models 73% to 78% on SWE-bench Verified against low-to-mid 80s for frontier closed models at the same date. SWE-bench tests real multi-file bug fixing, which is where cross-file reasoning shows up.
- **Instruction following:** noticeably weaker against a written style guide.
- **Tool-calling reliability:** weaker, and less likely to ask a clarifying question on an ambiguous request.

**Open wins outright**
- Fine-tuning on a proprietary codebase.
- Fully air-gapped deployment.
- Latency control for autocomplete-class work, and cost at very high token volume.

The pragmatic architecture is hybrid. Frontier API model for planning, multi-file reasoning, and complex agentic work. Local Qwen-class model for high-volume completion, boilerplate, and test scaffolding where latency or per-token cost dominates. Roughly 60% of coding tasks do not need frontier reasoning.

The same logic applies inside a single agent setup. Route exploration to a cheap model and reserve the expensive one for the edits. The Aider polyglot benchmark cost spread is the clearest illustration: the same 225-exercise suite ran at $1.30 on DeepSeek V3.2, $29.08 on GPT-5 high, and $146.32 on o3-pro high.

---

Built by OperatorOS | [operatoros.ai](https://operatoros.ai)

Follow [@daviss.dev](https://instagram.com/daviss.dev) and [@os.operator](https://instagram.com/os.operator) on Instagram.
