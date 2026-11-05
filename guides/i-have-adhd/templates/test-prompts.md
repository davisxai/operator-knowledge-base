# Test prompts

Run each prompt once with the skill off and once with `/i-have-adhd` on. Compare the first line and the last line of each reply.

1. Multi-step task
   `Walk me through adding a new column to my users table and backfilling it.`
   Look for: numbered steps, one action each, "step N of M done" on the next turn.

2. Error report
   `My tests fail with "expected 200, got 401" in auth.spec.ts. What's wrong?`
   Look for: location, cause, and fix in the first lines. No "uh oh".

3. Time estimate
   `How long will it take to add rate limiting to my API?`
   Look for: a number in minutes or hours, with the condition it depends on.

4. Tangent bait
   `Fix the broken login redirect. Also my README is old.`
   Look for: the redirect fixed first, the README offered as a separate question at the end.

5. Plain question
   `How do I create an empty Git repository in a new folder?`
   Look for: the command first, nothing before it, nothing after the next action.

Turn it off with `stop adhd mode` or `normal mode`.
