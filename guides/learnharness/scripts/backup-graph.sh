#!/usr/bin/env bash
# Usage: ./backup-graph.sh [destination-dir]  -- archives your LearnHarness data folder (graph, chats, settings, prompt overrides) to a timestamped tarball. API key files live beside the data folder and are deliberately not included.
set -euo pipefail

case "$(uname -s)" in
  Darwin)
    DATA_DIR="$HOME/Library/Application Support/LearnHarness/data"
    ;;
  Linux)
    DATA_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/LearnHarness/data"
    ;;
  *)
    echo "Unsupported OS for this script. On Windows, copy %APPDATA%\\LearnHarness\\data manually."
    exit 1
    ;;
esac

if [ ! -d "$DATA_DIR" ]; then
  echo "No LearnHarness data folder found at: $DATA_DIR"
  echo "Run the app at least once first."
  exit 1
fi

DEST="${1:-$HOME/learnharness-backups}"
mkdir -p "$DEST"

STAMP="$(date +%Y-%m-%d-%H%M%S)"
ARCHIVE="$DEST/learnharness-data-$STAMP.tar.gz"

tar -czf "$ARCHIVE" -C "$(dirname "$DATA_DIR")" "$(basename "$DATA_DIR")"

echo "Backed up to: $ARCHIVE"
du -h "$ARCHIVE" | awk '{print "Size: " $1}'
