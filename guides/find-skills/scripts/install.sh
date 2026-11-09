#!/usr/bin/env bash
# Installs find-skills by Vercel Labs into the current project. Pass -g for a global install.
set -e

if ! command -v node >/dev/null 2>&1; then
  echo "Node.js is required. Install it from https://nodejs.org and rerun."
  exit 1
fi

npx skills add vercel-labs/skills --skill find-skills -a claude-code -y "$@"

echo ""
echo "Verifying..."
if [ -e ".claude/skills/find-skills" ] || [ -e "$HOME/.claude/skills/find-skills" ]; then
  echo "find-skills is installed. Open Claude Code and ask: Find a skill for mobile app design."
else
  echo "Install finished but .claude/skills/find-skills was not found. Check the installer output above."
  exit 1
fi
