// Usage: export TYPESAFE_API_KEY="sk-..." && npx tsx quickstart.ts
// Same ticket, same three questions, TypeScript. Node 20 or newer.

import { choice, noul, score, TypeSafeClient } from "@typesafe-ai/sdk";

const ticket =
  "Hi, I've been trying to connect my Stripe account for 3 days and the " +
  "integration keeps failing. I'm losing sales. Please help ASAP.";

async function main(): Promise<void> {
  const client = new TypeSafeClient();

  const response = await client.systemOne({
    state: ticket,
    questions: {
      department: choice("Which team should handle this", {
        billing: "Payment or subscription issues",
        technical: "Bugs or integration problems",
        sales: "Pricing or account questions",
      }),
      frustration: score("How frustrated the customer appears", [
        "Calm, just stating facts",
        "Frustrated but civil",
        "Very angry, strong language",
      ]),
      is_urgent: noul("The message conveys urgency or time-sensitivity"),
    },
  });

  const { department, frustration, is_urgent } = response.answers;

  console.log(`model:       ${response.model}`);
  console.log(`department:  ${department.choice}  confidence=${department.confidence.toFixed(2)}`);
  console.log(`             probabilities=${JSON.stringify(department.probabilities)}`);
  console.log(`frustration: level ${frustration.score.toFixed(1)}  confidence=${frustration.confidence.toFixed(2)}`);
  console.log(`is_urgent:   ${is_urgent.noul.toFixed(2)}`);
  console.log(`usage:       ${response.usage.input_tokens} in / ${response.usage.output_tokens} out`);

  // Route on the numbers. The threshold is yours to set.
  if (department.choice === "technical" && is_urgent.noul > 0.8) {
    console.log("route: on-call engineer, top of queue");
  } else {
    console.log("route: standard queue");
  }
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
