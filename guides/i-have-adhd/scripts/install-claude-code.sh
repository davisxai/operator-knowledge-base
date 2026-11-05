#!/usr/bin/env bash
# Usage: bash install-claude-code.sh [--always]
# Installs the i-have-adhd plugin into Claude Code. --always turns on the SessionStart hook so every session starts in ADHD mode.
set -euo pipefail

if ! command -v claude >/dev/null 2>&1; then
  echo "Claude Code CLI not found. Install it first: https://docs.claude.com/en/docs/claude-code" >&2
  exit 1
fi

claude plugin marketplace add ayghri/i-have-adhd
claude plugin install i-have-adhd@i-have-adhd

if [[ "${1:-}" == "--always" ]]; then
  CONFIG_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
  touch "$CONFIG_DIR/.i-have-adhd-always"
  echo "Always-on enabled: $CONFIG_DIR/.i-have-adhd-always"
  echo "Remove that file to go back to on-demand."
else
  echo "Installed. Restart Claude Code, then type /i-have-adhd to turn it on."
fi
