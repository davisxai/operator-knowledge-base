---
name: system-design
description: >
  Map out a software or business system architecture with pipeline stages, tool recommendations,
  realistic volume/pricing numbers, and clear visual layouts. Use when the user says "system design",
  "map this system", "how should we build this", "what tools do we need", "architect this",
  "lay out the pipeline", "system architecture", or when scoping a technical build.
argument-hint: "[system-type]"
allowed-tools: Read, Write, Edit, Grep, Glob, WebSearch, WebFetch
---

# System Design

Map a business or software system into a clear, buildable architecture. Output a document with
pipeline visualization, named tools, realistic volume estimates, and monthly cost projections.

## Arguments

- **system-type** (optional): lead-gen, voice-agent, rag, automation, website, crm, custom

If no arguments, ask: "What system are we designing?" One sentence is enough.

## Phase 1: Gather Context

**If in a project workspace:**
- Read CLAUDE.md, package.json, or equivalent for the existing stack
- Scan directory structure for existing infrastructure
- Read any context, requirements, or scope docs the workspace holds

**If no context available:**
- Work from the user's description and conversation history

Extract:
- What the system needs to DO (jobs, not features)
- Who it serves (end users, internal team, customers)
- Volume requirements (how many leads, messages, requests, etc.)
- Budget constraints if mentioned
- Existing tools or accounts already in play

## Phase 2: Map the Pipeline

Every system is a pipeline. Break it into sequential stages where each stage has:

- **Stage name** (verb-noun: "Source Leads", "Enrich Data", "Send Outreach")
- **Job** one sentence explaining what this stage does
- **Input** what flows in
- **Output** what flows out
- **Tool** specific named tool(s) recommended, with alternatives

Draw the pipeline as ASCII:

```
[STAGE 1]  -->  [STAGE 2]  -->  [STAGE 3]  -->  [STAGE 4]  -->  [STAGE 5]
 Verb noun       Verb noun       Verb noun       Verb noun       Verb noun
```

Then detail each stage in this format:

```
### Stage N: [Name]

**Job:** [One sentence]

- **Input:** [What flows in]
- **Output:** [What flows out]
- **Tool:** [Primary recommendation] | Alt: [Alternative 1], [Alternative 2]
- **Cost:** $X/mo at [volume] ([pricing model])
- **Setup:** [One-time setup steps, if any]
- **Notes:** [Gotchas, dependencies, decisions needed]
```

## Phase 3: Volume Model

Build a realistic volume model for the system. Work backwards from the desired outcome.

**For lead gen systems:**
```
Target: X meetings booked/mo
  <-- requires Y positive replies (Z% reply-to-meeting rate)
    <-- requires W emails sent (V% reply rate)
      <-- requires U enriched leads (T% email valid rate)
        <-- requires S raw leads scraped
```

**For voice agent systems:**
```
Target: X calls handled/mo
  <-- requires Y concurrent lines
    <-- requires Z minutes/mo of voice API
      <-- at $W/min = $X/mo voice cost
```

**For automation/workflow systems:**
```
Target: X workflows triggered/mo
  <-- requires Y API calls
    <-- at Z executions/mo per tool
      <-- $W/mo per tool tier
```

Show the math. Use typical industry ranges as starting assumptions and verify against
your own market before committing:
- Cold email open rate: 40-60%
- Cold email reply rate: 2-5%
- Reply to meeting rate: 30-50%
- Email bounce rate (verified list): 2-5%
- Lead enrichment match rate: 60-80%

## Phase 4: Cost Stack

List every tool with its pricing tier and monthly cost at the projected volume.

Format:

```
## Monthly Cost Stack

- **[Tool 1]** [what it does] $X/mo ([tier name], [volume included])
- **[Tool 2]** [what it does] $X/mo ([tier name], [volume included])
- **Total monthly tooling:** $X/mo
- **One-time setup costs:** $X (domains, warmup period, etc.)
```

Research current pricing using WebSearch if not confident in numbers. Tool pricing changes
frequently, always verify. Include the pricing page URL as source.

## Phase 5: Decision Points

List what needs to be confirmed before building. Format:

```
## Decisions Needed

**Must decide before build starts:**
- [Decision 1] [options] [what depends on this]

**Can decide during build:**
- [Decision 2] [options] [when it needs to be locked]
```

## Phase 6: Write Output

- In a project workspace: write to `docs/system-design.md` or the workspace's equivalent
- Standalone: output directly to terminal

## Common System Templates

Use these as starting frameworks. Adapt, don't copy.

### Lead Gen / Outreach System
Stages: Source --> Enrich --> Load --> Outreach --> Convert
Tools: Apollo/Clay + enrichment APIs + Instantly/Smartlead + Cal.com/Calendly

### Voice Agent System
Stages: Configure --> Deploy --> Route --> Handle --> Log
Tools: Retell/Vapi + Twilio/OpenPhone + Supabase + n8n

### RAG Pipeline
Stages: Ingest --> Chunk --> Embed --> Store --> Query
Tools: Custom ingestion + LangChain/LlamaIndex + embeddings + Pinecone/Supabase pgvector

### Automation Workflow
Stages: Trigger --> Process --> Transform --> Act --> Notify
Tools: n8n/Make + custom logic + destination APIs + Slack/email

### Website / Web App
Stages: Design --> Build --> Deploy --> Monitor
Tools: Figma + Next.js/Supabase/Tailwind + Vercel + Analytics

## Quality Checks

Before delivering:
- [ ] Every stage has a named tool (not "TBD")
- [ ] Volume model works backwards from a real target number
- [ ] Cost stack has actual dollar amounts with tier names
- [ ] Decisions list separates "before build" from "during build"
- [ ] ASCII pipeline diagram is included
- [ ] No markdown tables, structured bullets only
