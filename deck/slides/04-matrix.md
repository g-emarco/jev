# 4. Choosing

---

## Jev vs an LLM with structured output

| | Jev | Gemini structured output |
|---|---|---|
| Output | probabilities + confidence | schema-valid JSON |
| Best at | classify, route, gate | generate, reason, extract, act |
| Gate on confidence | built in | you must build it (logprobs, self-report, ensembles) |
| Maturity | alpha package, experimental middleware | GA models |
| Open-ended text | no | yes |

`examples/jev/06_eval_decisions.py` runs both on one labeled set. **Measure before you choose.**

--

## Where the time goes

The router, guard and batch demos print wall-clock latency for the LLM act and the Jev act. Run `docs/WALKTHROUGH.md` live and read the numbers off the terminal.

| Step | LLM way | Decision-model way |
|---|---|---|
| Structured answer | one generation | one classification |
| Route to a model | extra generation first | one classification |
| Guard (off-topic, risky tool) | generation per check, bare boolean | classification per check, probability |
| Batch of N | N sequential generations | N classifications, with escalation |

<span class="small">Latency depends on region and load. Treat it as "about", not a benchmark.</span>

--

## Which tool for which decision

| If the decision is... | Use |
|---|---|
| a category, yes/no, or level, and you need thresholds | **Jev** (or Flash-Lite with a calibration step) |
| multi-step, needs tools and reasoning | **Gemini agent** (ADK or LangChain) |
| numeric prediction from history | **AutoML / BigQuery forecast** |
| combinatorial (routes, schedules) | **Route Optimization / a solver** |
| over a document corpus | **Agent Search / RAG Engine** |
| over thousands of warehouse rows | **BigQuery AI functions** |

--

## LangChain vs ADK vs managed

| | LangChain `create_agent` | ADK | Agent Runtime |
|---|---|---|---|
| Strength | middleware ecosystem, provider-neutral | Google-native deploy and trace | managed hosting and compliance |
| Choose when | existing LangChain/LangGraph code | greenfield on GCP | you want no infra |
| Combine | hosts on Agent Runtime | A2A to others | hosts either |

---

## Production checklist

- [ ] Thresholds chosen from **cost of error**, with a human path below them
- [ ] Offline tests with a mocked classifier (done here: 10 tests)
- [ ] A labeled eval set, rerun on every model change
- [ ] Alpha and experimental APIs **pinned**
- [ ] Model retirement dates tracked
- [ ] Fail-closed on classifier errors for risky actions
- [ ] Traces on, payload capture decided deliberately
- [ ] Budget for pricing changes (Gemini intro prices roughly double)
