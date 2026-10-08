# /stack-map

Read any repo and report it against the ten layers of the build stack, in the order a build happens. Which layers are present, which are missing, and the next command for each gap.

## Install

```bash
mkdir -p ~/.claude/skills/stack-map
curl -o ~/.claude/skills/stack-map/SKILL.md https://raw.githubusercontent.com/davisxai/operator-knowledge-base/main/skills/stack-map/SKILL.md
```

Or clone the repo and `cp -r skills/stack-map ~/.claude/skills/`.

## Usage

```
/stack-map
/stack-map ~/projects/client-app
```

## What you get

A ten-line report, one per layer, each marked present, partial, or not detected, with the file or dependency that proves it. Then a count, then the next command for each gap in build order.

## Why it's built this way

The skill only reads config files, lockfiles, and workflow files. It never scans source code to guess. A layer is present when a file on disk says so, and "not detected" is reported as a finding rather than hidden. Env files are read for variable names only, never values.

## Where the ten layers come from

The build stack guide at [guides/build-stack/](../../guides/build-stack/). The picks and alternatives per layer are documented there, and the skill reports against that list.
