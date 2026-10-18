# 2. Middleware

Where a decision belongs in an agent

Source: [LangChain middleware](https://docs.langchain.com/oss/python/langchain/middleware/built-in)

---

## The agent loop has hooks

| Hook | Runs | Typical use |
|---|---|---|
| `before_agent` | once per run | classify the request, refuse early |
| `before_model` / `after_model` | each model step | limits, output checks |
| `wrap_model_call` | around the model | swap model or prompt |
| `wrap_tool_call` | around each tool | gate, retry, log |

Return `{"jump_to": "end"}` (declared with `can_jump_to`) to stop the run.

--

## LangChain built-ins

```python
from langchain.agents.middleware import (
    PIIMiddleware, SummarizationMiddleware, ModelFallbackMiddleware,
    ModelCallLimitMiddleware, ToolRetryMiddleware, HumanInTheLoopMiddleware)
```

| Middleware | Purpose |
|---|---|
| `PIIMiddleware("email", strategy="redact")` | scrub inputs |
| `SummarizationMiddleware(trigger=("tokens", 4000))` | bound context |
| `ModelFallbackMiddleware(...)` | survive a provider failure |
| `ModelCallLimitMiddleware(run_limit=5)` | stop runaway loops |
| `HumanInTheLoopMiddleware(interrupt_on=...)` | human approves; needs a checkpointer |

---

## Jev as middleware: model routing

`examples/jev/03_model_router.py`, **experimental**

```python
router = ModelRouterMiddleware(
    choices={
        "fast":     ModelChoice(model=FAST,     criteria="Direct lookups, simple tasks."),
        "powerful": ModelChoice(model=POWERFUL, criteria="Architecture, multi-step reasoning."),
    },
    instructions="Choose the least costly model that can complete the task safely.",
)
agent = create_agent(FAST, middleware=[router])
```

- Classifies the latest human message **once** in `before_agent`
- Stores the full `ChoiceAnswer` in state (`result["model_route"]`)
- Classifier errors propagate; it never silently picks another model

--

## Jev as middleware: tool-risk gate

`examples/jev/04_auto_mode.py`, **experimental**

```python
agent = create_agent(FAST, tools=[read_file, delete_file],
                     middleware=[AutoModeMiddleware(tools=[delete_file])])
```

- A `Noul` question per guarded call: P(risky or not authorized)
- At or above **0.5**: returns an error `ToolMessage`, the tool never runs
- Only explicit **user** messages authorize; tool text is treated as data
- Fail-closed. It **blocks**, it does not ask for approval
- Live: allowed the authorized `/tmp` delete; blocked `/etc/shadow` (0.97) and `id_rsa` (0.99)

--

## Custom: classify first, spend later

`examples/jev_demo/triage.py`

```python
class OffTopicGuard(AgentMiddleware):
    @hook_config(can_jump_to=["end"])
    def before_agent(self, state, runtime):
        latest = next(m for m in reversed(state["messages"]) if isinstance(m, HumanMessage))
        r = self.classifier.invoke({"state": latest, "questions": {
            "off_topic": Noul(instructions=f"Is this unrelated to {self.topic}?")}})
        if r.nouls["off_topic"].noul >= self.threshold:
            return {"messages": [AIMessage(f"I can only help with {self.topic}.")],
                    "jump_to": "end"}
```

The main model is never called for refused requests (`tests/test_middleware.py`, and live: the otter-poem request was refused).

--

## Compose: order matters

`examples/jev/06_builtin_middleware_stack.py`

```python
middleware=[
    PIIMiddleware("email", strategy="redact", apply_to_input=True),  # scrub first
    SummarizationMiddleware(...),
    ModelFallbackMiddleware(CHEAP_FALLBACK),
    ModelCallLimitMiddleware(run_limit=5, exit_behavior="end"),
    ToolRetryMiddleware(max_retries=2),
    AutoModeMiddleware(tools=[send_refund]),         # Jev blocks the clearly unauthorized
    HumanInTheLoopMiddleware(interrupt_on={"send_refund": {...}}),  # a human approves the rest
]
```

Cheap automated gate first, human last. Only the calls that survive reach a person.

Note: The full stack ran live and paused at the human-approval step. That the Jev gate runs before HITL in this order was not isolated in a test; confirm if the order matters for you.
