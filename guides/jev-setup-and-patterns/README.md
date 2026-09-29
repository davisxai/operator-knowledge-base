# Jev Setup and Five Patterns

> Follow [@daviss.dev](https://instagram.com/daviss.dev) and [@os.operator](https://instagram.com/os.operator) on Instagram for more guides like this.

---

### From a fresh account to five typed decisions running in your stack.

Jev is TypeSafe AI's System One model. It does not write text. You send it content and a question with a fixed set of answers, and it picks one and tells you how sure it is. This guide covers the install, the three question types, and five patterns you can drop into a real system. It is not a review and it is not a benchmark.

Every command here was run. Every number has a source at the bottom.

---

## What you'll get

→ Account, API key, SDK install in Python and JavaScript, and the Claude Code plugin
→ The three question types with the exact fields each one returns
→ A runnable quickstart in both languages, with the response explained line by line
→ Five pattern scripts: intent routing, confidence-gated routing, speculative fan-out, composite scoring, tool-call risk gating
→ A decision spec template so you write the criteria before you write the call
→ The honest list of what Jev is bad at, taken from TypeSafe's own docs

---

## Prerequisites

- Python 3.10 or newer, or Node.js 20 or newer
- A TypeSafe account. Jev is in early access as of September 29, 2026. Create the account at [typesafe.ai](https://typesafe.ai). If signups are paused when you read this, join the list and come back. TypeSafe briefly lost the ability to serve users from the API in the first week because demand was too high.
- Claude Code, if you want the agent to write Jev calls for you. Optional.

---

## Contents

1. [What Jev is](#1-what-jev-is)
2. [Install](#2-install)
3. [The three question types](#3-the-three-question-types)
4. [Confidence, and what to do with it](#4-confidence-and-what-to-do-with-it)
5. [What goes in state](#5-what-goes-in-state)
6. [First call](#6-first-call)
7. [Five patterns](#7-five-patterns)
8. [Cost and speed](#8-cost-and-speed)
9. [Where it breaks](#9-where-it-breaks)
10. [Troubleshooting](#10-troubleshooting)
11. [Quick reference](#11-quick-reference)

---

## 1. What Jev is

A language model like Claude or ChatGPT builds its answer one token at a time. That is what makes it slow, what makes it cost money on output, and what lets it make things up.

Jev skips generation. It reads the whole input once and returns a probability distribution over answers you defined. TypeSafe calls this a System One model, after the fast, instinctive mode of thinking in Kahneman's "Thinking, Fast and Slow." Look, decide, done.

Three things follow from that design:

- **It is fast.** TypeSafe quotes 70 to 500 milliseconds end to end.
- **Output is free.** You pay $0.042 per million input tokens. Output tokens are not metered.
- **It cannot invent an option.** If you gave it three labels, you get one of the three. It can still pick the wrong one.

Jev launched on September 15, 2026. TypeSafe was founded by Diogo Almeida, who worked on RLHF and ChatGPT at OpenAI before leaving to build a model that decides instead of writes. Vercel replaced the OpenAI-based classifier that reviews commands for safety with Jev and reported results five to eighteen times faster. LangChain shipped a `langchain-typesafe` package two days after launch.

Here is the whole loop:

```
   your text            your questions
   (the state)          (choice / score / noul)
        │                       │
        └───────────┬───────────┘
                    ▼
          POST /v1/systemone
                    │
                    ▼
        ┌───────────────────────┐
        │  jev-1.13             │   one forward pass
        │  reads everything     │   no token generation
        └───────────────────────┘
                    │
                    ▼
     { answers: { dept: {choice, confidence, probabilities},
                  urgent: {noul} },
       usage: {input_tokens, output_tokens} }
                    │
                    ▼
            your code routes on the numbers
```

Jev does not replace the writer model. It sits next to it. The writer writes. Jev sorts, ranks, flags, and gates.

---

## 2. Install

### Account and key

1. Create an account at [typesafe.ai](https://typesafe.ai).
2. Create a key at [console.typesafe.ai/keys](https://console.typesafe.ai/keys).
3. Put it in your environment. Both SDKs read `TYPESAFE_API_KEY` on their own.

```bash
export TYPESAFE_API_KEY="sk-..."
```

A copyable env file is at [templates/env.example](templates/env.example). Never commit the actual key.

### Python

```bash
pip install typesafe-sdk
```

Version 0.7.2 on PyPI as of September 29, 2026. Requires Python 3.10 or newer. If you use uv, `uv add typesafe-sdk` works the same.

### JavaScript and TypeScript

```bash
npm install @typesafe-ai/sdk
```

Version 0.6.0 on npm as of September 29, 2026. Requires Node 20 or newer. Ships ESM, CommonJS, and type declarations. Answer types are inferred from your questions, so `answers.department.choice` is typed to the labels you passed in.

### Claude Code plugin

TypeSafe publishes an agent skill that teaches Claude Code the API, the current docs, and the patterns. Two commands:

```bash
claude plugin marketplace add typesafe-ai/skills
claude plugin install typesafe@typesafe-ai
```

After that you describe the decision and Claude writes the call. The repo's own example prompt: "Use TypeSafe to route incoming support tickets by department, with human review for uncertain decisions."

For other agents (Cursor, Codex, and so on):

```bash
npx skills add typesafe-ai/skills --skill typesafe-ai
```

The skills repo is MIT licensed with 2,400 stars as of September 29, 2026.

> [!NOTE]
> The plugin is a skill file, not a model. It makes the agent good at writing Jev code. It does not give the agent a key or make calls on its own.

---

## 3. The three question types

Everything you do with Jev is one of three question shapes. You can send any mix of them in one call.

### Choice. "Which one?"

You give labels with descriptions. Jev picks one label.

```python
Choice(
    instructions="Which team should handle this",
    criteria={
        "billing": "Payment or subscription issues",
        "technical": "Bugs or integration problems",
        "sales": "Pricing or account questions",
    },
)
```

Returns `choice` (the label), `confidence` (0 to 1), and `probabilities` (one number per label, summing to 1).

### Score. "Which level?"

You give an ordered rubric starting at level 0. Jev picks a level.

```python
Score(
    instructions="How frustrated the customer appears",
    criteria=[
        "Calm, just stating facts",        # 0
        "Frustrated but civil",            # 1
        "Very angry, strong language",     # 2
    ],
)
```

Returns `score`, `confidence`, `legend` (level number to description), and `probabilities` (one per level).

One detail that matters later: `score` is an expected value. It can land between two integer levels, like 1.4. That is by design. It is what makes weighted scoring work in the composite pattern.

### Noul. "Is this true?"

You make a statement. Jev returns the probability that it holds.

```python
Noul(instructions="The message conveys urgency or time-sensitivity")
```

Returns `noul`, a single number from 0 to 1. Near 1 means yes. Near 0 means no. Near 0.5 means it cannot tell. You can optionally describe the yes case and the no case in `criteria`.

The name is TypeSafe's own term. It is not a standard word.

### Writing criteria that work

- One label per real outcome. Labels must be mutually exclusive.
- Describe each label in plain words a new hire could apply. The description is what Jev matches against, not the label name.
- For Score, make each level concrete. "Frustrated but civil" beats "medium."
- Do not put the answer in the instructions. Ask the question, then let the criteria define the options.

---

## 4. Confidence, and what to do with it

Most people read the answer and skip the number next to it. The number is the product.

For Choice and Score, `confidence` collapses the whole probability distribution into one number from 0 to 1. All the mass on one option gives 1.0. The more evenly it spreads, the lower it goes. TypeSafe's docs say plainly that you are not locked into their definition. You get the full `probabilities`, so you can compute your own measure if the built-in one does not fit.

TypeSafe's guidance is a three-band split:

- **High confidence.** Act automatically.
- **Medium confidence.** Proceed with a check. Confirm with the user, or add a second signal.
- **Low confidence.** Do not act. Route to a person.

The part that matters: a threshold is not one number for the whole system. Each action gets its own bar based on what happens when the answer is wrong. Reading a balance back to the wrong customer is annoying. Moving money on a wrong read is a lawsuit. TypeSafe's own example uses 0.6 as the floor for any action and requires above 0.85 before a transfer runs without confirmation.

Start conservative. Run your real data through. Adjust when you see where the misses land.

---

## 5. What goes in state

State is the content Jev evaluates. Three shapes:

- **A string.** One message, one passage. Fine for simple cases.
- **An object.** Labeled fields. Best for most real decisions. A refund request, the order it refers to, and the refund policy can all go in as separate keys, and the question can ask whether the request fits the policy.
- **An array.** A conversation thread or a list of records.

Rules from the docs that will save you a bad week:

- Text only. No images, audio, or video.
- English is the primary language. Other languages run at lower accuracy today.
- Keep content in state and questions in questions. Do not stuff instructions into the state.
- Send only what the decision needs. Accuracy falls as unrelated content grows.

---

## 6. First call

The official quickstart, run as a script. Same ticket, three questions, one round trip.

[scripts/quickstart.py](scripts/quickstart.py)

```bash
cd scripts
export TYPESAFE_API_KEY="sk-..."
python3 quickstart.py
```

[scripts/quickstart.ts](scripts/quickstart.ts)

```bash
cd scripts
npm install @typesafe-ai/sdk
export TYPESAFE_API_KEY="sk-..."
npx tsx quickstart.ts
```

The ticket:

```
Hi, I've been trying to connect my Stripe account for 3 days and the
integration keeps failing. I'm losing sales. Please help ASAP.
```

The questions: `department` (Choice: billing, technical, sales), `frustration` (Score: three levels), `is_urgent` (Noul).

The response, from TypeSafe's docs:

```json
{
  "model": "jev-1.13.0",
  "answers": {
    "department": {
      "type": "choice",
      "choice": "technical",
      "confidence": 0.78,
      "probabilities": { "technical": 0.85, "sales": 0.0, "billing": 0.15 }
    },
    "frustration": {
      "type": "score",
      "score": 1.0,
      "confidence": 1.0,
      "legend": { "0": "Calm, just stating facts", "1": "Frustrated but civil", "2": "Very angry, strong language" },
      "probabilities": { "0": 0.0, "1": 1.0, "2": 0.0 }
    },
    "is_urgent": { "type": "noul", "noul": 1.0 }
  },
  "usage": { "input_tokens": 392, "output_tokens": 65 }
}
```

Reading it:

- **department** went to technical at 0.85, with 0.15 on billing because Stripe is a payment tool. Confidence 0.78 reflects that split.
- **frustration** landed on level 1, frustrated but civil, with nothing on the other levels. Confidence 1.0.
- **is_urgent** is 1.0. The message says "ASAP" and "losing sales."

The script then does the only thing that matters: it routes on the numbers. Technical plus urgent goes to on-call. Everything else waits in the standard queue.

> [!TIP]
> **Run the quickstart with your own ticket before you write anything else.** Swap the text, keep the questions, watch the probabilities move. Ten minutes of this teaches you more about criteria writing than any doc.

---

## 7. Five patterns

Four of these are TypeSafe's documented patterns. The fifth, tool-call risk gating, is the pattern LangChain built into its harness and the job Vercel described handing to Jev. Each one is a runnable script under [scripts/patterns/](scripts/patterns/).

### Pattern 1: Intent routing

**Scenario:** Customer messages arrive from a form, a chat widget, and email. Each one needs to reach a handler without a language model reading every single message.

**The script:** [scripts/patterns/intent_routing.py](scripts/patterns/intent_routing.py)

```python
questions = {
    "intent": Choice(
        instructions="The primary intent of this customer message",
        criteria={
            "order_status": "Asking about an existing order",
            "product_question": "Asking about a product before buying",
            "return_exchange": "Wants to return or exchange something",
            "complaint": "Unhappy with the experience, wants a resolution",
        },
    ),
    "complexity": Score(
        instructions="How complex is this request to resolve",
        criteria=[
            "Simple lookup or standard procedure",
            "Requires some judgment or a multi-step process",
            "Unusual situation, edge case, or escalation needed",
        ],
    ),
}
```

**What happens:**

- One call returns the intent and a complexity level.
- Below 0.5 confidence on intent, the message goes to a person.
- Complexity above 1.5 goes to a person even when the intent is clear.
- Otherwise the intent picks the handler: a lookup bot, an FAQ agent, the returns workflow, or the human queue for complaints.

**Expected outcome:** Most messages never touch a language model. The ones that do are the ones that need one.

> [!TIP]
> **Pair every Choice with a complexity Score.** Intent tells you where. Complexity tells you whether a machine should be the one to go there.

### Pattern 2: Confidence-gated routing

**Scenario:** A banking assistant handles balance checks, transfers, and fraud reports. Each of those has a different cost when the classifier is wrong.

**The script:** [scripts/patterns/confidence_gated_routing.py](scripts/patterns/confidence_gated_routing.py)

```python
FLOOR = 0.6
TRANSFER_AUTO = 0.85

if action.confidence < FLOOR:
    route_to_support_agent()
elif action.choice == "check_balance":
    show_balance()                       # low stakes, floor is enough
elif action.choice == "approve_transfer":
    if action.confidence > TRANSFER_AUTO:
        approve_transfer()               # high stakes, high confidence
    else:
        ask_user_to_confirm()            # high stakes, medium confidence
elif action.choice == "report_fraud":
    escalate_to_fraud_team()             # never automated
```

**What happens:**

- One Choice question, one confidence number.
- The floor catches genuine uncertainty across every action.
- Each action above the floor gets its own bar. Reads act at 0.6. Transfers need 0.85 or a confirmation step.
- Fraud reports go to a person no matter what the number says.

**Expected outcome:** The same classifier is safe for money movement and cheap for balance reads, because the threshold moved, not the model.

> [!TIP]
> **Write the "never automate" list first.** It is shorter than the threshold table and it is the part you will regret skipping.

### Pattern 3: Speculative fan-out

**Scenario:** A support ticket might be a bug, a billing issue, or a feature request. The old flow asks "what is it," waits, then asks the follow-up. Two round trips minimum.

**The script:** [scripts/patterns/speculative_fan_out.py](scripts/patterns/speculative_fan_out.py)

```python
questions = {
    "category": Choice(...),               # bug_report, billing, feature_request, question
    "bug_severity": Score(...),            # only used if category is bug_report
    "has_reproducible_steps": Noul(...),   # only used if category is bug_report
    "refund_requested": Noul(...),         # only used if category is billing
    "frustration": Score(...),             # always used
}
```

**What happens:**

- Every question you might need goes in one call, including the ones you probably will not use.
- TypeSafe's docs: all questions are evaluated in parallel, so adding more usually has little effect on response time.
- Your code reads only the answers that apply. A bug with severity above 1.5 and reproducible steps above 0.6 escalates to engineering. A billing ticket with refund above 0.7 gets flagged.
- Frustration above 1.5 adds "a human replies first" to any path.

**Expected outcome:** One round trip instead of two or three, and the branching moves into your code where you can read it.

> [!TIP]
> **Ask the speculative questions with a specific "if" in the instructions.** "If this is a bug, how severe is it" gives Jev the frame it needs when the ticket is not a bug at all.

### Pattern 4: Composite scoring

**Scenario:** Inbound leads need a priority. No single question captures it. Fit, budget, urgency, and authority all matter, and they matter differently depending on what you are optimizing for.

**The script:** [scripts/patterns/composite_scoring.py](scripts/patterns/composite_scoring.py)

```python
fit       = answers["fit"].score / 4
budget    = answers["budget"].score / 4
urgency   = answers["urgency"].score / 4
authority = answers["authority"].score / 4

priority_score = (0.40 * fit) + (0.30 * budget) + (0.15 * urgency) + (0.15 * authority)
speed_score    = (0.20 * fit) + (0.20 * budget) + (0.45 * urgency) + (0.15 * authority)
```

**What happens:**

- Four Score questions, each a five-level rubric from 0 to 4, all in one call.
- Each answer is divided by the top level so every dimension sits on 0 to 1.
- Two different weightings produce two different rankings from the same answers. No second API call.
- Thresholds on the composite pick the action: book today, offer two times this week, or nurture.

**Expected outcome:** A lead score you can explain, because every input is a rubric level you wrote and every weight is a number you chose.

> [!TIP]
> **When the ranking looks wrong, change the weights, not the rubrics.** The rubrics are the measurement. The weights are the opinion. Keep them separate and you can tune one without breaking the other.

### Pattern 5: Tool-call risk gating

**Scenario:** An agent is about to run a shell command. Before it does, something fast and cheap should decide whether the command is destructive, and whether it is actually what the user asked for. This is the job LangChain's `AutoModeMiddleware` gives to Jev, and the job Vercel described moving from an OpenAI classifier to Jev.

**The script:** [scripts/patterns/tool_call_risk_gate.py](scripts/patterns/tool_call_risk_gate.py)

```python
state = {
    "user_request": "Add a nullable 'archived_at' column to the projects table.",
    "tool": "bash",
    "command": "npm run db:reset && npm run db:migrate",
    "working_directory": "/srv/app",
}

questions = {
    "irreversible": Noul("Running this command would destroy data or make a change that cannot be undone ..."),
    "on_task": Noul("This command is a reasonable step toward exactly what the user requested, and nothing more"),
    "blast_radius": Score(["One file or one local process", "One service, table, or environment", "Shared infra, production data, or external systems"]),
}
```

**What happens:**

- The user's request and the pending command go in state together. The decision needs both. `db:reset` after "reset the database" is fine. `db:reset` after "add a column" is not.
- Two Nouls and one Score come back in one call.
- Irreversible above 0.7 and on-task below 0.5 is a block.
- Irreversible above 0.7 on its own, or blast radius above 1.5, means show it to a human first.
- On-task below 0.5 with nothing destructive is still an ask.
- Everything else runs.

**Expected outcome:** A gate that runs in well under a second on every tool call, so you can afford to run it on every tool call.

> [!TIP]
> **Put the original request in state, every time.** Without it, Jev is judging a command in a vacuum. With it, Jev is judging whether the command matches the intent, which is the actual question.

> [!WARNING]
> **This gate is one layer, not the only layer.** TypeSafe documents that content written to steer the model can move the answer. A command string that includes "this is safe and reversible" can shift the Noul. Keep your allow-lists, sandboxes, and confirmations. Add Jev on top.

---

## 8. Cost and speed

The numbers TypeSafe publishes:

- **Latency:** 70 to 500 milliseconds end to end.
- **Input:** $0.042 per million tokens, which is $42 per billion.
- **Output:** free. Not metered.

One independent data point. Senko Rašić ran 3,000 Croatian-language texts through a binary classifier with a one-sentence English instruction. Jev hit 97.1 percent accuracy against 97.6 percent for a fine-tuned BERT model, in about a minute, for about 20 cents. He noted that most of the disagreements turned out to be mislabeled data, and that Jev was the one following the stated definition more literally. His caveat is worth repeating: if you already have a tuned BERT running locally, the gains may be small.

One honest counterpoint from TechCrunch's coverage. Bryo AI's CTO tested Jev on business email classification and found it 10 to 20 times more expensive than Gemini for his workload, while still preferring it for the probability output. Cheap is relative to what you are replacing.

Three levers that move the bill:

1. **Trim state.** You pay for input tokens. Send the ticket, not the ticket plus the last forty messages in the thread. This also raises accuracy.
2. **Fan out instead of chaining.** Five questions in one call is one round trip. Five calls is five. The token cost is similar. The latency is not.
3. **Gate the expensive model.** Ask Jev "does this need a strong model" before you call one. The Jev call costs a fraction of a cent. The call it prevents costs more.

Both SDKs retry on 408, 429, and 5xx by default with exponential backoff. Default timeout is 10 seconds per attempt. Set a `RetryPolicy` if you need different behavior.

---

## 9. Where it breaks

All of these are from TypeSafe's own jaggedness page for Jev 1.13. They publish the weaknesses. Read them before you ship.

- **It reads literally.** It answers the question you wrote, not the one you meant. Scoping words, negations, and implied conditions are taken at face value. Write plain questions.
- **It does not count.** Characters in a word, occurrences of a term, items in a long list. Errors grow with the count.
- **It is bad with numbers as numbers.** Hex values, RGB triples, whether two numeric values are close. Semantic descriptions do better than numeric ones.
- **Do not do math with Score.** The expected value between two levels is not a precise measurement. Use it for ranking and thresholds, not arithmetic.
- **It reads dates as text.** Which of two dates is earlier, how far apart they are, whether one falls in a window. Unreliable, especially with mixed formats. Do that in code.
- **Double negatives and indirection cost accuracy.** A question about a property of a property is harder than a direct one.
- **Irrelevant context lowers accuracy.** Unrelated material in state acts as a distractor.
- **Adversarial content can move the answer.** Text written to argue for its own label can shift the output. Do not use Jev as the only line of defense on anything security-related.
- **Contradictory instructions confuse it.** If the instructions and the criteria disagree, expect noise.
- **Answers across question types are not guaranteed consistent.** TypeSafe's example: "is the customer seeking a refund" as a Noul returned 0.22, while the same idea as a Choice returned 0.99 confidence on "no." Pick one framing per decision and test it.
- **It cannot generate text.** You can force it. It will be bad and slow. That is not what it is for.

---

## 10. Troubleshooting

**The client raises an authentication error on the first call.**
- Cause: `TYPESAFE_API_KEY` is not set in the shell that ran the script, or it has whitespace around it.
- Fix: `echo $TYPESAFE_API_KEY` in the same terminal. The Python SDK strips whitespace and newlines from the key. It does not fix a missing one.

**Confidence is low on almost everything.**
- Cause: the criteria overlap, or the descriptions are vague enough that two labels fit most inputs.
- Fix: rewrite the descriptions so each one names a concrete situation. Run ten real examples and look at `probabilities`, not just `choice`. The spread tells you which two labels are fighting.

**The Score comes back as 1.4 and the code expected an integer.**
- Cause: `score` is an expected value and can sit between levels.
- Fix: threshold on it (`score > 1.5`) or round it. Do not compare with `==`.

**The TypeScript quickstart fails with an error about async modules or top-level await.**
- Cause: the file was run in a project without `"type": "module"` in package.json.
- Fix: the shipped script wraps the call in an async `main()` so it runs in either mode. If you copied only the body, wrap it, or add `"type": "module"`.

**Accuracy drops on long inputs.**
- Cause: unrelated content in state. This is documented behavior.
- Fix: send the fields the decision needs and nothing else. Use an object with labeled keys instead of one long string.

**A Noul and a Choice on the same idea disagree.**
- Cause: documented. Question types are not guaranteed to agree with each other.
- Fix: pick one framing per decision. Test it on your data. Do not ask the same thing twice and average.

**Requests fail with 429.**
- Cause: rate limit. Both SDKs retry 429 by default with backoff and honor `Retry-After`.
- Fix: if retries are exhausted, slow the caller. TypeSafe does not publish rate limits in the docs as of this writing, so measure your own ceiling.

**The Claude Code plugin installed but Claude still writes the calls wrong.**
- Cause: the skill is not being triggered, or the session started before the install.
- Fix: start a new session. Name the skill in the prompt: "Use the TypeSafe skill to write this."

---

## 11. Quick reference

**Install**

```bash
pip install typesafe-sdk                 # Python 3.10+
npm install @typesafe-ai/sdk             # Node 20+
export TYPESAFE_API_KEY="sk-..."
```

**Claude Code plugin**

```bash
claude plugin marketplace add typesafe-ai/skills
claude plugin install typesafe@typesafe-ai
```

**Python, minimum call**

```python
from typesafe_sdk import Choice, Noul, Score, TypeSafeClient

client = TypeSafeClient()                      # reads TYPESAFE_API_KEY
r = client.system_one(
    state="I was charged twice. Please fix this ASAP.",
    questions={
        "category": Choice(instructions="What is this about", criteria={"billing": None, "technical": None, "other": None}),
        "anger": Score(instructions="How angry", criteria=["calm", "annoyed", "furious"]),
        "urgent": Noul(instructions="The message is urgent"),
    },
)
r.answers["category"].choice            # "billing"
r.answers["category"].confidence        # 0..1
r.answers["category"].probabilities     # {"billing": 0.9, ...}
r.answers["anger"].score                # expected level, may be fractional
r.answers["urgent"].noul                # 0..1
```

**TypeScript, minimum call**

```ts
import { choice, noul, score, TypeSafeClient } from "@typesafe-ai/sdk";

const client = new TypeSafeClient();
const r = await client.systemOne({
  state: "I was charged twice. Please fix this ASAP.",
  questions: {
    category: choice("What is this about", { billing: null, technical: null, other: null }),
    anger: score("How angry", ["calm", "annoyed", "furious"]),
    urgent: noul("The message is urgent"),
  },
});
```

**Answer fields**

- Choice: `choice`, `confidence`, `probabilities`
- Score: `score`, `confidence`, `legend`, `probabilities`
- Noul: `noul`

**Environment variables**

- `TYPESAFE_API_KEY` required
- `TYPESAFE_DEFAULT_MODEL` defaults to `jev-latest`
- `TYPESAFE_BASE_URL` defaults to `https://api.typesafe.ai`
- `TYPESAFE_LOG_LEVEL` defaults to `warn`

**Endpoint**

- `POST https://api.typesafe.ai/v1/systemone`
- Body: `{ state, questions, model }`
- Model string in responses today: `jev-1.13.0`

**Threshold starting points, from TypeSafe's examples**

- Floor for any automated action: 0.6
- High-stakes automatic action: above 0.85
- Anything below the floor: a person

**Files in this folder**

- [scripts/quickstart.py](scripts/quickstart.py) and [scripts/quickstart.ts](scripts/quickstart.ts)
- [scripts/patterns/intent_routing.py](scripts/patterns/intent_routing.py)
- [scripts/patterns/confidence_gated_routing.py](scripts/patterns/confidence_gated_routing.py)
- [scripts/patterns/speculative_fan_out.py](scripts/patterns/speculative_fan_out.py)
- [scripts/patterns/composite_scoring.py](scripts/patterns/composite_scoring.py)
- [scripts/patterns/tool_call_risk_gate.py](scripts/patterns/tool_call_risk_gate.py)
- [templates/decision-spec.md](templates/decision-spec.md)
- [templates/env.example](templates/env.example)

---

## Sources

All checked September 29, 2026.

- [Introducing System One Models and Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev), TypeSafe AI blog. Latency, pricing, release date.
- [Quickstart](https://docs.typesafe.ai/introduction/quickstart), TypeSafe docs. The ticket example and response.
- [Primitives](https://docs.typesafe.ai/primitives), TypeSafe docs. Choice, Score, Noul and their return fields.
- [Confidence](https://docs.typesafe.ai/confidence), TypeSafe docs. Definition and threshold guidance.
- [State](https://docs.typesafe.ai/concepts/state), TypeSafe docs. What goes in and what does not.
- [Patterns](https://docs.typesafe.ai/patterns), TypeSafe docs. [Intent routing](https://docs.typesafe.ai/patterns/intent-routing), [confidence-gated routing](https://docs.typesafe.ai/patterns/confidence-routing), [speculative fan-out](https://docs.typesafe.ai/patterns/fan-out), [composite scoring](https://docs.typesafe.ai/patterns/composite-scoring).
- [Jev 1.13 jaggedness](https://docs.typesafe.ai/model-jaggedness/jev-1.13), TypeSafe docs. Every item in section 9.
- [Python SDK](https://docs.typesafe.ai/sdk/python) and [JavaScript SDK](https://docs.typesafe.ai/sdk/javascript), TypeSafe docs. Client options, env vars, retries.
- [typesafe-ai/skills](https://github.com/typesafe-ai/skills), GitHub. Plugin install commands.
- [A new kind of AI model from a ChatGPT inventor is thrilling developers](https://techcrunch.com/2026/09/18/a-new-kind-of-ai-model-from-a-chatgpt-inventor-is-thrilling-developers/), TechCrunch, September 18, 2026. Vercel and Bryo AI quotes, Almeida background, the API outage.
- [Building a harness with Jev](https://www.langchain.com/blog/building-a-harness-with-jev), LangChain, September 17, 2026. `langchain-typesafe`, `TypeSafeClassifier`, `AutoModeMiddleware`.
- [Analyzing Jev, a new AI model](https://blog.senko.net/analyzing-jev-a-new-ai-model), Senko Rašić, September 22, 2026. The 3,000-text comparison.

---

Built by OperatorOS | [operatoros.ai](https://operatoros.ai)
Follow [@daviss.dev](https://instagram.com/daviss.dev) and [@os.operator](https://instagram.com/os.operator) for production-grade AI guides.
Patterns 1 through 4 are TypeSafe's documented patterns. Pattern 5 is adapted from LangChain's harness work.
