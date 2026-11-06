// Usage: VAULT_PATH=~/path/to/vault ANTHROPIC_API_KEY=... npx tsx operator.mts "list out all my offers"
// A read-only Operator: the Claude Agent SDK with three vault tools, answering from your own files.
// Needs: npm install @anthropic-ai/claude-agent-sdk zod tsx
import { readFileSync, readdirSync, statSync } from "node:fs";
import { join, relative, resolve, sep } from "node:path";
import { createSdkMcpServer, query, tool } from "@anthropic-ai/claude-agent-sdk";
import { z } from "zod";

const VAULT = resolve(process.env.VAULT_PATH ?? ".");
const SKIP = new Set([".obsidian", ".git", ".claude", "node_modules"]);

function walk(dir: string): string[] {
  return readdirSync(dir).flatMap((name) => {
    if (SKIP.has(name)) return [];
    const full = join(dir, name);
    if (statSync(full).isDirectory()) return walk(full);
    return name.endsWith(".md") ? [relative(VAULT, full)] : [];
  });
}

function safePath(rel: string): string | null {
  const full = resolve(VAULT, rel);
  return full.startsWith(VAULT + sep) ? full : null;
}

function text(t: string) {
  return { content: [{ type: "text" as const, text: t }] };
}

const vaultSearch = tool(
  "vault_search",
  "Search the vault by keyword. Call this first when the user asks about a person, company, offer, or topic and you do not know the exact page path. Returns paths ranked by matches.",
  {
    query: z.string().describe("Keywords, e.g. a name or topic."),
    limit: z.number().optional().describe("Max results, default 8."),
  },
  async ({ query: q, limit }) => {
    const terms = q.toLowerCase().split(/\s+/).filter(Boolean);
    const hits = walk(VAULT)
      .map((path) => {
        const body = readFileSync(join(VAULT, path), "utf8").toLowerCase();
        const name = path.toLowerCase();
        const score = terms.reduce(
          (s, t) => s + (name.includes(t) ? 50 : 0) + body.split(t).length - 1,
          0,
        );
        return { path, score };
      })
      .filter((h) => h.score > 0)
      .sort((a, b) => b.score - a.score)
      .slice(0, limit ?? 8);
    return text(hits.length ? JSON.stringify(hits, null, 2) : `No pages match "${q}".`);
  },
);

const vaultRead = tool(
  "vault_read",
  "Read a vault page by relative path, e.g. hot.md or wiki/concepts/offers.md. Start with hot.md and index.md, then drill into specific pages.",
  { path: z.string().describe("Relative vault path.") },
  async ({ path }) => {
    const full = safePath(path);
    try {
      if (!full) throw new Error("outside vault");
      return text(readFileSync(full, "utf8"));
    } catch {
      return text(`No page at "${path}". Use vault_search or vault_list to find the right path.`);
    }
  },
);

const vaultList = tool(
  "vault_list",
  "List every page in the vault, optionally only those under one folder, e.g. wiki/people.",
  { folder: z.string().optional().describe("Folder prefix to filter by.") },
  async ({ folder }) => {
    const all = walk(VAULT).filter((p) => !folder || p.startsWith(folder));
    return text(all.join("\n"));
  },
);

const SYSTEM = `You are Operator, the AI operating system for the business whose vault you can read.
Lead with the answer. Short sentences. No filler.

Retrieval order, every time:
1. vault_read hot.md for current state.
2. vault_read index.md to find the right pages.
3. vault_read the specific pages. Use vault_search when you do not know the page name.

Do not answer from memory when the vault has the answer. Cite every page you used as a [[wikilink]] by file name.
If the vault does not know, say so. The vault is read only. You cannot edit files or send anything.`;

const prompt = process.argv.slice(2).join(" ") || "What is going on in the business right now?";

for await (const message of query({
  prompt,
  options: {
    model: process.env.OPERATOR_MODEL ?? "claude-opus-4-8",
    systemPrompt: SYSTEM,
    cwd: VAULT,
    settingSources: [],
    mcpServers: {
      vault: createSdkMcpServer({ name: "vault", version: "1.0.0", tools: [vaultSearch, vaultRead, vaultList] }),
    },
    allowedTools: ["mcp__vault__vault_search", "mcp__vault__vault_read", "mcp__vault__vault_list"],
    disallowedTools: ["Write", "Edit", "Bash", "WebFetch", "WebSearch"],
  },
})) {
  if (message.type === "assistant") {
    for (const block of message.message.content) {
      if (block.type === "tool_use") console.log(`> ${block.name} ${JSON.stringify(block.input)}`);
    }
  }
  if (message.type === "result" && message.subtype === "success") console.log(`\n${message.result}`);
}
