from conftest import choice, make_classifier, noul
from langchain.agents import create_agent
from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
from langchain_core.messages import AIMessage
from langchain_typesafe.experimental.middleware import ModelChoice, ModelRouterMiddleware

from jev_demo.triage import OffTopicGuard


def fake(text: str) -> GenericFakeChatModel:
    return GenericFakeChatModel(messages=iter([AIMessage(text)]))


def ask(agent, text):
    return agent.invoke({"messages": [{"role": "user", "content": text}]})


def test_guard_stops_off_topic_before_the_model_runs():
    model = fake("SHOULD NOT APPEAR")
    guard = OffTopicGuard(make_classifier({"off_topic": noul(0.97)}), topic="payments")
    result = ask(create_agent(model, middleware=[guard]), "write a poem")
    assert result["messages"][-1].content == "I can only help with payments."


def test_guard_lets_on_topic_through():
    guard = OffTopicGuard(make_classifier({"off_topic": noul(0.02)}), topic="payments")
    result = ask(create_agent(fake("card updated"), middleware=[guard]), "update my card")
    assert result["messages"][-1].content == "card updated"


def test_router_uses_the_model_jev_picks(typesafe_env):
    router = ModelRouterMiddleware(
        choices={
            "fast": ModelChoice(model=fake("from fast"), criteria="simple"),
            "powerful": ModelChoice(model=fake("from powerful"), criteria="hard"),
        },
        instructions="cheapest that works",
    )
    router.classifier = make_classifier(
        {"model_route": choice("powerful", 0.9, labels=("fast", "powerful"))}
    )
    result = ask(create_agent(fake("default"), middleware=[router]), "hard question")
    assert result["messages"][-1].content == "from powerful"
    assert result["model_route"].choice == "powerful"


def _auto_mode(p_risky: float, typesafe_env):
    from langchain.tools import tool
    from langchain_typesafe.experimental.middleware import AutoModeMiddleware

    @tool
    def delete_file(path: str) -> str:
        """Delete a file."""
        return "deleted"

    mw = AutoModeMiddleware(tools=[delete_file])
    mw.classifier = make_classifier({"is_risky": noul(p_risky)})
    return mw, delete_file


def _tool_request(tool_obj):
    from langchain.tools.tool_node import ToolCallRequest
    from langchain_core.messages import HumanMessage

    call = {"id": "1", "name": tool_obj.name, "args": {"path": "/etc/passwd"}}
    return ToolCallRequest(
        tool_call=call, tool=tool_obj, state={"messages": [HumanMessage("rm it")]}, runtime=None
    )


def test_auto_mode_blocks_risky_call(typesafe_env):
    mw, tool_obj = _auto_mode(0.95, typesafe_env)
    out = mw.wrap_tool_call(_tool_request(tool_obj), lambda r: "EXECUTED")
    assert out != "EXECUTED" and out.status == "error"


def test_auto_mode_runs_safe_call(typesafe_env):
    mw, tool_obj = _auto_mode(0.05, typesafe_env)
    assert mw.wrap_tool_call(_tool_request(tool_obj), lambda r: "EXECUTED") == "EXECUTED"
