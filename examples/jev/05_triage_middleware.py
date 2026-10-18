"""Custom middleware: a Jev guard in before_agent that ends the run early."""

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_typesafe import TypeSafeClassifier

from jev_demo.triage import OffTopicGuard

from jev_demo.models import DEFAULT

load_dotenv()

agent = create_agent(
    DEFAULT,
    system_prompt="You are a support assistant for a payments product.",
    middleware=[OffTopicGuard(TypeSafeClassifier(), topic="payments and billing")],
)

for prompt in ["How do I update my card?", "Write me a poem about otters."]:
    result = agent.invoke({"messages": [{"role": "user", "content": prompt}]})
    print(f"> {prompt}\n{result['messages'][-1].text[:200]}\n")
