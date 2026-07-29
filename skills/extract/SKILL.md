---
name: extract
description: Extract decisions, action items, facts, and open questions from messy input. Voice transcripts, meeting notes, Slack dumps, email threads. Use when the user says "extract from this", "what did we decide", "action items from this", or drops unstructured text.
---

Process the input through four passes.

Pass 1 - Decisions
Find every moment something was decided. Format: who decided what. Include the reasoning if it was given.

Pass 2 - Action Items
Pull every commitment to do something. Format: who is doing what, by when if stated. Mark "TBD" if no owner.

Pass 3 - Facts
Surface concrete facts stated: numbers, dates, names, claims worth verifying. One bullet per fact.

Pass 4 - Open Questions
List unresolved questions explicitly raised or implied by incomplete decisions.

Output four sections in that order. Skip a section if empty. Do not pad. Do not interpret beyond what was said.
