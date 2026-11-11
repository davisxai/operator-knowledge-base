#!/usr/bin/env bash
# Usage: bash install.sh [--list] [all | lemo-opuscar pixelfx blender shotcraft clawd librosa web]
# Installs the Claude Code side of the motion repos guide. Each target is independent and safe to rerun.
set -euo pipefail

SKILLS_DIR="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
WORK_DIR="${MOTION_REPOS_DIR:-$HOME/motion-repos}"

usage() {
  cat <<'EOF'
Targets
  lemo-opuscar   Claude Code plugin: 66 film styles, films rendered in code
  pixelfx        Claude Code plugin: 244 pixel art effects and the skill that makes new ones
  blender        MCP for Blender: adds the "blender" MCP server to Claude Code (needs uv)
  shotcraft      video-shotcraft: clones the repo and links it into ~/.claude/skills
  clawd          ClaudeAnimationBase: clones the repo and runs npm install
  librosa        pip3 install librosa
  web            prints the npm line for three.js, rapier, and postprocessing in a React project
  all            every target above

Flags
  --list         show what each target would run, run nothing
  -h, --help     this text

Environment
  CLAUDE_SKILLS_DIR   where skills get linked (default ~/.claude/skills)
  MOTION_REPOS_DIR    where repos get cloned (default ~/motion-repos)
EOF
}

LIST=0
TARGETS=()
for arg in "$@"; do
  case "$arg" in
    --list) LIST=1 ;;
    -h|--help) usage; exit 0 ;;
    all) TARGETS=(lemo-opuscar pixelfx blender shotcraft clawd librosa web) ;;
    lemo-opuscar|pixelfx|blender|shotcraft|clawd|librosa|web) TARGETS+=("$arg") ;;
    *) echo "unknown target: $arg" >&2; usage; exit 1 ;;
  esac
done
if [ "${#TARGETS[@]}" -eq 0 ]; then usage; exit 1; fi

need() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "missing: $1. $2" >&2
    return 1
  fi
}

run() {
  # run "description" cmd args...
  local desc="$1"; shift
  if [ "$LIST" -eq 1 ]; then
    printf '  %s\n    %s\n' "$desc" "$*"
  else
    echo "-> $desc"
    "$@"
  fi
}

clone_or_pull() {
  local url="$1" dir="$2"
  if [ -d "$dir/.git" ]; then
    run "update $(basename "$dir")" git -C "$dir" pull --ff-only
  else
    run "clone $(basename "$dir")" git clone --depth=1 "$url" "$dir"
  fi
}

for t in "${TARGETS[@]}"; do
  echo "== $t"
  case "$t" in
    lemo-opuscar)
      need claude "Install Claude Code first: https://claude.com/claude-code" || continue
      run "add the lemolab marketplace" claude plugin marketplace add lemomo-ai/lemo-opuscar
      run "install lemo-opuscar" claude plugin install lemo-opuscar@lemolab
      ;;
    pixelfx)
      need claude "Install Claude Code first: https://claude.com/claude-code" || continue
      run "add the pixelfx marketplace" claude plugin marketplace add patch-gg/pixelfx
      run "install pixelfx" claude plugin install pixelfx@pixelfx
      ;;
    blender)
      need claude "Install Claude Code first: https://claude.com/claude-code" || continue
      need uvx "Install uv with the official installer, not pip: https://docs.astral.sh/uv/" || continue
      run "register the blender MCP server with Claude Code" claude mcp add blender uvx mcp-for-blender
      echo "   then: install the Blender addon with 'uvx mcp-for-blender setup', open Blender, restart Claude Code."
      ;;
    shotcraft)
      need git "Install git." || continue
      mkdir -p "$WORK_DIR" "$SKILLS_DIR"
      clone_or_pull https://github.com/Vincentwei1021/video-shotcraft.git "$WORK_DIR/video-shotcraft"
      run "link video-shotcraft into $SKILLS_DIR" ln -sfn "$WORK_DIR/video-shotcraft" "$SKILLS_DIR/video-shotcraft"
      ;;
    clawd)
      need git "Install git." || continue
      need npm "Install Node.js 20 or newer." || continue
      mkdir -p "$WORK_DIR"
      clone_or_pull https://github.com/JohnHeibel/ClaudeAnimationBase.git "$WORK_DIR/ClaudeAnimationBase"
      run "install ClaudeAnimationBase dependencies" npm --prefix "$WORK_DIR/ClaudeAnimationBase" install
      ;;
    librosa)
      need pip3 "Install Python 3." || continue
      run "install librosa" pip3 install librosa
      ;;
    web)
      echo "  In a React project (fiber v9, React 19):"
      echo "    npm install three @react-three/fiber @react-three/rapier @react-three/postprocessing"
      echo "  In a plain HTML file, use the import map in templates/one-file-scene.html instead."
      ;;
  esac
done
echo "done."
