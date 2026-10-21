# LangChain v1 Python API notes (fetched 2026-10-18)

## 1. Typesafe page
URL: https://docs.langchain.com/oss/python/integrations/providers/typesafe
Title: "TypeSafe integrations". NOT about type-safe structured output. It is a provider page for TypeSafe's "Jev" model, which returns typed answers and calibrated probabilities (classification) rather than generated text.
- Install: `pip install langchain-typesafe` (or `uv add`); experimental: `pip install "langchain-typesafe[experimental]" langchain-openai`
- Env: `TYPESAFE_API_KEY` (required), `TYPESAFE_BASE_URL` (optional, default https://api.typesafe.ai)
- Imports: `from langchain_typesafe import Choice, Noul, Score, TypeSafeClassifier` (also ChoiceAnswer, NoulCriteria); `from langchain_typesafe.experimental.middleware import ModelChoice, ModelRouterMiddleware, AutoModeMiddleware`
- Decision types: Noul (yes/no probability), Choice (pick one), Score (level on spectrum). Classifier is a Runnable; state and questions both go in invoke().
- Experimental middleware: ModelRouterMiddleware (routes model; result["model_route"].choice), AutoModeMiddleware (tool-risk gating; refuses risky calls, no approval prompt). Custom TriageMiddleware example subclasses AgentMiddleware and classifies in before_agent.
```python
from langchain_typesafe import Choice, Noul, Score, TypeSafeClassifier
classifier = TypeSafeClassifier()
response = classifier.invoke({
    "state": "The deploy failed twice and customers are seeing 500s. Can someone look now?",
    "questions": {
        "urgent": Noul(instructions="Does this need attention right now?"),
        "team": Choice(instructions="Which team should pick this up?",
                       criteria={"infra": "Deploys, availability, and on-call incidents.",
                                 "billing": "Payments, invoices, and subscriptions."}),
        "severity": Score(instructions="How severe is the impact?",
                          criteria=["Cosmetic.", "Degraded for some users.", "Full outage."]),
    },
})
print(response.nouls["urgent"].noul)
print(response.choices["team"].choice, response.choices["team"].confidence)
print(response.scores["severity"].score)
```
```python
router = ModelRouterMiddleware(
    choices={"fast": ModelChoice(model="openai:gpt-5.6-terra", criteria="Direct lookups..."),
             "powerful": ModelChoice(model="openai:gpt-6-astra", criteria="Architecture...")},
    instructions="Choose the least costly model that can complete the task safely.")
agent = create_agent("openai:gpt-5.6-terra", middleware=[router])
```
Tool gating: `create_agent("openai:gpt-6-astra", tools=[t], middleware=[AutoModeMiddleware(tools=[t])])`

## 2. create_agent
URLs: https://docs.langchain.com/oss/python/langchain/agents ; https://reference.langchain.com/python/langchain/agents/factory/create_agent
```python
create_agent(
    model: str | BaseChatModel,
    tools: Sequence[BaseTool | Callable | dict] | None = None,
    *,
    system_prompt: str | SystemMessage | None = None,
    middleware: Sequence[AgentMiddleware] = (),
    response_format: ResponseFormat[ResponseT] | type[ResponseT] | dict | None = None,
    state_schema: type[AgentState] | None = None,
    context_schema: type | None = None,
    checkpointer: Checkpointer | None = None,
    store: BaseStore | None = None,
    interrupt_before: list[str] | None = None,
    interrupt_after: list[str] | None = None,
    debug: bool = False,
    name: str | None = None,
    cache: BaseCache | None = None,
    transformers: Sequence[TransformerFactory] | None = None,
) -> CompiledStateGraph
```
Model strings on page: "anthropic:claude-sonnet-5", "openai:gpt-5.5", "google_genai:gemini-3.6-flash", etc.
```python
agent = create_agent(model="anthropic:claude-sonnet-5", tools=tools)
result = agent.invoke({"messages": [{"role": "user", "content": "..."}]})
```

## 3. Built-in middleware
URL: https://docs.langchain.com/oss/python/langchain/middleware/built-in  (all from `langchain.agents.middleware`)
- ToolErrorMiddleware(on_error, aon_error=None, tools=None)  [langchain>=1.3.14]
- ToolRetryMiddleware(max_retries=2, tools=None, retry_on=default_retry_on, on_failure="continue", backoff_factor=2.0, initial_delay=1.0, max_delay=60.0, jitter=True)
- ModelRetryMiddleware(same, no tools)
- ModelFallbackMiddleware(first_model, *additional_models)  e.g. ("gpt-5.4-mini", "claude-sonnet-4-6")
- SummarizationMiddleware(model, trigger=None, keep=("messages", 20), token_counter=None, summary_prompt=None, trim_tokens_to_summarize=4000)  (deprecated: summary_prefix, max_tokens_before_summary, messages_to_keep)
- HumanInTheLoopMiddleware(interrupt_on, interrupt_mode=...)  needs checkpointer
- ModelCallLimitMiddleware(thread_limit=None, run_limit=None, exit_behavior="end")
- ToolCallLimitMiddleware(tool_name=None, thread_limit=None, run_limit=None, exit_behavior="continue")
- PIIMiddleware(pii_type, strategy="redact", detector=None, apply_to_input=True, apply_to_output=False, apply_to_tool_results=False)
- TodoListMiddleware(system_prompt=None, tool_description=None)
- LLMToolSelectorMiddleware(model=None, system_prompt=None, max_tools=None, always_include=None)
- ProviderToolSearchMiddleware(searchable_tools=None)
- ShellToolMiddleware(workspace_root=None, startup_commands=None, shutdown_commands=None, execution_policy=None, redaction_rules=None, tool_description=None, shell_command=None, env=None)
- FilesystemFileSearchMiddleware(root_path, use_ripgrep=True, max_file_size_mb=10)
- ContextEditingMiddleware(edits=[ClearToolUsesEdit()], token_count_method="approximate"); ClearToolUsesEdit(trigger=100000, clear_at_least=0, keep=3, clear_tool_inputs=False, exclude_tools=(), placeholder="[cleared]")
- LLMToolEmulator(tools=None, model=None)
- deepagents: FilesystemMiddleware, SubAgentMiddleware, RubricMiddleware (not langchain core)
```python
SummarizationMiddleware(model="gpt-5.4-mini", trigger=("tokens", 4000), keep=("messages", 20))
HumanInTheLoopMiddleware(interrupt_on={"your_send_email_tool": {"allowed_decisions": ["approve","edit","reject"]}, "your_read_email_tool": False})
ModelFallbackMiddleware("gpt-5.4-mini", "claude-sonnet-4-6")
ModelCallLimitMiddleware(thread_limit=10, run_limit=5, exit_behavior="end")
ToolRetryMiddleware(max_retries=3, backoff_factor=2.0, initial_delay=1.0)
PIIMiddleware("email", strategy="redact", apply_to_input=True)
PIIMiddleware("credit_card", strategy="mask", apply_to_input=True)
ToolCallLimitMiddleware(tool_name="search", thread_limit=5, run_limit=3)
```

## 4. Custom middleware
URL: https://docs.langchain.com/oss/python/langchain/middleware/custom
Decorators: before_model, after_model, wrap_model_call, wrap_tool_call, hook_config (also dynamic_prompt listed on page but NO sample in docs fetched; the dynamic prompt example uses wrap_model_call). jump_to targets: 'end', 'tools', 'model'; declare via can_jump_to.
```python
from langchain.agents.middleware import before_model, after_model, wrap_model_call, wrap_tool_call, hook_config, AgentState, AgentMiddleware, ModelRequest, ModelResponse
from langgraph.runtime import Runtime

@before_model(can_jump_to=["end"])
def check_message_limit(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    if len(state["messages"]) >= 50:
        return {"messages": [AIMessage("Conversation limit reached.")], "jump_to": "end"}
    return None

@wrap_model_call
def add_context(request: ModelRequest, handler: Callable[[ModelRequest], ModelResponse]) -> ModelResponse:
    new_content = list(request.system_message.content_blocks) + [{"type": "text", "text": "Additional context."}]
    return handler(request.override(system_message=SystemMessage(content=new_content)))

@wrap_tool_call
def monitor_tool(request: ToolCallRequest, handler: Callable[[ToolCallRequest], ToolMessage | Command]) -> ToolMessage | Command:
    print(request.tool_call['name'], request.tool_call['args'])
    return handler(request)
# imports: from langchain.tools.tool_node import ToolCallRequest ; from langgraph.types import Command ; from langchain.messages import AIMessage, SystemMessage, ToolMessage
```
State schema (decorator): `@before_model(state_schema=CustomState, can_jump_to=["end"])`, where `class CustomState(AgentState): model_call_count: NotRequired[int]`.
Class-based:
```python
class MessageLimitMiddleware(AgentMiddleware):
    def __init__(self, max_messages: int = 50):
        super().__init__(); self.max_messages = max_messages
    @hook_config(can_jump_to=["end"])
    def before_model(self, state: AgentState, runtime: Runtime) -> dict[str, Any] | None: ...
    def after_model(self, state, runtime): ...
    def wrap_model_call(self, request, handler): return handler(request)
    def wrap_tool_call(self, request, handler): return handler(request)
    # async variants: abefore_model, aafter_model
class CallCounter(AgentMiddleware[CustomState]):
    state_schema = CustomState
```
Also before_agent exists (used by Typesafe page).

## 5. Structured output
URL: https://docs.langchain.com/oss/python/langchain/structured-output
- response_format accepts ToolStrategy[T] | ProviderStrategy[T] | type[T] | None. Bare schema auto-selects ProviderStrategy (if model supports native), else tool strategy. AutoStrategy not mentioned in docs.
- ToolStrategy(schema, tool_message_content=None, handle_errors=...); handle_errors: str | ExceptionType | tuple | callable | False
- ProviderStrategy(schema, strict: bool | None = None)
- Errors: `from langchain.agents.structured_output import StructuredOutputValidationError, MultipleStructuredOutputsError`
```python
agent = create_agent(model="anthropic:claude-sonnet-5", tools=tools, response_format=ToolStrategy(ProductReview))
agent = create_agent(..., response_format=ProviderStrategy(ContactInfo))
result["structured_response"]
```

## 6. langchain-google-genai
URL: https://docs.langchain.com/oss/python/integrations/chat/google_generative_ai
- `pip install -U langchain-google-genai`
- Env: GOOGLE_API_KEY (fallback GEMINI_API_KEY). Vertex/enterprise: GOOGLE_GENAI_USE_VERTEXAI, GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_LOCATION.
- Models on page: gemini-3.7-flash, gemini-3.1-pro-preview, gemini-2.5-flash, gemini-2.5-flash-image, ...
```python
from langchain_google_genai import ChatGoogleGenerativeAI
model = ChatGoogleGenerativeAI(model="gemini-3.7-flash", temperature=1.0, max_tokens=None, timeout=None, max_retries=2)
# Vertex: add project="your-project-id", location="us-central1"
from langchain.chat_models import init_chat_model
model = init_chat_model("google_genai:gemini-3.7-flash")
agent = create_agent("google_genai:gemini-3.6-flash", tools=[...])
```
Caveat: model-name versions are as printed in the docs; verify availability against the live API.
