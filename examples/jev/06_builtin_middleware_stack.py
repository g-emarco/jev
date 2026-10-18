"""Jev middleware composed with LangChain's built-ins: order matters, top runs first."""

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.agents.middleware import (
    HumanInTheLoopMiddleware,
    ModelCallLimitMiddleware,
    ModelFallbackMiddleware,
    PIIMiddleware,
    SummarizationMiddleware,
    ToolRetryMiddleware,
)
from langchain.tools import tool
from langchain_typesafe.experimental.middleware import AutoModeMiddleware
from langgraph.checkpoint.memory import InMemorySaver

from jev_demo.models import CHEAP_FALLBACK, DEFAULT

load_dotenv()


@tool
def send_refund(order_id: str, amount: float) -> str:
    """Refund an order."""
    return f"refunded {amount} on {order_id}"


agent = create_agent(
    DEFAULT,
    tools=[send_refund],
    middleware=[
        PIIMiddleware("email", strategy="redact", apply_to_input=True),
        SummarizationMiddleware(
            model=DEFAULT, trigger=("tokens", 4000), keep=("messages", 20)
        ),
        ModelFallbackMiddleware(CHEAP_FALLBACK),
        ModelCallLimitMiddleware(run_limit=5, exit_behavior="end"),
        ToolRetryMiddleware(max_retries=2),
        AutoModeMiddleware(tools=[send_refund]),  # Jev blocks clearly unauthorized calls...
        HumanInTheLoopMiddleware(  # ...and a human approves the rest
            interrupt_on={"send_refund": {"allowed_decisions": ["approve", "reject"]}}
        ),
    ],
    checkpointer=InMemorySaver(),  # required for human-in-the-loop interrupts
)

config = {"configurable": {"thread_id": "demo"}}
result = agent.invoke(
    {"messages": [{"role": "user", "content": "Refund 20 on order A-17, I'm bob@example.com."}]},
    config,
)
print("interrupted:", "__interrupt__" in result)
