# 1. Jev

Source: [TypeSafe integrations](https://docs.langchain.com/oss/python/integrations/providers/typesafe)

```bash
pip install --pre "langchain-typesafe[experimental]"   # 0.0.1a3 is a pre-release
export TYPESAFE_API_KEY=...
```

Note: The package is alpha and `TypeSafeClassifier` is marked beta. Pin the version and expect API changes. Default model name is `jev-latest`; pin a concrete model id for reproducibility.

---

## Three question types

| Type | Asks | Returns |
|---|---|---|
| `Noul` | Yes or no? | `noul`: P(yes) in [0, 1] |
| `Choice` | Which one? | `choice`, `probabilities`, `confidence` |
| `Score` | How much? | expected `score` (may be fractional), `probabilities`, `confidence` |

One request can carry several questions about the same state.

--

## One call, three decisions

`examples/jev/01_classifier_basics.py`

```python
classifier = TypeSafeClassifier()
response = classifier.invoke({
    "state": "The deploy failed twice and customers are seeing 500s.",
    "questions": {
        "urgent":   Noul(instructions="Does this need attention right now?"),
        "team":     Choice(instructions="Which team should pick this up?",
                           criteria={"infra": "Deploys, availability, on-call.",
                                     "billing": "Payments and invoices.",
                                     "other": "Anything else."}),
        "severity": Score(instructions="How severe is the impact?",
                          criteria=["Cosmetic.", "Degraded for some.", "Full outage."]),
    },
})
response.nouls["urgent"].noul          # 0.93
response.choices["team"].confidence    # how concentrated the distribution is
response.scores["severity"].score      # e.g. 1.7
```

--

## Confidence is not the label's probability

> Confidence describes how concentrated the distribution is; it is not the selected label's probability. Thresholds should be chosen according to the consequences of an incorrect automated decision.
>
> (langchain-typesafe docs)

Include an `other` label so the model has somewhere to put what you did not anticipate.

---

## From probabilities to policy

`examples/jev_demo/gating.py`

```python
def decide(response, *, min_confidence=0.7, urgent_at=0.8, outage_at=1.5):
    team = response.choices["team"]
    if team.confidence < min_confidence or team.choice == "other":
        return Decision("human_triage", ...)           # low confidence: ask a human
    if response.nouls["urgent"].noul >= urgent_at \
       and response.scores["severity"].score >= outage_at:
        return Decision("page_oncall", ...)
    return Decision("auto_route", ...)
```

The thresholds are yours, tunable per cost of error. Tested offline in `tests/test_gating.py`.

--

## Testing without the API

`TypeSafeClassifier(client=...)` accepts an injected `httpx2` client.

```python
def handler(request):
    return httpx2.Response(200, json={"model": "jev-latest", "answers": {...}})

classifier = TypeSafeClassifier(
    api_key="test", client=httpx2.Client(transport=httpx2.MockTransport(handler)))
```

Real classifier, canned answers: 10 tests run with no keys and no network.
