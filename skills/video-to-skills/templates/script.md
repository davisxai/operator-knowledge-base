---
name: {{SLUG}}-script
description: Write a script, post, email, or talk outline with {{NAME}}'s structure and the user's own content. Reads the user's voice file first, then applies {{NAME}}'s openers, skeleton, and sentence shapes from {{SOURCE}}. Use when the user says "write this like {{NAME}}", "{{SLUG}} script", "use {{NAME}}'s structure on [topic]", or "{{SLUG}}-script".
argument-hint: [topic, or a rough draft]
allowed-tools: Read, Write, Glob
---

# {{NAME}}: script

Write the user's topic through {{NAME}}'s structure. The structure, the openers, the rhythm are his. The words, the examples, the numbers, and the stakes are the user's. If the result could be mistaken for {{NAME}}, it failed.

## Read first, in order

1. `{{VOICE}}` for how the user sounds and the words they never use. If the file does not exist, stop and ask for three samples of the user's own writing (an email, a post, a message to a client) before writing a line.
2. `{{ANALYSIS}}` only when the engine below is not enough for the topic.

## The engine, from the talk

### How he opens

<!-- FILL: his three strongest openers, verbatim with timestamps, each followed by the pattern in plain words (a promise, a number, a question he answers, a story). Pull from analysis section 6. -->

### The skeleton

<!-- FILL: the beat order he follows for one point, as a numbered list. Each beat gets one line on what it does and the verbatim transition line he uses to get there, with timestamp. Pull from analysis sections 2 and 6. If he has more than one skeleton (teaching a framework vs telling a story), list both and say when he uses each. -->

### How he lands a point

<!-- FILL: four to six verbatim sentences with timestamps, each followed by what the shape does (claim then because, question then answer, number then consequence, rule then the mistake it prevents). Pull from analysis section 7. -->

### How he closes

<!-- FILL: his close lines, verbatim with timestamps, and what each does (a callback to the open, a single rule to remember, an ask). Pull from analysis section 6. -->

### The frameworks he teaches

<!-- FILL: one line per framework from analysis section 2: the name, and when it is the right one to build a piece around. -->

## Rules

- **Transfer the engine, not the identity.** Never put his phrases in the user's mouth. Do not use any of these: <!-- FILL: the signature phrases from analysis section 8, comma separated -->.
- **Every number is the user's.** If the topic needs a number and the user gave none, write `[number]` in the draft and ask. Never borrow his numbers as if they were the user's.
- **Every example is the user's.** His examples show what kind of example goes in the slot. The user's business, clients, and week supply the actual one.
- **The user's anti-voice list wins.** If a word or shape is on the user's never list, it does not appear, no matter how often he uses it.
- **One idea per sentence, in the user's register.** Keep his pacing, not his vocabulary.

## Process

1. **Take the topic** from `$ARGUMENTS`. If it is a rough draft, keep every fact and number in it and rebuild the structure. If it is a topic, ask one question only if the format is unclear (a 60 second script, a post, an email, a talk outline). Otherwise assume a 60 second spoken script.
2. **Pick the frame.** Choose the framework or skeleton above that fits the topic and say which one in one line.
3. **Draft.** Open with one of his opener patterns, filled with the user's claim. Run the beats in his order. Land each point with one of his sentence shapes. Close with one of his close patterns.
4. **Read it out loud.** Cut every sentence the user would not say. Replace every borrowed phrase. Check the number slots.
5. **Deliver** in the output shape below.

## Output

- **Frame:** which framework or skeleton, one line.
- **The piece:** plain paragraphs, no beat labels, ready to read or paste.
- **Beat map:** the same piece as a numbered list, one line per beat, each tagged with the pattern it uses and the timestamp it came from.
- **Open slots:** every `[number]` or `[example]` the user still has to fill.

## Quality rules

- Never quote the talk inside the user's piece. The talk is the engine, not the content.
- Never pad to length. If the user's material covers three beats, write three beats.
- Never invent a fact, a client, a result, or a number for the user.
- If the user's voice file says they never do something he does constantly (profanity, hype, long stories), his habit loses.

Built from {{SOURCE}}. Analysis at {{ANALYSIS}}.
