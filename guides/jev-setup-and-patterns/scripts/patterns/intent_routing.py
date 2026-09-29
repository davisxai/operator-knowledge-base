# Usage: export TYPESAFE_API_KEY="sk-..." && python3 intent_routing.py
# Pattern 1. Classify what the message wants, then send it to the right handler.
# Source pattern: https://docs.typesafe.ai/patterns/intent-routing

from typesafe_sdk import Choice, Score, TypeSafeClient

MESSAGE = (
    "I ordered the black hoodie two weeks ago and it still hasn't shipped. "
    "Order number 48211. Can you tell me what's going on?"
)

INTENT = Choice(
    instructions="The primary intent of this customer message",
    criteria={
        "order_status": "Asking about an existing order",
        "product_question": "Asking about a product before buying",
        "return_exchange": "Wants to return or exchange something",
        "complaint": "Unhappy with the experience, wants a resolution",
    },
)

COMPLEXITY = Score(
    instructions="How complex is this request to resolve",
    criteria=[
        "Simple lookup or standard procedure",
        "Requires some judgment or a multi-step process",
        "Unusual situation, edge case, or escalation needed",
    ],
)


def handle_order_status(message: str) -> str:
    return "order-status bot: look up the order and reply with tracking"


def handle_product_question(message: str) -> str:
    return "product FAQ agent"


def handle_return(message: str) -> str:
    return "returns workflow"


def handle_human(message: str, reason: str) -> str:
    return f"human queue ({reason})"


def main() -> None:
    client = TypeSafeClient()
    response = client.system_one(
        state=MESSAGE,
        questions={"intent": INTENT, "complexity": COMPLEXITY},
    )

    intent = response.answers["intent"]
    complexity = response.answers["complexity"]

    print(f"intent:     {intent.choice} (confidence {intent.confidence:.2f})")
    print(f"complexity: {complexity.score:.1f} (confidence {complexity.confidence:.2f})")

    # Floor: anything the model is unsure about goes to a person.
    if intent.confidence < 0.5:
        route = handle_human(MESSAGE, "low confidence on intent")
    # Edge cases go to a person even when the intent is clear.
    elif complexity.score > 1.5:
        route = handle_human(MESSAGE, "high complexity")
    elif intent.choice == "order_status":
        route = handle_order_status(MESSAGE)
    elif intent.choice == "product_question":
        route = handle_product_question(MESSAGE)
    elif intent.choice == "return_exchange":
        route = handle_return(MESSAGE)
    else:
        route = handle_human(MESSAGE, "complaint")

    print(f"route:      {route}")


if __name__ == "__main__":
    main()
