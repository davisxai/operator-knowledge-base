# Usage: export TYPESAFE_API_KEY="sk-..." && python3 composite_scoring.py
# Pattern 4. Score several independent dimensions, then weight them into one number you control.
# Source pattern: https://docs.typesafe.ai/patterns/composite-scoring

from typesafe_sdk import Score, TypeSafeClient

LEAD = {
    "company": "Harbor Dental Group",
    "form_message": (
        "We run four dental offices in the Tampa area. Front desk spends most of the "
        "day on the phone confirming appointments. We tried a scheduling app last year "
        "and dropped it. Looking for someone to handle after-hours calls and reminders. "
        "Budget is around 3k a month if it actually works. Can we talk this week?"
    ),
    "source": "website contact form",
}

# Every dimension is its own rubric, scored 0 to 4. Keep the levels concrete.
QUESTIONS = {
    "fit": Score(
        instructions="How well does this lead's problem match a voice agent or automation build",
        criteria=[
            "No clear problem stated",
            "Vague interest in AI or automation",
            "A real process is named but not the pain",
            "A specific repetitive process with a stated pain",
            "A specific process, stated pain, and a clear outcome they want",
        ],
    ),
    "budget": Score(
        instructions="How much budget signal is in the message",
        criteria=[
            "No mention of money",
            "Asks what it costs",
            "Hints at a range or a comparison to a current tool",
            "States a number or range",
            "States a number that fits a retainer and says they will pay for results",
        ],
    ),
    "urgency": Score(
        instructions="How soon does this lead want to move",
        criteria=[
            "No timing mentioned",
            "Someday, exploring",
            "Within a few months",
            "This month",
            "This week or immediately",
        ],
    ),
    "authority": Score(
        instructions="How likely is the sender the decision maker",
        criteria=[
            "Unclear who is writing",
            "Employee gathering info for someone else",
            "Manager with influence but not final say",
            "Owner or executive speaking for the business",
            "Owner or executive who already states they can commit budget",
        ],
    ),
}

MAX_LEVEL = 4


def main() -> None:
    client = TypeSafeClient()
    response = client.system_one(state=LEAD, questions=QUESTIONS)
    a = response.answers

    # Normalize each dimension to 0..1 so the weights mean what they say.
    fit = a["fit"].score / MAX_LEVEL
    budget = a["budget"].score / MAX_LEVEL
    urgency = a["urgency"].score / MAX_LEVEL
    authority = a["authority"].score / MAX_LEVEL

    for name, value in (("fit", fit), ("budget", budget), ("urgency", urgency), ("authority", authority)):
        print(f"{name:10} {value:.2f}")

    # Two different weightings of the same four answers. No second API call needed.
    priority_score = (0.40 * fit) + (0.30 * budget) + (0.15 * urgency) + (0.15 * authority)
    speed_score = (0.20 * fit) + (0.20 * budget) + (0.45 * urgency) + (0.15 * authority)

    print(f"priority   {priority_score:.2f}")
    print(f"speed      {speed_score:.2f}")

    if priority_score >= 0.7:
        print("action:    book a call today")
    elif priority_score >= 0.45:
        print("action:    reply with two times this week")
    else:
        print("action:    nurture sequence")


if __name__ == "__main__":
    main()
