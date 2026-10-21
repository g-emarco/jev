"""Custom middleware: classify the request once, before the agent runs, and stop early."""

from typing import Any

from langchain.agents.middleware import AgentMiddleware, AgentState, hook_config
from langchain.messages import AIMessage, HumanMessage
from langchain_typesafe import Noul, TypeSafeClassifier
from langgraph.runtime import Runtime


class OffTopicGuard(AgentMiddleware):
    """Refuse off-topic requests before spending a single main-model token."""

    def __init__(self, classifier: TypeSafeClassifier, topic: str, threshold: float = 0.8):
        super().__init__()
        self.classifier = classifier
        self.topic = topic
        self.threshold = threshold

    @hook_config(can_jump_to=["end"])
    def before_agent(self, state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
        latest = next(m for m in reversed(state["messages"]) if isinstance(m, HumanMessage))
        question = Noul(instructions=f"Is this request unrelated to {self.topic}?")
        response = self.classifier.invoke({"state": latest, "questions": {"off_topic": question}})
        if response.nouls["off_topic"].noul >= self.threshold:
            return {
                "messages": [AIMessage(f"I can only help with {self.topic}.")],
                "jump_to": "end",
            }
        return None
