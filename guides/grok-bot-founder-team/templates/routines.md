# Routines

Paste-ready routine requests. Send each one to the bot that owns it, in that bot's chat. Confirm the timezone, the input, the output, and the failure behavior before you accept the schedule. Then use Test run once and read the result before you let it run on its own.

Two rules from the docs worth keeping in front of you: a test run performs real work, and deleting a routine has no undo.

## Atlas

```
Every weekday at 7:30 AM my time, rebuild /workspace/atlas/attention.md from the inbox, calendar, and every bot's latest file, then post the daily brief in this conversation. Three sections: needs you, in motion, done since yesterday. If nothing changed, post one line that says so. Never send anything.
```

```
Every weekday at 3:30 PM my time, sweep the inbox once, add anything new that needs me to the attention file, and post only the items that need me today. If there are none, post nothing.
```

## Sonar

```
Every Monday at 6:30 AM my time, run the weekly competitor read against /workspace/sonar/competitors.md, compare to the most recent file in /workspace/sonar/reads/, write the new read to /workspace/sonar/reads/ with today's date, append one line to /workspace/sonar/log.md, and post the "what changed" section here. If a source is blocked, mark it unavailable and continue.
```

## Tracer

```
Every Tuesday at 7:00 AM my time, build a prospect batch of [N] against /workspace/tracer/icp.md, mark each row CLEAR or FLAG with evidence links, write it to /workspace/tracer/batches/ with today's date, and post the count of CLEAR rows here. Do not enroll or contact anyone.
```

```
Every Friday at 4:00 PM my time, run the CRM hygiene pass. List duplicates, missing fields, and stale stages in /workspace/tracer/hygiene.md. Post the counts here. Change nothing.
```

## Sentinel

```
Every weekday at 8:00 AM and 2:00 PM my time, sweep the support inbox. Draft replies for questions the docs answer, cite the doc in each draft, put every draft in /workspace/atlas/queue/, build a repro pack for any bug into /workspace/anvil/inbox/, and update /workspace/sentinel/daily/ with today's counts. Send nothing.
```

## Rainmaker

```
Every Friday at 9:00 AM my time, write the weekly cash view to /workspace/rainmaker/weekly/ with today's date. Cash in, cash out, due in the next 14 days, three biggest line items, every flag over the thresholds file. Link every number to its source row. Post the flags here. Move no money.
```

```
On the first weekday of every month at 9:00 AM my time, reconcile the latest bank export in /workspace/rainmaker/exports/ against /workspace/rainmaker/subscriptions.csv. List charges not on the sheet and sheet items not charged in 60 days. Post the list here. Cancel nothing.
```

## Anvil

```
Every 30 minutes on weekdays between 8:00 AM and 6:00 PM my time, check open PRs and CI. For each PR, post the link and one of: green and small, merged; green but wide, needs you; red, here is why. Merge only what the description rules allow.
```

## Prism

```
Every Monday at 7:00 AM my time, write the weekly scoreboard to /workspace/prism/weekly/ with today's date using the metrics in /workspace/prism/metrics.md, comparing to the same weekday four weeks prior. Post the "what moved" section here. Change no settings.
```

## Event triggers

Where your Cursor account integrations support it, a routine can start from an event instead of a clock. Keep the match rule narrow. From the docs: a broad listener like "every new message" creates noise, consumes usage, and raises the chance of acting on the wrong input.

```
When a message in #support contains a ticket link and the phrase "needs repro", build a repro pack for that ticket into /workspace/anvil/inbox/ and post the path here. Do not reply in Slack.
```

## What not to schedule

- Anything that runs every 15 minutes "just to check." That is 96 runs a day, each one billed, most of them finding nothing.
- Anything vague. "Keep an eye on the blog" loops. "Compare today's post list to the RSS feed and report additions" finishes.
- Anything that sends. Every routine above ends in a draft, a file, or a post in the bot's own chat. Sending is the founder's job.
