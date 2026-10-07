# Schema

Canonical frontmatter spec for every page in this vault. The contract between the vault, the agents, and anything that reads it. Writes that do not validate against this file are rejected.

## Universal fields (every note)

- **type:** one of `person`, `company`, `concept`, `decision`, `client`, `deal`, `project`, `source`, `daily`, `moc`
- **created:** YYYY-MM-DD. Set once, never changed.
- **updated:** YYYY-MM-DD. Bumped on every edit.
- **status:** see status vocab below.
- **tags:** list. First tag is always the type. Optional taxonomy tags after (e.g. `tool`, `content`, `family`).
- **aliases:** list. Alternate names the viewer should resolve to this page. Empty list allowed.

## Status vocab

- **Wiki pages** (`wiki/`): `seedling` (thin, needs enrichment), `growing` (useful, gaps remain), `evergreen` (complete, stable, trustworthy).
- **Ops pages** (`ops/`): `active` (live work), `won` (deal closed in our favor), `lost` (deal dead), `done` (work complete, candidate for `archive/`).
- **Sources** (`sources/`): use `processed` boolean instead, see source fields.
- **Daily and MOC pages:** use wiki vocab. MOCs are usually `growing`.

## Per-type fields

### person (`wiki/people/`)

- **company:** wikilink slug of their company, or empty string.
- **role:** short free-text role.
- **relationship:** one of `client`, `prospect`, `partner`, `vendor`, `competitor`, `friend`, `family`, `self` (`self` is reserved for the principal's own page).
- **last_contact:** YYYY-MM-DD or empty string.

### company (`wiki/companies/`)

- **category:** short free-text category (e.g. `telehealth`, `event-venue`, `ai-agency`).
- **relationship:** one of `client`, `prospect`, `partner`, `vendor`, `competitor`, `family`, `self`, `reference`.
- **website:** domain or URL, or empty string.

### concept (`wiki/concepts/`)

No extra required fields. Use tags for taxonomy: `tool`, `methodology`, `offer`, `content`.

### decision (`wiki/decisions/`)

- **decided_on:** YYYY-MM-DD.
- **relates_to:** list of wikilink slugs the decision affects.
- **supersedes:** wikilink slug of a prior decision, or empty string.
- **confidence:** one of `high`, `medium`, `low`.

### client (`ops/clients/<name>/brief.md`)

- **company:** wikilink slug of the client company.
- **status:** lifecycle vocab (`discovery`, `active`, `client`, `paused`, `lost`, `closed`). `discovery` is talking and scoping, `active` is a build underway, `client` is signed and ongoing. `paused` is on hold. `lost` and `closed` are terminal.
- **retainer:** monthly amount as string, or empty string.
- **started:** YYYY-MM-DD or empty string.

### deal (`ops/pipeline/`)

- **client:** wikilink slug of the person or company the deal is with.
- **stage:** one of `lead`, `discovery`, `proposal`, `build`, `retainer`, `closed`.
- **value:** deal value as string (e.g. `$8,000 build + $1,500/mo`).
- **next_action:** one line, what moves the deal forward.
- **next_action_date:** YYYY-MM-DD or empty string.

### project (`ops/projects/`)

- **client:** wikilink slug of the client it serves, or empty string for internal.
- **repo:** absolute path or URL to the codebase, or empty string.

### source (`sources/YYYY/`)

- **url:** original URL or empty string.
- **source_type:** one of `article`, `transcript`, `email`, `note`, `document`, `research`.
- **date_ingested:** YYYY-MM-DD.
- **processed:** boolean. True once the ingest operation has folded it into the wiki.

### daily (`daily/`)

- **date:** YYYY-MM-DD. Filename matches.

### moc (`wiki/mocs/`)

No extra required fields. Body is the index: linked pages with one-line hooks.

## Color system (optional)

One palette per type, used for the Obsidian graph and for any dashboard that reads the vault. Swap the values for your own brand. Reserve the strongest color for the type that represents money.

- **client:** `#d2042d`
- **deal:** `#f97316`
- **project:** `#10b981`
- **person:** `#3b82f6`
- **company:** `#8b5cf6`
- **concept:** `#06b6d4`
- **decision:** `#f59e0b`
- **moc:** `#fafafa`
- **source:** `#6b7280`
- **daily:** `#64748b`
- **inbox:** `#ec4899`
- **archive / meta:** `#525252`

## Validation rules

- Every field above for the page's type must be present. Empty string is allowed where noted, missing keys are not.
- Enum fields must use an allowed value exactly.
- Dates are absolute `YYYY-MM-DD`. Never relative.
- Slugs are lowercase, hyphenated, canonical: `jane-doe`, `acme-co`, `q3-pricing-reset`.
- First tag equals `type`.
