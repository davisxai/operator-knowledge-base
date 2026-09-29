# Usage: export TYPESAFE_API_KEY="sk-..." && python3 speculative_fan_out.py
# Pattern 3. Ask every question you might need in one call. Decide in code which answers matter.
# Source pattern: https://docs.typesafe.ai/patterns/fan-out

from typesafe_sdk import Choice, Noul, Score, TypeSafeClient

TICKET_ID = "T-7710"

TICKET = {
    "subject": "App crashes when I open the export screen",
    "body": (
        "Every time I tap Export on iOS 19.1 the app closes. Steps: open a project, "
        "tap the share icon, tap Export as PDF. Happens 10 out of 10 times. "
        "I pay for the Pro plan and this is the main thing I use it for."
    ),
}

# Questions about a bug and questions about billing both go in the same call.
# Jev evaluates them in parallel, so the extra questions cost little time.
QUESTIONS = {
    "category": Choice(
        instructions="What kind of ticket is this",
        criteria={
            "bug_report": "Something is broken or behaving incorrectly",
            "billing": "Charges, plans, refunds, invoices",
            "feature_request": "Asking for something the product does not do",
            "question": "Asking how to do something that already works",
        },
    ),
    "bug_severity": Score(
        instructions="If this is a bug, how severe is it",
        criteria=[
            "Cosmetic or minor annoyance",
            "A feature is degraded but there is a workaround",
            "A core feature is unusable or data is at risk",
        ],
    ),
    "has_reproducible_steps": Noul(
        instructions="The message includes clear steps to reproduce the problem",
    ),
    "refund_requested": Noul(
        instructions="The customer is asking for money back",
    ),
    "frustration": Score(
        instructions="How frustrated the customer appears",
        criteria=[
            "Calm, just stating facts",
            "Frustrated but civil",
            "Very angry, strong language",
        ],
    ),
}


def main() -> None:
    client = TypeSafeClient()
    response = client.system_one(state=TICKET, questions=QUESTIONS)
    a = response.answers

    category = a["category"]
    severity = a["bug_severity"]
    repro = a["has_reproducible_steps"]
    refund = a["refund_requested"]
    frustration = a["frustration"]

    print(f"category:   {category.choice} ({category.confidence:.2f})")
    print(f"severity:   {severity.score:.1f}   repro: {repro.noul:.2f}   refund: {refund.noul:.2f}")
    print(f"frustration {frustration.score:.1f}")

    # Only the answers relevant to the category get used. The rest were cheap to ask.
    if category.choice == "bug_report":
        if severity.score > 1.5 and repro.noul > 0.6:
            action = f"escalate {TICKET_ID} to engineering as high severity"
        else:
            action = f"add {TICKET_ID} to the bug backlog"
    elif category.choice == "billing":
        if refund.noul > 0.7:
            action = f"route {TICKET_ID} to billing, flagged refund likely"
        else:
            action = f"route {TICKET_ID} to billing"
    elif category.choice == "feature_request":
        action = f"log {TICKET_ID} in the feature tracker"
    else:
        action = f"answer {TICKET_ID} from the help docs"

    if frustration.score > 1.5:
        action += ", and a human replies first"

    print(f"action:     {action}")


if __name__ == "__main__":
    main()
