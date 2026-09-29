# Usage: export TYPESAFE_API_KEY="sk-..." && python3 confidence_gated_routing.py
# Pattern 2. Gate each action on its own confidence threshold. Riskier action, higher bar.
# Source pattern: https://docs.typesafe.ai/patterns/confidence-routing

from typesafe_sdk import Choice, TypeSafeClient

ACCOUNT_ID = "acct_2291"

MESSAGE = "Move 4,000 from my savings to checking please, I need it today."

INTENT = Choice(
    instructions="What the customer is asking the banking assistant to do",
    criteria={
        "check_balance": "Wants to know a balance on one of their accounts",
        "approve_transfer": "Wants money moved between accounts or to someone else",
        "report_fraud": "Reports a charge or activity they did not authorize",
        "other": "Anything else",
    },
)

# Thresholds are per action, not one global number.
# Read operations can act at the floor. Money movement needs a much higher bar.
FLOOR = 0.6
TRANSFER_AUTO = 0.85


def main() -> None:
    client = TypeSafeClient()
    response = client.system_one(state=MESSAGE, questions={"intent": INTENT})
    action = response.answers["intent"]

    print(f"intent: {action.choice} (confidence {action.confidence:.2f})")
    print(f"probabilities: {action.probabilities}")

    if action.confidence < FLOOR:
        decision = "route to a support agent (below confidence floor)"

    elif action.choice == "check_balance":
        # Worst case is the user hears a balance they did not ask for. Low stakes.
        decision = f"show balance for {ACCOUNT_ID}"

    elif action.choice == "approve_transfer":
        if action.confidence > TRANSFER_AUTO:
            decision = f"approve transfer on {ACCOUNT_ID} automatically"
        else:
            decision = "ask the user to confirm before moving money"

    elif action.choice == "report_fraud":
        # Never automate this one. A person picks it up regardless of confidence.
        decision = "escalate to the fraud team"

    else:
        decision = "route to a support agent"

    print(f"decision: {decision}")


if __name__ == "__main__":
    main()
