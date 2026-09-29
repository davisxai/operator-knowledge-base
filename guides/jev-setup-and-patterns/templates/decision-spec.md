# Decision spec: [name of the decision]

Fill this in before you write the call. One spec per decision point. If you cannot fill in the thresholds and fallback, the decision is not ready to automate.

## What is being decided

One sentence. Example: "Which queue a new support ticket lands in, and whether a human reads it first."

## State

What goes in. Only the content the decision needs. Label the fields.

- **Field:** description of what it holds
- **Field:** description of what it holds

Rules:
- Text only. No images, audio, or video.
- Keep unrelated content out. Extra material lowers accuracy.
- If the decision compares things (a request against a policy, a message against an order), put both in state under their own labels.

## Questions

One entry per question. Name, type, instructions, criteria.

### [question_name] (choice | score | noul)

- **Instructions:** the plain question, written so a new hire could answer it
- **Criteria:** (choice) label: description, one per option, mutually exclusive
- **Criteria:** (score) ordered levels from 0 upward, each one concrete
- **Criteria:** (noul) optional descriptions of the yes case and the no case

## Thresholds

One line per action. Riskier action, higher bar.

- **Act automatically when:** [answer] and confidence above [number]
- **Ask a person when:** confidence between [number] and [number], or [condition]
- **Never automate:** [answer], regardless of confidence

## Fallback

What happens when the call fails, times out, or returns low confidence on everything. Name the queue or the person.

## Test set

Ten to twenty real examples with the answer you expect. Run them before you ship, and again when you change the criteria.

- [example input] should return [expected answer]
- [example input] should return [expected answer]
