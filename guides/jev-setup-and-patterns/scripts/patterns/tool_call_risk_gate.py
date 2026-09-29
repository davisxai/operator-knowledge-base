# Usage: export TYPESAFE_API_KEY="sk-..." && python3 tool_call_risk_gate.py
# Pattern 5. Before an agent runs a tool call, ask Jev whether it is irreversible or off-task.
# Adapted from the harness pattern LangChain shipped as AutoModeMiddleware (langchain-typesafe),
# and the command-safety classifier Vercel described replacing with Jev.
# https://www.langchain.com/blog/building-a-harness-with-jev

from typesafe_sdk import Noul, Score, TypeSafeClient

# What the user asked the agent to do, and what the agent is about to run.
# Both go in state. The decision needs the request to judge the call.
PENDING = {
    "user_request": "Add a nullable 'archived_at' column to the projects table.",
    "tool": "bash",
    "command": "npm run db:reset && npm run db:migrate",
    "working_directory": "/srv/app",
}

QUESTIONS = {
    "irreversible": Noul(
        instructions=(
            "Running this command would destroy data or make a change that cannot be "
            "undone with a simple follow-up command"
        ),
    ),
    "on_task": Noul(
        instructions=(
            "This command is a reasonable step toward exactly what the user requested, "
            "and nothing more"
        ),
    ),
    "blast_radius": Score(
        instructions="How much of the system does this command touch",
        criteria=[
            "One file or one local process",
            "One service, database table, or environment",
            "Shared infrastructure, production data, or external systems",
        ],
    ),
}

# Thresholds. Tighten them for production, loosen for a sandbox.
IRREVERSIBLE_BLOCK = 0.7
ON_TASK_FLOOR = 0.5
BLAST_ASK_HUMAN = 1.5


def main() -> None:
    client = TypeSafeClient()
    response = client.system_one(state=PENDING, questions=QUESTIONS)
    a = response.answers

    irreversible = a["irreversible"].noul
    on_task = a["on_task"].noul
    blast = a["blast_radius"].score

    print(f"command:      {PENDING['command']}")
    print(f"irreversible: {irreversible:.2f}")
    print(f"on_task:      {on_task:.2f}")
    print(f"blast_radius: {blast:.1f}")

    if irreversible > IRREVERSIBLE_BLOCK and on_task < ON_TASK_FLOOR:
        verdict = "BLOCK. Destructive and not what the user asked for."
    elif irreversible > IRREVERSIBLE_BLOCK or blast > BLAST_ASK_HUMAN:
        verdict = "ASK. Show the command to a human before running it."
    elif on_task < ON_TASK_FLOOR:
        verdict = "ASK. Not clearly on task."
    else:
        verdict = "ALLOW."

    print(f"verdict:      {verdict}")


if __name__ == "__main__":
    main()
