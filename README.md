# jev

Slide deck and runnable examples for **Jev**, TypeSafe's decision model, with LangChain
middleware and Google's decision offerings.

> **Disclaimer:** This is **not** an official or Google-endorsed repository.
> It is an independent implementation made for demonstration purposes only and
> does not reflect the views, products, or endorsement of Google in any way.

## Run the tests (offline, no keys)

    uv sync && uv run pytest

## View the deck

    cd deck && python -m http.server 8000   # then open http://localhost:8000

Markdown sections load over HTTP, so opening `index.html` as a file will not work.
Press `s` for speaker notes.

## Run the examples (live)

Copy `.env.example` to `.env`. Set `TYPESAFE_API_KEY`. Gemini runs on Vertex AI with Application Default
Credentials (`gcloud auth application-default login`); set `GOOGLE_CLOUD_PROJECT` (location defaults to `global`, required for Gemini 4 Argon).

    uv run --env-file .env python examples/jev/01_classifier_basics.py

| Script | Shows |
|---|---|
| `examples/jev/01_classifier_basics.py` | Noul, Choice, Score |
| `examples/jev/02_confidence_gating.py` | tickets, LLM vs Jev: act / escalate policy |
| `examples/jev/03_model_router.py` | `ModelRouterMiddleware` (experimental) |
| `examples/jev/04_auto_mode.py` | `AutoModeMiddleware` tool-risk gate (experimental) |
| `examples/jev/05_triage_middleware.py` | custom `before_agent` guard |
| `examples/jev/06_eval_decisions.py` | Jev vs Gemini on one labeled set |

## Status

- Offline tests cover gating, the custom guard, `ModelRouterMiddleware`, and `AutoModeMiddleware`.
- All six scripts were run live (Jev + Gemini 4 Argon on Vertex via ADC). `ModelRouterMiddleware`,
  `AutoModeMiddleware` and the custom guard were each seen doing their job.
- Gemini's safety filter often refuses risky tool calls itself, so `04_auto_mode.py` also feeds the
  gate synthetic tool calls to show Jev's risk classification directly.
- `langchain-typesafe` is a pre-release (`0.0.1a3`); its middleware is experimental.
- Model IDs live in `jev_demo/models.py`; several Gemini models retire soon.

## Research

`research/` holds the sourced notes behind the Google slides. Items marked UNVERIFIED there
were not confirmed against official docs.

---

> **Disclaimer:** This is **not** an official or Google-endorsed repository.
> It is an independent implementation made for demonstration purposes only and
> does not reflect the views, products, or endorsement of Google in any way.
