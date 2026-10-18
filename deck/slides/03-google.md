# 3. Google's decision offerings

Production use cases, and when to reach for each

<span class="small">Researched 2026-10-18 from official docs. Names and prices are moving: verify before quoting. Details: `research/google-*.md`</span>

---

## Three layers

| Layer | Products | Decides by |
|---|---|---|
| **Models** | Gemini, Model Garden | LLM reasoning |
| **Agent platform** | ADK, Agent Runtime, A2A, Agent Registry | LLM + orchestration |
| **Decision engines** | BigQuery AI, Route Optimization, AutoML, Search | statistics, solvers, ranking |

Rule of thumb: **use an LLM to decide what to do, an engine to compute the answer.**

---

## Gemini: the model tier

| Model | Role | Note |
|---|---|---|
| Gemini 4 Argon | hardest reasoning | stable, $2 / $10 per 1M tokens, 1M context |
| 3.8 Flash | default agent and decision loops | stable, $0.75 / $3.75 |
| 3.5 / 3.1 Flash-Lite | high-volume classification, routing | $0.25 to $0.30 input |

<span class="small">Introductory prices roughly double on 2026-12-01 (Argon) and 2027-01-01 (3.8 Flash). Gemini API pricing page; Vertex prices not confirmed.</span>

--

## Gemini: decision features

| Feature | Use for | Watch out |
|---|---|---|
| Function calling | taking actions | keep to ~10-20 tools; validate calls before executing |
| Structured output | enum decisions, extraction | valid JSON is not correct JSON; no confidence score |
| Search grounding | fresh public facts | billed per search query; not for private data |
| `thinking_level` | multi-step decisions | thinking tokens are billed; lower it for routing |
| Context caching | large reused policy prompts | 4,096-token minimum on current models |

`examples/google/01_*`, `03_*`

--

## Lifecycle is a production risk

- Gemini 2.5 family retires on Vertex **2026-10-20**
- 3.6 Flash retires **2026-11-19**, 3.7 Flash **2027-01-28**
- Preview model IDs can be deprecated on short notice
- Gemini API and Vertex model lists differ

Keep model ids in **one module** (`examples/jev_demo/models.py`) and put the dates in a calendar.

---

## ADK and Agent Runtime

**ADK** (open source: Python, TypeScript, Go, Java, Kotlin)

- Use: on or moving to Google Cloud; multi-agent routing; first-party deploy, trace, registry
- Skip: you already run LangGraph. Agent Runtime hosts LangChain and LangGraph too

**Agent Runtime** (Agent Engine renamed, inferred)

- Use: minimal infra, enterprise controls (VPC-SC, CMEK, HIPAA, Sessions, Memory Bank)
- Skip: you need container-level control or open-model hosting (use GKE), or non-GCP hosting

`examples/google/02_adk_router_agent.py`: router + specialists + `before_tool_callback` guardrail

--

## ADK in production: caveats from the docs

- **Human-in-the-loop confirmation is Experimental**, and unsupported with `DatabaseSessionService` and `VertexAiSessionService`
- Cloud Trace: payload capture is **off by default** on Agent Runtime (placeholders instead of prompts)
- Guardrails are layered: callbacks, plugins (Model Armor, PII redaction, Gemini-as-judge), in-tool checks
- Pricing and quotas: **not verified**

--

## A2A and Agent Registry

- **A2A**: open standard (Linux Foundation) for agent-to-agent calls across vendors. Complements MCP (agent-to-tool)
  - Use when separate teams or frameworks must interoperate; unneeded inside one process
- **Agent Registry**: catalog + governance for agents, MCP servers, skills, with Agent Identity and Agent Gateway
  - Use at many-teams scale; overkill for two agents. Release status not stated in docs

---

## Decision engines: not everything is an agent

| Product | Use it for | Not for |
|---|---|---|
| **BigQuery AI** (`AI.IF`, `AI.CLASSIFY`, `AI.SCORE`, GA 2026-04-13) | batch enrichment in the warehouse | per-row low latency; note failed rows return `NULL` unless `max_error_ratio` is lowered |
| **Route Optimization API** | fleet routing, dispatch, field service | non-routing optimization. $30 / 1k fleet events, $10 single-vehicle |
| **AutoML tabular / forecasting** | churn, demand, price from your history | tiny datasets; use `AI.FORECAST` for simple series |
| **Agent Search** (was Vertex AI Search) | grounded answers over a corpus | aggregation, actions |
| **RAG Engine** | developer-controlled retrieval | exact numeric queries. GA in only four regions |
| **Document AI** | invoices, forms, IDs | one-off varied docs: plain Gemini may be simpler |
| **Conversational Analytics** | NL-to-SQL BI on BigQuery/Looker | numbers that must be right without review |

--

## The production pattern

```text
request -> cheap classifier (Jev / Flash-Lite) -> confident?  -- no --> human
                                |
                               yes
                                v
              LLM agent (plans, calls tools) -> solver / forecast / search as TOOLS
                                v
                  guardrail middleware -> action
```

The agent orchestrates and explains. Deterministic engines compute.
