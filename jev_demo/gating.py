"""Turn Jev's calibrated probabilities into an explicit act / escalate / refuse policy."""

from dataclasses import dataclass
from typing import Literal

from langchain_typesafe import Choice, ClassifierResponse, Noul, Score
from langchain_typesafe.types import Question

QUESTIONS: dict[str, Question] = {
    "urgent": Noul(instructions="Does this need attention right now?"),
    "team": Choice(
        instructions="Which team should pick this up?",
        criteria={
            "infra": "Deploys, availability, and on-call incidents.",
            "billing": "Payments, invoices, and subscriptions.",
            "other": "Anything that fits neither team.",
        },
    ),
    "severity": Score(
        instructions="How severe is the impact?",
        criteria=["Cosmetic.", "Degraded for some users.", "Full outage."],
    ),
}


@dataclass(frozen=True)
class Decision:
    action: Literal["auto_route", "page_oncall", "human_triage"]
    team: str
    reason: str


def decide(
    response: ClassifierResponse,
    *,
    min_confidence: float = 0.7,
    urgent_at: float = 0.8,
    outage_at: float = 1.5,
) -> Decision:
    """Pick an action. Low confidence always falls back to a human."""
    team = response.choices["team"]
    if team.confidence < min_confidence or team.choice == "other":
        return Decision("human_triage", team.choice, f"team confidence {team.confidence:.2f}")
    if response.nouls["urgent"].noul >= urgent_at and response.scores["severity"].score >= outage_at:
        return Decision("page_oncall", team.choice, "urgent and near full outage")
    return Decision("auto_route", team.choice, f"team confidence {team.confidence:.2f}")
