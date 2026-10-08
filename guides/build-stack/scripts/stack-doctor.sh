#!/usr/bin/env bash
# Usage: bash stack-doctor.sh
# Checks the local tools behind each layer of the build stack and prints the install step for anything missing.

set -u

ok=0
missing=0

check() {
  local label="$1" cmd="$2" version_cmd="$3" install="$4"
  if command -v "$cmd" >/dev/null 2>&1; then
    local v
    v=$(eval "$version_cmd" 2>/dev/null | head -1)
    printf "  OK       %-14s %s\n" "$label" "${v:-installed}"
    ok=$((ok + 1))
  else
    printf "  MISSING  %-14s %s\n" "$label" "$install"
    missing=$((missing + 1))
  fi
}

check_app() {
  local label="$1" path="$2" install="$3"
  if [ -d "$path" ]; then
    printf "  OK       %-14s %s\n" "$label" "$path"
    ok=$((ok + 1))
  else
    printf "  MISSING  %-14s %s\n" "$label" "$install"
    missing=$((missing + 1))
  fi
}

echo
echo "Build stack doctor"
echo

echo "02 Code"
check "node"        node        "node -v"                       "https://nodejs.org (22 or newer)"
check "pnpm"        pnpm        "pnpm -v"                       "npm install -g pnpm"
check "claude"      claude      "claude --version"              "npm install -g @anthropic-ai/claude-code"
check "codex"       codex       "codex --version"               "npm install -g @openai/codex (optional)"
echo

echo "04 Database"
check "docker"      docker      "docker --version"              "https://docs.docker.com/get-docker (self-hosting only)"
check "supabase"    supabase    "supabase --version"            "brew install supabase/tap/supabase (optional, local dev)"
check "psql"        psql        "psql --version"                "brew install libpq (optional)"
echo

echo "05 Automation"
check "n8n"         n8n         "n8n --version"                 "npx n8n (or use n8n Cloud, nothing to install)"
echo

echo "06 Source control"
check "git"         git         "git --version"                 "https://git-scm.com"
check "gh"          gh          "gh --version"                  "brew install gh, then gh auth login"
echo

echo "07 Deploy"
check "wrangler"    wrangler    "wrangler --version"            "npm install -g wrangler (or run via pnpm exec inside the project)"
echo

echo "09 Memory"
if [ "$(uname)" = "Darwin" ]; then
  check_app "Obsidian" "/Applications/Obsidian.app" "https://obsidian.md/download"
else
  check "obsidian"  obsidian    "echo installed"                "https://obsidian.md/download"
fi
echo

echo "10 Integrations"
check "composio"    composio    "composio --version"            "npm install -g @composio/cli (optional)"
echo

echo "Scripting"
check "python3"     python3     "python3 --version"             "https://www.python.org/downloads"
echo

echo "$ok found, $missing missing."
echo "Missing is fine. Install only the layers the project needs. The guide says which."
