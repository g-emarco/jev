"""An LLM always acts. Jev lets you escalate to a human when it is unsure."""

from typing import Literal

from dotenv import load_dotenv
from langchain_typesafe import TypeSafeClassifier
from pydantic import BaseModel

from jev_demo.gating import QUESTIONS, decide
from jev_demo.models import gemini
from jev_demo.present import act, pause

load_dotenv()

TICKETS = {
    "clear": "The deploy failed twice and customers are seeing 500s. Can someone look now?",
    "ambiguous": "Customer says the invoice page is down, so they can't pay. Probably the payment API?",
    "dark mode": "Do you have a dark mode?",
}


class Route(BaseModel):
    team: Literal["infra", "billing", "other"]


act(1, "the LLM way: three runs each at temperature 1, always routes")
router = gemini(Route, temperature=1)
for name, ticket in TICKETS.items():
    teams = [router.invoke(f"Which team should handle this? {ticket}").team for _ in range(3)]
    print(f"{name:10} auto_route, teams across runs: {teams}")

pause()

act(2, "the decision-model way: act only when confident")
classifier = TypeSafeClassifier()
for name, ticket in TICKETS.items():
    response = classifier.invoke({"state": ticket, "questions": QUESTIONS})
    team = response.choices["team"]
    decision = decide(response)
    print(f"{name:10} {decision.action}, team: {team.choice}, confidence: {team.confidence:.2f}")

print("\nTakeaway: same tickets, but only Jev can say 'I am not sure, ask a human'.")
