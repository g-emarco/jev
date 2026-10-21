"""Batch finale: Gemini vs Jev on one labeled set. Confidence lets Jev act on the easy ones and escalate the rest."""

from dotenv import load_dotenv
from langchain_typesafe import TypeSafeClassifier

from jev_demo.gating import QUESTIONS
from jev_demo.models import gemini
from jev_demo.present import act, pause, timed

load_dotenv()

DATASET = [
    ("Checkout returns 500 for every customer.", "infra"),
    ("The deploy rolled back twice overnight.", "infra"),
    ("Why was I charged twice this month?", "billing"),
    ("My invoice shows the wrong VAT number.", "billing"),
    ("Do you have a dark mode?", "other"),
    ("Payment page times out for everyone.", "infra"),
    ("Customer says the invoice page is down, so they can't pay.", "infra"),
    ("Refund hasn't arrived after two weeks.", "billing"),
    ("Can I change my login email?", "other"),
    ("Subscription renewal failed with a gateway error.", "billing"),
]
MIN_CONFIDENCE = 0.7

llm = gemini({"title": "Team", "type": "object", "properties": {"team": {"enum": ["infra", "billing", "other"]}}, "required": ["team"]})
jev = TypeSafeClassifier()


def llm_team(text):
    return llm.invoke(f"Which team should handle this? {text}")["team"]


def jev_team(text):
    return jev.invoke({"state": text, "questions": {"team": QUESTIONS["team"]}}).choices["team"]


def run_llm():
    return [llm_team(text) for text, _ in DATASET]


def run_jev():
    return [jev_team(text) for text, _ in DATASET]


act(1, f"the LLM way: {len(DATASET)} sequential generations")
llm_teams, llm_seconds = timed(run_llm)
llm_correct = sum(team == label for team, (_, label) in zip(llm_teams, DATASET))
print(f"accuracy {llm_correct / len(DATASET):.0%} in {llm_seconds:.1f}s. It answered every item, so it escalated none.")

pause()

act(2, "the decision-model way: same items, with confidence")
answers, jev_seconds = timed(run_jev)
correct = sum(a.choice == label for a, (_, label) in zip(answers, DATASET))
confident = [(a, label) for a, (_, label) in zip(answers, DATASET) if a.confidence >= MIN_CONFIDENCE]
confident_correct = sum(a.choice == label for a, label in confident)
print(f"accuracy {correct / len(DATASET):.0%} in {jev_seconds:.1f}s")
print(f"acted on {len(confident)} items at confidence >= {MIN_CONFIDENCE}, accuracy on those: {confident_correct / len(confident):.0%}")
print(f"escalated {len(DATASET) - len(confident)} items to a human")

print("\nTakeaway: accuracy alone looks similar. Confidence is what lets you act on the easy ones and escalate the rest.")
