#!/usr/bin/env bash
# Usage: bash new-stack.sh my-app
# Scaffolds a Next.js app with the first four layers of the build stack wired in:
# Next.js with TypeScript and Tailwind, the Supabase client, shadcn/ui, a validate-only CI workflow,
# a project CLAUDE.md for Claude Code, and a .env.example. Run it from the folder that should hold the app.

set -euo pipefail

name="${1:-}"
if [ -z "$name" ]; then
  echo "Usage: bash new-stack.sh my-app"
  exit 1
fi

here="$(cd "$(dirname "$0")" && pwd)"
templates="$here/../templates"

command -v pnpm >/dev/null 2>&1 || { echo "pnpm is required: npm install -g pnpm"; exit 1; }

echo "1/6  Next.js app"
pnpm dlx create-next-app@latest "$name" \
  --ts --tailwind --eslint --app --src-dir \
  --import-alias "@/*" --use-pnpm --yes

cd "$name"

echo "2/6  Supabase client"
pnpm add @supabase/supabase-js @supabase/ssr

echo "3/6  shadcn/ui"
pnpm dlx shadcn@latest init --defaults --yes

echo "4/6  CI workflow (lint and typecheck, validates only)"
mkdir -p .github/workflows
cp "$templates/ci.yml" .github/workflows/ci.yml
node - <<'NODE'
const fs = require("fs");
const pkg = JSON.parse(fs.readFileSync("package.json", "utf8"));
pkg.scripts = pkg.scripts || {};
pkg.scripts.typecheck = pkg.scripts.typecheck || "tsc --noEmit";
fs.writeFileSync("package.json", JSON.stringify(pkg, null, 2) + "\n");
NODE

echo "5/6  Claude Code project file and env example"
cp "$templates/CLAUDE.md" CLAUDE.md
cp "$templates/env.example" .env.example
grep -q "^.env" .gitignore 2>/dev/null || printf "\n.env\n.env.local\n.env.*.local\n" >> .gitignore

echo "6/6  First commit"
git add -A
git commit -q -m "Scaffold the build stack: Next.js, Supabase client, shadcn, CI, CLAUDE.md" || true

echo
echo "Done. Next:"
echo "  cd $name"
echo "  cp .env.example .env.local   # fill in the Supabase keys"
echo "  pnpm dev"
echo "  gh repo create $name --private --source=. --push   # layer 06"
