# Long-talk analysis spec

What `analysis/analysis.md` contains, section by section, for one person's long video. The reader of this file is the pack generator and the three pack skills, not a human browsing. Tight, evidenced, in order.

## Hard rules

- Every pattern claim needs a verbatim quote with a timestamp from the transcript. If the transcript cannot support a section, write TBD and say what is missing.
- Captions and Whisper mishear names and brands. Normalize obvious mishears when quoting. Never invent words.
- Timestamps come from the transcript blocks. Never from memory.
- No markdown tables. Use `- **Key:** Value` bullets. No emojis. No em dashes or double dashes. Absolute dates only.
- Describe, do not judge. What he does and how it works, not whether it is right.

## Sections, in order

### 1. Basis

One block: `# Analysis: NAME`, then the source title, channel, URL, length, transcript source (captions or which Whisper), word count, and the date analyzed.

### 2. Frameworks

Every named or repeatable method he teaches. One entry each:

- **Name:** his name for it if he gives one, else a plain label in brackets.
- **Steps:** numbered, in his words, in his order, each with a timestamp. Three steps if he gave three.
- **Solves:** the problem he says it is for, quoted.
- **Where he applies it:** the examples he runs it on, with timestamps.

### 3. Claims and the numbers behind them

Every claim he attaches a number to. One line each: the claim, the number, the timestamp, and whether he names a source (his own business, a client, a study, nothing). Keep the unsourced ones. The validate skill uses this list to stop the user from repeating a number as fact.

### 4. Rules he states

Do and never lines, verbatim, with timestamps. "Always X." "Never Y." "The mistake everyone makes is Z." Group them if they cluster (pricing rules, hiring rules), otherwise list them in order.

### 5. What he keeps coming back to

Recurring topics ranked by how many separate times he returns to them. One line each: the topic, the count, the timestamps, and the one sentence he says about it most often. The ideate skill is built from this section.

### 6. Openers, transitions, closes

- **How he opens:** the first two or three sentences of the talk, verbatim, and the first sentence of each major section. Name the pattern (a promise, a question, a story, a number).
- **How he moves between points:** the exact transition lines, verbatim, with timestamps.
- **How he closes:** the last two or three sentences, verbatim, and what they do (a callback, an ask, a rule).

### 7. Sentence shapes and delivery

How he talks, with five or more verbatim sentences that are unmistakably him:

- Typical sentence length and whether he repeats lines for emphasis.
- Questions he asks and then answers himself.
- Specificity habits: numbers, names, dates, concrete nouns.
- What he does when he changes his mind mid-sentence or restarts.
- Who he talks to: "you", "we", a named person in the room.

### 8. Signature phrases

Verbatim phrases that appear more than once, with the count. These go in every pack skill's avoid list, so be complete.

### 9. Practices to adopt

The point of the whole exercise. Each practice:

- **Practice:** one line, as an action.
- **His words:** the quote and timestamp it comes from.
- **In your business:** what it looks like as a concrete step for the user. Where it depends on the user's context, write the question to ask them instead of guessing.

Order them by how much of the talk he spends on each.

### 10. Why it lands

The specific mechanics that make him worth listening to on camera. Concrete: how often a number lands, how he uses the audience, how he admits what he does not know, where the humor comes from, how long he lets a point sit. This is the section the script skill borrows from.

### 11. Open

Every TBD from the sections above, and every question the user has to answer before the pack can give its best output.
