# Handoff protocol

How the eight bots pass work without a group chat. Finding credited to Flavio Copes: file handoffs with named owners beat open group chats, which tend toward bots repeating each other and burning usage on discussion.

## The rule

One bot writes a file. The next bot reads it. Nobody discusses.

## Folder layout in /workspace

```
/workspace/
  desk/
    attention.md        rebuilt every morning
    promises.md         what the founder said they would do
    queue/              every draft waiting for the founder
  radar/
    competitors.md      the watch list
    reads/              YYYY-MM-DD.md, the weekly read
    deep-dives/
    log.md
  pen/
    voice.md            the founder's voice rules
    structures/         one file per format
    drafts/
    sent/               what the founder actually sent
    deltas.md           what changed between draft and sent
    inbox.md            requests from other bots
  pipeline/
    icp.md
    batches/
    keeper.csv
    hygiene.md
  front/
    policy.md
    customers.csv
    daily/
    watch.md
    notes/language.md   customers' own words
    canned/
  ledger/
    subscriptions.csv
    thresholds.md
    exports/
    receipts/YYYY/MM/
    weekly/
  forge/
    spec.md
    inbox/              repro packs from Sentinel
    tickets.md
    known-issues.md
    postmortems/
  score/
    metrics.md
    weekly/
    questions.md
```

## Who writes where

- A bot writes only inside its own folder, plus /workspace/atlas/queue/ for anything needing approval, plus the inbox file of the bot it is handing to.
- A bot reads any folder it needs. Reading is free. Writing outside your folder is the failure.

## The handoff file

When one bot needs another, it appends a block to that bot's inbox file:

```
## YYYY-MM-DD HH:MM from <bot>
Task: one line
Input: path to the file with the details
Needed by: date or "no deadline"
Return to: path where the result should land
```

The receiving bot reads its inbox at the start of every run, works the oldest item first, and writes the result where the block said.

## When a group chat is right

Two cases only:

- A handoff the founder needs to watch live, like a launch day.
- A question that needs two specialists to disagree in front of the founder, like Sonar and Prism on whether a competitor move matters.

Cap it at three bots plus the founder. End it when the decision is made. Do not leave it running.

## The ledger (optional, for multiple projects)

If you run more than one project, keep a Projects board and a Tasks board in Notion or a sheet. One channel per project, six bots max per channel, reuse existing bots before creating new ones. Pattern credited to Eric Zakariasson's "How I run multiple teams of Grok Bots." A starter CSV for the Tasks board is at `task-ledger.csv`.
