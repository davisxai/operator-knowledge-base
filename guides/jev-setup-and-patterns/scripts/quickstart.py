# Usage: export TYPESAFE_API_KEY="sk-..." && python3 quickstart.py
# One support ticket in, three typed decisions out, in one round trip.

from typesafe_sdk import Choice, Noul, Score, TypeSafeAPIError, TypeSafeClient

TICKET = (
    "Hi, I've been trying to connect my Stripe account for 3 days and the "
    "integration keeps failing. I'm losing sales. Please help ASAP."
)


def main() -> None:
    client = TypeSafeClient()

    try:
        response = client.system_one(
            state=TICKET,
            questions={
                "department": Choice(
                    instructions="Which team should handle this",
                    criteria={
                        "billing": "Payment or subscription issues",
                        "technical": "Bugs or integration problems",
                        "sales": "Pricing or account questions",
                    },
                ),
                "frustration": Score(
                    instructions="How frustrated the customer appears",
                    criteria=[
                        "Calm, just stating facts",
                        "Frustrated but civil",
                        "Very angry, strong language",
                    ],
                ),
                "is_urgent": Noul(
                    instructions="The message conveys urgency or time-sensitivity",
                ),
            },
        )
    except TypeSafeAPIError as error:
        print(f"API error {error.status} (request {error.request_id})")
        raise SystemExit(1)

    department = response.answers["department"]
    frustration = response.answers["frustration"]
    is_urgent = response.answers["is_urgent"]

    print(f"model:       {response.model}")
    print(f"department:  {department.choice}  confidence={department.confidence:.2f}")
    print(f"             probabilities={department.probabilities}")
    print(f"frustration: level {frustration.score:.1f}  confidence={frustration.confidence:.2f}")
    print(f"             legend={frustration.legend}")
    print(f"is_urgent:   {is_urgent.noul:.2f}")
    print(f"usage:       {response.usage.input_tokens} in / {response.usage.output_tokens} out")

    # Route on the numbers. The threshold is yours to set.
    if department.choice == "technical" and is_urgent.noul > 0.8:
        print("route: on-call engineer, top of queue")
    else:
        print("route: standard queue")


if __name__ == "__main__":
    main()
