# vault-ingest

Run your vault's ingest operation from any project. Paired with the [agent-vault-starter](../../guides/agent-vault-starter/) guide. The auto-capture rule in that guide tells every Claude Code session to write to the vault without being asked. This is the skill it calls for anything bigger than a quick inbox note.

## Install

```bash
mkdir -p ~/.claude/skills/vault-ingest
curl -o ~/.claude/skills/vault-ingest/SKILL.md https://raw.githubusercontent.com/davisxai/operator-knowledge-base/main/skills/vault-ingest/SKILL.md
```

Then open the file and replace `/ABSOLUTE/PATH/TO/vault` with your vault's path. One edit, one line.

## Usage

```
/vault-ingest ~/Downloads/discovery-call-2026-10-07.md
/vault-ingest https://example.com/article
/vault-ingest                      # drains inbox/, oldest first
```

## Why it is built this way

The skill holds no logic of its own. It loads the vault's contract and the vault's own ingest skill, then runs that. One canonical definition of ingest lives inside the vault, and this wrapper makes it reachable from every other project on the machine. Change the operation once, in the vault, and every project picks it up.
