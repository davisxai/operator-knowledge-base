# Resources

Open source projects and tools I actually run, plus the ones I evaluated properly and passed on. Nothing is on this list because it is popular.

Two rules for this section:

1. **Every entry gets a verdict, not a rating.** A verdict names the condition that would flip the decision. "Skyvern is overkill at this scale" is useful. "Skyvern is worse" would have been wrong.
2. **The rejections stay.** In every tooling scan I have run, the "deliberately not installed" list carried more decision value than the shortlist, because it encodes the boundary.

> [!NOTE]
> Version numbers, star counts, benchmark scores, and vendor pricing here are point-in-time snapshots from research passes between March and July 2026. The architectural patterns and operating rules have held. The numbers have not. Re-verify anything version-specific before you act on it.

## Index

- **[ai-and-agents.md](ai-and-agents.md)** AI coding tools, agent frameworks, and local inference engines.
- **[mcp-and-infra.md](mcp-and-infra.md)** MCP servers, knowledge and memory tools, automation and infrastructure.
- **[media-and-frontend.md](media-and-frontend.md)** Generation and media tools, image sourcing APIs, and the frontend stack.

## How I pick

- **Pick the category before you pick the tool.** Choosing the second-best tool inside the right category beats the best tool in the wrong one. This is the most common expensive mistake.
- **Measure token cost, not subscription price.** Side-by-side comparisons of the same task varied by 4x to 6x across tools. Headline pricing tells you close to nothing about cost per result.
- **Prefer the thing that already integrates.** A tool with an existing MCP server, n8n node, or documented REST API beats a better tool you have to wire up yourself.
- **Anything you re-run on a schedule has to survive drift.** One-shot automation can be brittle. Recurring automation cannot.
- **Documented ceilings are not practical ceilings.** A batch endpoint said 100 requests. The real number was 10. Find yours empirically.

## What "open source" means on this list

Licenses are noted where they change the decision. Two specific traps:

- **AGPL** matters the moment you resell a stack to a client. It is the reason an alternative stays on the bench even when the AGPL tool wins on merit.
- **Open weight is not open source.** Apache 2.0 or MIT means modify and redistribute freely. Open weight means you get the weights and the license may still restrict commercial or production use. Check before you build a client deliverable on a model.

---

Built by OperatorOS | [operatoros.ai](https://operatoros.ai)

Follow [@daviss.dev](https://instagram.com/daviss.dev) and [@os.operator](https://instagram.com/os.operator) on Instagram.
