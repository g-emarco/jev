"""Routing to a model: an LLM router costs a whole generation. Jev routes with one classification."""

from typing import Literal

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_typesafe.experimental.middleware import ModelChoice, ModelRouterMiddleware
from pydantic import BaseModel

from jev_demo.models import DEFAULT, FAST, POWERFUL, gemini
from jev_demo.present import act, pause, timed

load_dotenv()

PROMPTS = [
    "What is the capital of France?",
    "Design a zero-downtime migration from a monolith to services.",
]


class Difficulty(BaseModel):
    level: Literal["fast", "powerful"]


def ask(agent, prompt):
    return agent.invoke({"messages": [{"role": "user", "content": prompt}]})


act(1, "the LLM way: pay for a routing call before the real call")
llm_router = gemini(Difficulty)
agents = {"fast": create_agent(FAST), "powerful": create_agent(POWERFUL)}
for prompt in PROMPTS:
    pick, routing_seconds = timed(llm_router.invoke, f"Does this need a fast or a powerful model? {prompt}")
    _, answer_seconds = timed(ask, agents[pick.level], prompt)
    print(f"{pick.level}: routing {routing_seconds:.1f}s + answer {answer_seconds:.1f}s <- {prompt}")

pause()

act(2, "the decision-model way: routing is a classification")
router = ModelRouterMiddleware(
    choices={
        "fast": ModelChoice(model=FAST, criteria="Direct lookups and simple, well-scoped questions."),
        "powerful": ModelChoice(model=POWERFUL, criteria="Architecture, multi-step reasoning, and ambiguous problems."),
    },
    instructions="Choose the least costly model that can complete the task safely.",
)
agent = create_agent(DEFAULT, middleware=[router])
for prompt in PROMPTS:
    result, seconds = timed(ask, agent, prompt)
    route = result["model_route"]
    print(f"{route.choice} (confidence {route.confidence:.2f}): routing + answer {seconds:.1f}s <- {prompt}")

print("\nTakeaway: the LLM router costs a whole generation; Jev's costs one classification, with a confidence.")
