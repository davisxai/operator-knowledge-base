# Auto-review rules

Grok Bot lets you write approval rules in plain language under Settings, General, Auto-review. Two kinds. "Ask first" always stops the matching action for you. "Allow automatically" lets it through if the reviewer sees no reason to stop it. Keep each rule narrow and specific to one action.

These are personal rules, so they apply to every bot on your account. That is fine. The bot descriptions carry the per-bot boundaries. These are the floor under all of them.

## Ask first

```
Ask first before sending any email, Slack message, DM, or LinkedIn message to anyone outside my account.
```

```
Ask first before creating, accepting, declining, or moving any calendar event.
```

```
Ask first before any payment, transfer, plan change, subscription cancellation, or entering a card number.
```

```
Ask first before merging any pull request that touches auth, payments, database schemas, or deployment configuration.
```

```
Ask first before deleting any file outside /workspace, any CRM record, any ticket, or any routine.
```

```
Ask first before publishing, posting, or scheduling anything on a social account or a website.
```

```
Ask first before changing any setting in an ad account, an analytics tool, or a billing tool.
```

## Allow automatically

```
Allow automatically when reading files under /workspace.
```

```
Allow automatically when running git status, git diff, git log, or git fetch.
```

```
Allow automatically when reading a connected Google Sheet or Notion page without writing to it.
```

## What auto-review does not see

From the security docs: memory writes and settings changes are not reviewed. If a bot learns a wrong preference, the reviewer will not catch it. Correct it in chat and check the bot's memory in its profile. Keep the systems of record (CRM, repo, tracker) as the truth so a drifted memory cannot quietly replace them.
