---
name: {{SLUG}}-ideate
description: Turn what {{NAME}} keeps coming back to into ranked angles for the user's own business or content. Reads the user's voice and context first, then maps {{NAME}}'s recurring topics and frameworks from {{SOURCE}} onto the user's situation. Use when the user says "ideas from {{NAME}}", "{{SLUG}} ideate", "what would {{NAME}} say about my business", "angles for this week", or "{{SLUG}}-ideate".
argument-hint: [one line on your business or the audience you write for]
allowed-tools: Read, Write, Glob
---

# {{NAME}}: ideate

Angles, not summaries. Each angle is something the user can write, say, or do this week, tied to the exact moment in the talk it came from and ranked by how much weight {{NAME}} put on it.

## Read first, in order

1. `{{VOICE}}` for who the user is, what they sell or make, and who they write for. If the file does not exist, ask for a one-line description of the business and the audience before going on.
2. `{{ANALYSIS}}` sections 5 and 9 when the lists below are not enough.

## What he keeps coming back to

Ranked by how many separate times he returned to it in the talk. The count is the weight.

<!-- FILL: from analysis section 5, one line per topic: the topic, the return count, the timestamps, and the sentence he says about it most often, verbatim. Keep the ranking. -->

## The frameworks

<!-- FILL: from analysis section 2, one entry per framework: the name, the steps as a single line, and the problem he says it solves, quoted with timestamp. -->

## Practices he teaches

<!-- FILL: from analysis section 9, one line per practice: the action, and the quote with timestamp. Keep his order. -->

## Process

1. **Take the context** from `$ARGUMENTS`: the business, the offer, the audience. One line is enough. If missing and the voice file does not cover it, ask once.
2. **Map every recurring topic** onto the user's context. For each one, write the angle as the user would state it, about the user's customers, not about {{NAME}}'s. Drop any topic that has no honest mapping and say so in one line.
3. **Map the frameworks.** For each framework, write the piece or the move the user could build on it: a post that walks their customer through it, an offer rebuilt with it, a process change.
4. **Rank.** Weight first (his return count), then fit to the user's context. Break ties toward the angle the user can act on with what they already have.
5. **Deliver** ten angles. Fewer if the talk only supports fewer. Never pad.

## Output

For each angle, in rank order:

- **Angle:** one sentence, in the user's voice, about the user's situation.
- **From:** the topic or framework, with the quote and timestamp it came from.
- **Shape:** what it becomes (a 60 second script, a post, an email to clients, a change to the offer, a question to ask customers).
- **First line:** one possible opening line, written for the user.

Then:

- **Dropped:** topics that did not map to the user's context, one line each on why.
- **Questions:** anything about the user's business you needed and did not have.

## Quality rules

- Never present his angle as the user's. Every angle is rewritten about the user's customers and stakes.
- Never bring his numbers across as the user's. If an angle needs a number, write `[your number]`.
- Never rank by what sounds exciting. Rank by his weight and the user's fit, and say the count.
- Never invent a topic he did not return to. The counts come from the analysis.
- Do not use his signature phrases in any first line: <!-- FILL: the signature phrases from analysis section 8, comma separated -->.

Built from {{SOURCE}}. Analysis at {{ANALYSIS}}.
