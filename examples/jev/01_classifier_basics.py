"""One ticket, three questions. The LLM returns answers; Jev returns probabilities."""

from typing import Literal

from dotenv import load_dotenv
from langchain_typesafe import TypeSafeClassifier
from pydantic import BaseModel

from jev_demo.gating import QUESTIONS
from jev_demo.models import gemini
from jev_demo.present import act, pause

load_dotenv()

TICKET = "The deploy failed twice and customers are seeing 500s. Can someone look now?"


class Answers(BaseModel):
    urgent: bool
    team: Literal["infra", "billing", "other"]
    severity: Literal[0, 1, 2]


act(1, "the LLM way: three answers, zero probabilities")
print(gemini(Answers).invoke(f"Is it urgent, which team, and how severe (0-2)? {TICKET}"))

pause()

act(2, "the decision-model way: answers with probabilities")
response = TypeSafeClassifier().invoke({"state": TICKET, "questions": QUESTIONS})
team = response.choices["team"]
severity = response.scores["severity"]
print("urgent probability:", response.nouls["urgent"].noul)
print("team:", team.choice, "| confidence:", team.confidence, "|", team.probabilities)
print("severity (expected level):", severity.score, "|", severity.probabilities)
