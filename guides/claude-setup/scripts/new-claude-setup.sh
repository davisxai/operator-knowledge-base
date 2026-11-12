#!/usr/bin/env bash
# Usage: scripts/new-claude-setup.sh [/absolute/path/to/folder]   (default: ~/claude-setup)
# Copies the five templates and the instructions into a folder of your own,
# stamps today's date into corrections.md, and starts git history if git is installed.
set -euo pipefail

TARGET="${1:-$HOME/claude-setup}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$HERE/../templates"
TODAY="$(date +%Y-%m-%d)"

if [ -e "$TARGET" ]; then
  echo "Refusing to overwrite: $TARGET already exists" >&2
  exit 1
fi

mkdir -p "$TARGET"
cp "$SRC"/*.md "$TARGET"/

# The first entry in corrections.md carries today's date. The .bak dance keeps sed portable across macOS and Linux.
sed -i.bak "s/YYYY-MM-DD/$TODAY/g" "$TARGET/corrections.md"
rm -f "$TARGET/corrections.md.bak"

if command -v git >/dev/null 2>&1; then
  ( cd "$TARGET" && git init -q && git add -A && git commit -q -m "Create the Claude setup folder from the guide" )
  echo "Folder created at $TARGET with git history."
else
  echo "Folder created at $TARGET. Install git later if you want a history of your edits."
fi

echo
echo "Next:"
echo "  1. Open the Claude desktop app. Create a project. Name it after your business."
echo "  2. Paste project-instructions.md into the project's Instructions. Replace the two bracketed names."
echo "  3. Add the five files to the project's Context: character-bible.md, business-map.md, icp.md, tools.md, corrections.md."
echo "  4. Run the prompt at the top of each file inside the project, then paste the result back into the file."
echo "  5. Take tools.md to Customize, Connectors, Discover and connect every tool on the list."
