---
name: recurring-report
description: Compile a recurring status report from multiple data sources. Schedule with Claude Desktop's task scheduler. Use when the user says "weekly report", "status summary", "recurring report", or wants to automate something they currently do manually each week.
---

Build the report in three phases.

Phase 1 - Source Pull
Read from each configured source in parallel. Default sources to look for unless overridden:
  - Gmail (last 7 days, filtered by labels the user provides)
  - Notion (a specific database or page if specified)
  - Linear (current cycle issues, status changes)
  - GitHub (PRs merged, issues closed)

Phase 2 - Compile
Group findings by source. Within each group:
  - Highlights (3-5 bullets max)
  - Open items (anything blocked, pending decision, or stale)
  - Notable numbers (counts, totals, percentages)

Phase 3 - Format
Output in the user's template format. Default template if none provided:
  - This Week's Wins
  - In Progress
  - Blocked / Needs Decision
  - Numbers
  - Next Week's Focus

End the report with a one-line summary of the most important thing. Save the output to the destination the user specifies (Notion page, email draft, file).
