#!/usr/bin/env python3
"""Usage: python3 scripts/validate-frontmatter.py /absolute/path/to/vault

Checks every markdown page under wiki/, ops/, sources/, daily/, and the root
index/hot pages against meta/schema.md: universal fields present, type and
status enums exact, first tag equals type, dates absolute, per-type required
fields present. Prints one line per violation and exits 1 if any. No
dependencies beyond the standard library.
"""
import re
import sys
from pathlib import Path

TYPES = {"person", "company", "concept", "decision", "client", "deal", "project", "source", "daily", "moc"}
WIKI_STATUS = {"seedling", "growing", "evergreen"}
OPS_STATUS = {"active", "won", "lost", "done"}
CLIENT_STATUS = {"discovery", "active", "client", "paused", "lost", "closed"}
REQUIRED = {
    "person": ["company", "role", "relationship", "last_contact"],
    "company": ["category", "relationship", "website"],
    "concept": [],
    "decision": ["decided_on", "relates_to", "supersedes", "confidence"],
    "client": ["company", "retainer", "started"],
    "deal": ["client", "stage", "value", "next_action", "next_action_date"],
    "project": ["client", "repo"],
    "source": ["url", "source_type", "date_ingested", "processed"],
    "daily": ["date"],
    "moc": [],
}
ENUMS = {
    "relationship": {"client", "prospect", "partner", "vendor", "competitor", "friend", "family", "self", "brand-deal", "reference"},
    "stage": {"lead", "discovery", "proposal", "build", "retainer", "closed"},
    "confidence": {"high", "medium", "low"},
    "source_type": {"article", "transcript", "email", "note", "document", "research"},
}
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SKIP_DIRS = {"meta", "inbox", "archive", ".obsidian", ".claude", ".git"}


def parse_frontmatter(text):
    """Minimal YAML reader for the flat key: value and '- item' list forms the schema uses."""
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    data, key = {}, None
    for raw in text[4:end].splitlines():
        line = raw.rstrip()
        if not line.strip():
            continue
        if line.startswith("  - ") or line.startswith("- "):
            if key is None:
                continue
            data.setdefault(key, [])
            if not isinstance(data[key], list):
                data[key] = []
            data[key].append(line.split("- ", 1)[1].strip().strip("'\""))
            continue
        if ":" in line and not line.startswith(" "):
            key, _, val = line.partition(":")
            key, val = key.strip(), val.strip()
            if val == "[]":
                data[key] = []
            elif val == "":
                data[key] = None  # list follows, or empty
            else:
                data[key] = val.strip("'\"")
    for k, v in list(data.items()):
        if v is None:
            data[k] = []
    return data


def check(path, fm, rel):
    problems = []
    for f in ["type", "created", "updated", "status", "tags", "aliases"]:
        if f not in fm:
            problems.append(f"missing universal field: {f}")
    t = fm.get("type")
    if t not in TYPES:
        problems.append(f"type not in schema: {t}")
        return problems
    for f in ["created", "updated"]:
        v = fm.get(f)
        if isinstance(v, str) and not DATE.match(v):
            problems.append(f"{f} is not YYYY-MM-DD: {v}")
    tags = fm.get("tags")
    if not isinstance(tags, list) or not tags or tags[0] != t:
        problems.append(f"first tag must equal type ({t}): {tags}")
    status = fm.get("status")
    top = rel.parts[0] if len(rel.parts) > 1 else ""
    if top == "wiki" or t in {"moc", "daily"}:
        if status not in WIKI_STATUS:
            problems.append(f"status not in wiki vocab: {status}")
    elif t == "client":
        if status not in CLIENT_STATUS:
            problems.append(f"status not in client vocab: {status}")
    elif top == "ops":
        if status not in OPS_STATUS:
            problems.append(f"status not in ops vocab: {status}")
    for f in REQUIRED[t]:
        if f not in fm:
            problems.append(f"missing {t} field: {f}")
    for f, allowed in ENUMS.items():
        v = fm.get(f)
        if isinstance(v, str) and v and v not in allowed:
            problems.append(f"{f} not an allowed value: {v}")
    for f in ["last_contact", "decided_on", "started", "next_action_date", "date_ingested", "date"]:
        v = fm.get(f)
        if isinstance(v, str) and v and not DATE.match(v):
            problems.append(f"{f} is not YYYY-MM-DD: {v}")
    return problems


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    root = Path(sys.argv[1]).expanduser().resolve()
    if not (root / "meta" / "schema.md").exists():
        print(f"No meta/schema.md under {root}. Is this a vault?")
        sys.exit(2)
    pages = []
    for p in root.rglob("*.md"):
        rel = p.relative_to(root)
        if rel.parts[0] in SKIP_DIRS or p.name == "README.md":
            continue
        if len(rel.parts) == 1 and p.name not in {"index.md", "hot.md"}:
            continue
        pages.append((p, rel))
    total, bad = 0, 0
    for p, rel in sorted(pages):
        total += 1
        fm = parse_frontmatter(p.read_text(errors="replace"))
        if fm is None:
            bad += 1
            print(f"{rel}: no frontmatter block")
            continue
        problems = check(p, fm, rel)
        if problems:
            bad += 1
            for pr in problems:
                print(f"{rel}: {pr}")
    print(f"\n{total} pages checked, {bad} with violations")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
