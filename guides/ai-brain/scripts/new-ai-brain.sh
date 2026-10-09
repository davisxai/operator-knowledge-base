#!/usr/bin/env bash
# Usage: scripts/new-ai-brain.sh [/absolute/path/to/ai-brain]   (default: ~/ai-brain)
# Copies the template folder, stamps today's date into memory/README.md,
# initializes a git repo so every edit has history, and prints the setup steps.
set -euo pipefail

TARGET="${1:-$HOME/ai-brain}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$HERE/../templates/ai-brain"
TODAY="$(date +%Y-%m-%d)"

if [ -e "$TARGET" ]; then
  echo "Refusing to overwrite: $TARGET already exists" >&2
  exit 1
fi

mkdir -p "$(dirname "$TARGET")"
cp -R "$SRC" "$TARGET"

# Stamp the creation date into the memory index. The .bak dance keeps sed portable across macOS and Linux.
sed -i.bak "s/YYYY-MM-DD/$TODAY/g" "$TARGET/memory/README.md"
rm -f "$TARGET/memory/README.md.bak"

( cd "$TARGET" && git init -q && git add -A && git commit -q -m "Create AI brain from the ai-brain guide" )

echo "AI brain created at $TARGET"
echo
echo "Next:"
echo "  1. Drop your logo in as $TARGET/logo.png and fill brand-kit.md."
echo "  2. Open the Claude desktop app. Create a project. Name it AI Brain."
echo "  3. Paste INSTRUCTIONS.md into the project Instructions. Replace the bracketed names."
echo "  4. Add brand-voice.md, brand-kit.md, character-bible.md, customer.md, logo.png, and the files in memory/ to the project Context."
echo "  5. Run the two prompts (brand-voice.md, character-bible.md) inside the project to fill those files from your own writing."
