# Walkthrough: the LLM way vs the decision-model way

Every demo script runs two acts on the same input and prints wall-clock latency:

- **Act 1** is how you would do it with a generative LLM (Gemini via Vertex).
- **Act 2** is how you do it with a decision model (Jev).

Press Enter between acts. `DEMO_NOPAUSE=1` skips the pauses (CI, dry runs).

## Setup

```bash
uv sync
gcloud auth application-default login      # Gemini via Vertex (ADC)
cp .env.example .env                        # TYPESAFE_API_KEY, GOOGLE_CLOUD_PROJECT
cd deck && python -m http.server 8000       # slides on one half of the screen
```

Run any step with `uv run --env-file .env python <path>` from the repo root, in a terminal on the other half.

## Order and what to say

| # | Run | Idea | Act 1 point | Act 2 point |
|---|-----|------|-------------|-------------|
| 1 | `examples/jev/01_classifier_basics.py` | Belief vs answer | Three valid answers, no probabilities. | Same three questions, each with a distribution. |
| 2 | `examples/jev/02_confidence_gating.py` | Belief becomes a decision | Every ticket is auto-routed. At temperature 1 the ambiguous one can flip teams, and nothing says when. | Same tickets: `decide()` escalates the low-confidence one and "dark mode". |
| 3 | `examples/jev/03_model_router.py` | Cost and speed | Routing costs a whole extra generation. | Routing is one classification, with a confidence. |
| 4 | `examples/jev/05_triage_middleware.py` | Guards | An LLM guard is a generation returning a bare boolean. | A probability, and the same guard as middleware stops the run early. |
| 5 | `examples/jev/06_eval_decisions.py` | At scale | Ten sequential generations. Accuracy looks fine. | Same accuracy, but confidence lets it act on the easy ones and escalate the rest. |

Each demo adds one idea. Demos 1 and 2 are about belief; latency is not the point until demo 3.

Unchanged, run when relevant: `jev/04_auto_mode.py`.

## Tips

- Latency numbers depend on region and load. Run once beforehand and read them aloud as "about", not as a benchmark.
- Whether the ambiguous ticket in demo 2 diverges is model-dependent. If it does not on the day, edit `TICKETS["ambiguous"]`.
- The talk track is "an answer vs a degree of belief"; the latency is the second point, not the first.
