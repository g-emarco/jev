"""Jev returns typed answers with probabilities: Noul (yes/no), Choice, Score."""

from dotenv import load_dotenv
from langchain_typesafe import TypeSafeClassifier

from jev_demo.gating import QUESTIONS

load_dotenv()

classifier = TypeSafeClassifier()  # reads TYPESAFE_API_KEY; model defaults to "jev-latest"
response = classifier.invoke(
    {
        "state": "The deploy failed twice and customers are seeing 500s. Can someone look now?",
        "questions": QUESTIONS,
    }
)

print("urgent probability:", response.nouls["urgent"].noul)
team = response.choices["team"]
print("team:", team.choice, "| confidence:", team.confidence, "|", team.probabilities)
severity = response.scores["severity"]
print("severity (expected level):", severity.score, "|", severity.probabilities)
print("tokens:", response.usage, "| request id:", response.request_id)
