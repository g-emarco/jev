"""Gemini through LangChain: a decision as a typed, validated object (no probabilities)."""

from typing import Literal

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field

from jev_demo.models import ARGON_ID

load_dotenv()


class TicketDecision(BaseModel):
    team: Literal["infra", "billing", "other"]
    urgent: bool
    reason: str = Field(description="One sentence justifying the choice.")


model = ChatGoogleGenerativeAI(model=ARGON_ID, vertexai=True, temperature=0)
decider = model.with_structured_output(TicketDecision)

decision = decider.invoke("Checkout returns 500 for every customer since the 14:00 deploy.")
print(decision)
# Schema-valid is not the same as correct, and there is no confidence to gate on.
# Compare with examples/jev/01_classifier_basics.py, which returns calibrated probabilities.
