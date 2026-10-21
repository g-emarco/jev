# Google LLM offerings, focus (a): Gemini models and Vertex AI APIs

Research date: 2026-10-18. Sources are official Google pages fetched that day. Pages are fetched through a summarizing tool, so exact figures should be re-checked on the source before commitments.
Note: Vertex AI docs now show "Agent Platform" / "Gemini Enterprise Agent Platform" branding in navigation (https://docs.cloud.google.com/vertex-ai/generative-ai/docs/quotas). How the rebrand maps onto the "Vertex AI" product name is UNVERIFIED.

Source keys:
- [MODELS] https://ai.google.dev/gemini-api/docs/models
- [PRICING] https://ai.google.dev/gemini-api/docs/pricing
- [FC] https://ai.google.dev/gemini-api/docs/function-calling
- [SO] https://ai.google.dev/gemini-api/docs/structured-output
- [THINK] https://ai.google.dev/gemini-api/docs/thinking
- [CACHE] https://ai.google.dev/gemini-api/docs/caching
- [GROUND] https://ai.google.dev/gemini-api/docs/google-search
- [VERSIONS] https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/model-versions
- [QUOTAS] https://docs.cloud.google.com/vertex-ai/generative-ai/docs/quotas
- [GARDEN] https://docs.cloud.google.com/vertex-ai/generative-ai/docs/model-garden/explore-models
- [EVAL-DOC] https://cloud.google.com/vertex-ai/generative-ai/docs/evaluation/introduction (redirected to a docs.cloud.google.com URL that returned 404; evaluation content NOT read)

## 1. Model lineup (Flash/Pro tiers)

What: Gemini family; Gemini 4 Argon flagship, Flash (balanced), Flash-Lite (cheapest/fastest), Pro (3.1 preview) [MODELS].

| Model | ID | Status | Price per 1M tokens, in/out (Standard) |
|---|---|---|---|
| Gemini 4 Argon | gemini-4-argon | Stable, flagship reasoning, 1M context | $2.00/$10.00, rising to $4/$20 from Dec 1 2026 |
| 3.8 Flash | gemini-3.8-flash | Stable, aimed at agents and long-horizon coding | $0.75/$3.75, rising to $1.50/$7.50 from Jan 1 2027 |
| 3.6 Flash | gemini-3.6-flash | Stable | $0.75/$3.75, rising likewise |
| 3.5 Flash-Lite | gemini-3.5-flash-lite | Stable, high throughput | $0.30/$2.50 |
| 3.1 Flash-Lite | gemini-3.1-flash-lite | Stable | $0.25/$1.50 |
| 3.1 Pro | gemini-3.1-pro-preview | Preview ID | $2/$12 (<=200k), $4/$18 (>200k) |
| 3 Flash | gemini-3-flash-preview | Preview | $0.50/$3.00 |
| 2.5 Pro/Flash/Flash-Lite | gemini-2.5-* | Access limited to prior users on the Gemini API [MODELS] | see [PRICING] |

Sources for table: [MODELS], [PRICING]. Output price includes thinking tokens [PRICING]. Priority tier is about 1.8x Standard; Flex equals Batch price; Batch is 50% off [PRICING].

Other models: Live/voice, TTS, transcribe, image (Nano Banana), video (Veo, Omni), music (Lyria), embeddings (gemini-embedding-2-preview, -001), robotics, deep-research agents [MODELS].

Lifecycle on Vertex [VERSIONS]:
- Long-term models are available at least 12 months after release.
- Short-term models get at least 45 days notice once a retirement date is set.
- gemini-4-argon released Oct 13 2026; 3.8-flash Sep 2 2026; 3.5-flash-lite Jul 21 2026; 3.5-flash May 19 2026.
- gemini-3.6-flash retires Nov 19 2026 (replacement 3.8-flash); 3.7-flash retires Jan 28 2027.
- gemini-2.5-pro, 2.5-flash and 2.5-flash-lite retire Oct 20 2026 on Vertex.
- 2.0 Flash and Flash-Lite already retired Jun 1 2026.
- Gemini API says preview models may be deprecated with at least 2 weeks notice [MODELS].

Production use cases: agents, extraction, classification, routing, RAG answerers, voice agents (UNVERIFIED as a use-case list; the model descriptions in [MODELS] only mention agents, software engineering and enterprise workflows).
When to use:
- Argon for the hardest reasoning.
- Flash for default agent and decision loops.
- Flash-Lite for high-volume classification and routing.
When NOT to use:
- Preview IDs (3.1 Pro, 3 Flash) for stable production, given the short deprecation notice [MODELS].
- Anything pinned to 2.5 or 3.6 without a migration plan, given the dates above.
Ops: introductory prices roughly double on the dates above [PRICING]; budget for it. Gemini API and Vertex model lists differ (3.5 Flash and 3.7 Flash appear in [VERSIONS] but not in [MODELS]); check the target platform.

## 2. Function calling

What: the model returns a function_call with a name and arguments; your code executes it and returns a function_result. Modes via tool_choice: auto (default), any (forced call), none, validated; allowed_tools restricts the callable set. Parallel and compositional (chained) calls are supported [FC].
Use: tool-using agents, taking actions, knowledge augmentation [FC].
Best practices and limits [FC]:
- Keep the active tool set to 10-20 tools.
- Only an OpenAPI schema subset is supported.
- In any mode, very large or deeply nested schemas may be rejected.
- Validate calls before executing them.
- Streaming gives partial arguments that must be aggregated before execution.
- MCP: only Streamable HTTP servers; SSE is not supported.
- Forcing structured text right before a tool call can cause Malformed_Function_Call; the page suggests an update() function or Markdown headers as workarounds.
- Gemini 3 models can combine built-in tools (Search etc.) with function calling and support multimodal function responses.
- Stateless mode requires resending all model steps unmodified, including thought steps.
NOT for: executing anything unvalidated; very large tool catalogs (more than 20) without tool retrieval or narrowing.

## 3. Structured output (JSON schema)

What: response_format of application/json with a schema; Pydantic and Zod supported [SO].
Supported: string, number, integer, boolean, object, array, null via type arrays; enum, format, min/max, minItems/maxItems, prefixItems, additionalProperties, anyOf, recursive $ref [SO].
Combining with tools (Search, URL Context, Code Execution, File Search, function calling) is Preview and Gemini 3 only [SO].
Caveats [SO]:
- Only a subset of JSON Schema is supported.
- Large or deeply nested schemas may be rejected.
- Syntactically valid JSON can still be semantically wrong, so validate in your app.
Use: decision outputs (enum classification, routing, extraction). Use enums plus a short reasoning field (this last tip is UNVERIFIED as official guidance).
NOT for: relying on schema validity as correctness.

## 4. Grounding with Google Search

What: the google_search tool; the model decides whether to search, generates queries, and returns a grounded answer with url_citation annotations and search_suggestions HTML [GROUND].
Models: Argon, 3.8/3.6 Flash, 3.5 Flash-Lite, 3.1 Pro, 3 Flash, 2.5 family [GROUND]. Can combine with URL context, code execution and Maps [GROUND].
Pricing: Gemini 3+ is billed per executed search query; 5,000 free per month shared, then $14 per 1,000. Gemini 2.5 is billed per grounded prompt (1,500 per day free, then $35 per 1,000) [GROUND][PRICING].
Use: fresh-fact decisions, verifiable citations.
NOT for: closed-corpus or private-data decisions (use RAG/File Search); latency- or cost-sensitive bulk calls (every query is billed, with multiple queries possible per call) [GROUND]. Display requirements for search suggestions are in the ToS and were not detailed in the doc [GROUND]; check them before building a UI.

## 5. Thinking/reasoning controls

What: thinking_level (minimal, low, medium, high) in the current docs; dynamic reasoning by default [THINK]. thinkingBudget is not mentioned on the current page (older-API detail UNVERIFIED).
Defaults [THINK]:
- Argon and 3.8 Flash: medium (low/medium/high only).
- 3.6 Flash: medium (minimal through high).
- 3.5 Flash-Lite: minimal.
- 3.1 Pro: high.
Other behavior [THINK]:
- Thought summaries are opt-in (thinking_summaries).
- Thought signatures are required for continuity: stateful mode (store plus previous_interaction_id) handles them; stateless mode needs all thought blocks resent unmodified.
- Billing covers the full thought tokens, not just the summary.
- max_output_tokens includes thinking, so a low cap truncates but still bills.
- Argon is capped at 65,536 output tokens synchronously; longer output needs background=True.
Use: raise level for multi-step decisions; lower it to cut cost and latency.
NOT for: tight-latency routing at high level; use minimal/Flash-Lite.

## 6. Context caching

What: implicit caching is on by default for 2.5 and newer, with savings passed on automatically; explicit cache objects are unavailable for Argon and in the Interactions API but remain on 3 and 2.5 via generateContent [CACHE].
Minimum tokens: 4,096 for Argon, 3.8 Flash, 3.6 Flash and 3.1 Pro; 2,048 for 2.5 [CACHE].
Prices [PRICING]:
- Cached input is about 10% of the input price (Argon $0.10, 3.8 Flash $0.075).
- Explicit-cache storage costs $0.50-$4.50 per hour per 1M tokens depending on model (storage unit inferred from the table, so confirm on the page).
Tip: put the shared prefix first; check usage.total_cached_tokens [CACHE].
Use: big static system prompt, policy docs or tool schemas reused across decisions.
NOT for: prompts under the minimum, or highly variable prefixes. TTL details were not given in the doc fetched (UNVERIFIED).

## 7. Vertex AI operations: quotas, Model Garden, evaluation

Quotas [QUOTAS]:
- Quotas are per project.
- Tuned models use the base model quota.
- Batch inference on Gemini has no predefined quota; jobs may queue.
- Embeddings: gemini-embedding-2 allows 200M tokens per minute and 60k requests per minute.
- Gen AI evaluation: 1,000 requests per minute, 20 concurrent runs, 60-second request timeout, up to 2 minutes setup delay on first use.
- Navigation lists Provisioned Throughput and Standard/Priority/Flex PayGo, and a 429 troubleshooting page, but details were NOT read (UNVERIFIED).

Model Garden [GARDEN]:
- A catalog for finding, customizing and deploying Google, partner and open models.
- Partner models: Claude, Grok, Mistral, Meta. Open models: Gemma, Llama, Qwen, DeepSeek and others (per navigation).
- Deployment options: managed open-model APIs (MaaS) or self-deploy on GPU/TPU with vLLM/Hex-LLM; Hugging Face models are scanned, but suspicious ones can still be deployed, so review them.
- Org policy can allow-list models. (Note: this very research session's own web_search tool was blocked by such a policy, which shows the control is real. Source: tool error.)
- Open-model costs are tuning and endpoint compute.
Use: need non-Gemini or self-hosted models, or a data-residency or custom-weights requirement.
NOT for: simple Gemini use (call the API directly).

Evaluation service: a Gen AI evaluation service exists, with limits above [QUOTAS] and a mention in [GARDEN]. Metric types, agent evaluation and pricing were NOT retrieved; the doc URL redirect returned 404. UNVERIFIED. Judge-model usage counts against that model's consumption [QUOTAS].

## Gaps
- Provisioned Throughput and PayGo tier details; evaluation metrics and pricing; context cache TTL; Google Search display rules; Vertex-specific pricing (only Gemini API pricing was retrieved, and Vertex prices may differ, UNVERIFIED).
- The web search tool was unavailable (org policy block), so only direct page fetches were used.
