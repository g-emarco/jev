"""Measure decisions before trusting them: Jev vs Gemini structured output on one dataset."""

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_typesafe import Choice, TypeSafeClassifier

from jev_demo.evaluation import evaluate
from jev_demo.gating import QUESTIONS

from jev_demo.models import ARGON_ID

load_dotenv()

DATASET = [
    ("Checkout returns 500 for every customer.", "infra"),
    ("The deploy rolled back twice overnight.", "infra"),
    ("Why was I charged twice this month?", "billing"),
    ("My invoice shows the wrong VAT number.", "billing"),
    ("Do you have a dark mode?", "other"),
]
LABELS = ("infra", "billing", "other")

jev = TypeSafeClassifier()
gemini = ChatGoogleGenerativeAI(model=ARGON_ID, vertexai=True, temperature=0).with_structured_output(
    {"title": "Team", "type": "object", "properties": {"team": {"enum": list(LABELS)}}, "required": ["team"]}
)


def jev_team(text: str) -> str:
    return jev.invoke({"state": text, "questions": {"team": QUESTIONS["team"]}}).choices["team"].choice


def gemini_team(text: str) -> str:
    return gemini.invoke(f"Which team should handle this? {text}")["team"]


for name, fn in [("jev", jev_team), ("gemini", gemini_team)]:
    print(name, evaluate(fn, DATASET))
