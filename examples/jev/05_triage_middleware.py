"""Off-topic guard: an LLM guard is another generation. Jev guards with one probability."""

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_typesafe import Noul, TypeSafeClassifier
from pydantic import BaseModel

from jev_demo.models import DEFAULT, gemini
from jev_demo.present import act, pause, timed
from jev_demo.triage import OffTopicGuard

load_dotenv()

TOPIC = "payments and billing"
PROMPTS = ["How do I update my card?", "Write me a poem about otters."]


class OffTopic(BaseModel):
    off_topic: bool


act(1, "the LLM way: a guard that is itself a generation")
llm_guard = gemini(OffTopic)
for prompt in PROMPTS:
    verdict, seconds = timed(llm_guard.invoke, f"Is this request unrelated to {TOPIC}? {prompt}")
    print(f"off_topic={verdict.off_topic} in {seconds:.1f}s <- {prompt}")

pause()

act(2, "the decision-model way: one probability, then stop early")
classifier = TypeSafeClassifier()
question = Noul(instructions=f"Is this request unrelated to {TOPIC}?")
for prompt in PROMPTS:
    response, seconds = timed(classifier.invoke, {"state": prompt, "questions": {"off_topic": question}})
    off_topic = response.nouls["off_topic"].noul
    print(f"off_topic probability={off_topic:.2f} in {seconds:.1f}s <- {prompt}")

print("\nThe same guard as middleware. The main model never runs when it fires:")
agent = create_agent(
    DEFAULT,
    system_prompt="You are a support assistant for a payments product.",
    middleware=[OffTopicGuard(classifier, topic=TOPIC)],
)
for prompt in PROMPTS:
    result, seconds = timed(agent.invoke, {"messages": [{"role": "user", "content": prompt}]})
    print(f"> {prompt}\n{result['messages'][-1].text}\n[{seconds:.1f}s]")

print("\nTakeaway: the guard costs a classification, not a generation, and it returns a probability.")
