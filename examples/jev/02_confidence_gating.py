"""Decide act / escalate from probabilities, not from a model's prose."""

from dotenv import load_dotenv
from langchain_typesafe import TypeSafeClassifier

from jev_demo.gating import QUESTIONS, decide

load_dotenv()

classifier = TypeSafeClassifier()
messages = [
    "Checkout returns 500 for every customer since the 14:00 deploy.",
    "Why was I charged twice this month?",
    "Do you have a dark mode?",
]
for text in messages:
    decision = decide(classifier.invoke({"state": text, "questions": QUESTIONS}))
    print(f"{decision.action:13} team={decision.team:8} {decision.reason} <- {text}")
