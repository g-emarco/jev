"""ADK: a router agent delegating to specialists, with a before_tool_callback guardrail."""

import asyncio

from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner

load_dotenv()

from jev_demo.models import ARGON_ID

MODEL = ARGON_ID


def lookup_invoice(invoice_id: str) -> dict:
    """Look up an invoice by id."""
    return {"invoice_id": invoice_id, "status": "paid", "amount": 900.0}


def issue_refund(invoice_id: str, amount: float) -> dict:
    """Refund an invoice."""
    return {"invoice_id": invoice_id, "refunded": amount}


def refund_guardrail(tool, args, tool_context):
    """Block refunds above a limit. Returning a dict skips the tool and uses it as the result."""
    if tool.name == "issue_refund" and args.get("amount", 0) > 100:
        return {"error": "Refunds over 100 need human approval."}
    return None


billing = Agent(
    name="billing",
    model=MODEL,
    description="Handles invoices, charges, and refunds.",
    instruction="Resolve billing questions using the tools. Be brief.",
    tools=[lookup_invoice, issue_refund],
    before_tool_callback=refund_guardrail,
)
infra = Agent(
    name="infra",
    model=MODEL,
    description="Handles outages, deploys, and availability incidents.",
    instruction="Triage the incident and state the first three diagnostic steps.",
)
root_agent = Agent(
    name="router",
    model=MODEL,
    instruction="Delegate each request to the best specialist. Do not answer yourself.",
    sub_agents=[billing, infra],
)


async def main() -> None:
    runner = InMemoryRunner(agent=root_agent)
    await runner.run_debug("Refund 500 on invoice INV-9, the customer was double charged.")


if __name__ == "__main__":
    asyncio.run(main())
