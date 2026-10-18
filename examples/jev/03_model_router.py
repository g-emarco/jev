"""ModelRouterMiddleware: Jev picks the cheapest model that fits the task (experimental)."""

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_typesafe.experimental.middleware import ModelChoice, ModelRouterMiddleware

from jev_demo.models import DEFAULT, FAST, POWERFUL

load_dotenv()

router = ModelRouterMiddleware(
    choices={
        "fast": ModelChoice(
            model=FAST,
            criteria="Direct lookups and simple, well-scoped questions.",
        ),
        "powerful": ModelChoice(
            model=POWERFUL,
            criteria="Architecture, multi-step reasoning, and ambiguous problems.",
        ),
    },
    instructions="Choose the least costly model that can complete the task safely.",
)
agent = create_agent(DEFAULT, middleware=[router])

for prompt in ["What is the capital of France?", "Design a zero-downtime migration from a monolith to services."]:
    result = agent.invoke({"messages": [{"role": "user", "content": prompt}]})
    route = result["model_route"]  # full ChoiceAnswer is kept in state
    print(f"{route.choice:8} confidence={route.confidence:.2f} <- {prompt}")
