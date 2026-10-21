# 5. In production

Who runs decision models, and what moved.

Research date 2026-10-20. Vendor-published numbers, not independently verified. Notes in `research/production-cases-{a,b,c}.md`.

---

## Jev: one named customer

| | |
|---|---|
| Customer | **Jack & Jill** (AI talent marketplace) |
| Decision | first-stage candidate scoring |
| Replaced | Gemini 3.1 Flash Lite, 100% of calls in that stage |
| Time to prod | 10 days after first test |
| Reach | "15+ workflows" (vendor post only) |

Source: [TypeSafe case study](https://typesafe.ai/blog/jack-jill-jev-case-study), Oct 7 2026

<span class="small">No other customer is named on the LangChain page, PyPI, docs, evals site, launch post or adapter repo. No third-party benchmarks found. typesafe.com is Akka, not TypeSafe.</span>

Note: Be upfront with the audience: this is a young product with one public reference.

--

## Jack & Jill: Gemini → Jev

Offline test, 150 live roles, same candidates.

| Metric | Gemini | Jev |
|---|---|---|
| Cost per 1,000 candidates | $0.755 | **$0.092** (-88%) |
| Median screening time | 20.3 s | **10.3 s** |
| Winners kept in shortlist | 93.9% | 94.6% |
| AUC | 0.924 | 0.933 |

**Cost and latency moved; quality held.** The shortlist difference is not statistically significant.

<span class="small">Claimed savings: $265K/yr at current volume. The CEO quote ("about half a million last week") conflicts with the article's own numbers, so quote neither without checking.</span>

--

## Jev: vendor claims to discount

| Claim | Caveat |
|---|---|
| "193.6x faster, 444.6x cheaper" | the launch post calls it the high end of real-world gains |
| 0% type errors | true by construction, not measured |
| 67.8% avg accuracy, $0.0004 and 0.4 s per case | labels are the average of two frontier models, so this is agreement, not ground truth |
| Top models score 73-74% on the same evals | Jev is weakest on invoices: 61.8% vs 79.1% |

Source: [evals.typesafe.ai](https://evals.typesafe.ai/), [launch post](https://typesafe.ai/blog/introducing-system-one-models-and-jev)

**Read it as: cheaper and faster, a few points less accurate on hard tasks.**

<span class="small">Name: Jev is not an acronym. It refers to Jevons (the Jevons paradox), per the launch post.</span>

---

## Routing: pick the model per request

| Who | Result | Source type |
|---|---|---|
| **RouteLLM** (LMSYS/Berkeley) | >85% cost cut on MT Bench, 45% on MMLU, 35% on GSM8K at 95% of GPT-4 quality | research, open source |
| **Not Diamond**, own chatbot | -51% inference cost, about $750K/yr; engagement flat | vendor, real traffic |
| **Not Diamond Code** | 20-80% cheaper than Opus xhigh at matched quality | vendor benchmark |
| **AWS Bedrock prompt routing** | "up to 30%" cost cut | vendor claim, no method |

<span class="small">Paper Table 6 is more modest than the blog: 3.66x on MT Bench, 1.41x MMLU, 1.49x GSM8K. Azure model router: no numbers published, only quality bands.</span>

--

## Guardrails: gate every call

| Who | Decision | Result |
|---|---|---|
| **Constitutional Classifiers v1** | block jailbreaks | success 86% → 4.4%, over-refusal +0.38%, +23.7% compute |
| **Classifiers++** | same, as a cascade | ~1% overhead, 0.05% refusals on production traffic |
| **Claude Code auto mode** | allow/block each tool call | 0.4% false positives (n=10,000), **17% false negatives** on real overeager actions (n=52) |
| **NVIDIA NemoGuard recipe** | safety gate | content safety 88% → 94%, security 56% → 63% |
| **Llama Guard** | prompt/response safety | AUPRC 0.945 vs 0.764 (OpenAI Mod API), on its own test set |

Source: [Anthropic](https://www.anthropic.com/research/constitutional-classifiers), research notes B.

**Closest analogue to Jev's `AutoModeMiddleware`: measure the miss rate, not just false alarms.**

---

## Triage, fraud, ETA: classic decision models

| Who | Decision | Result |
|---|---|---|
| **Uber COTA v1** | ticket type + top-3 fixes | handle time about -10% (A/B), CSAT up a few points |
| **Uber COTA v2** | same, deep learning | accuracy 49% → 65%, handle time -6.6% vs v1, p95 under 10 ms |
| **Uber DeepETA** | ETA | MAE -2.91% delivery, -2.66% rides (shadow test) |
| **Stripe Radar** | block/allow payment | fraud -32% average; under 100 ms; 0.1% legit blocked |
| **Google Maps GNN** | ETA | bad-ETA outcomes down up to 50% |
| **Zendesk / TeamSystem** | AI agent deflection | up to 80% automated, NPS 53 → 59 |

<span class="small">Only the Uber rows are clean A/B or shadow tests. Stripe and Google figures are self-reported, mostly relative, with no baselines. Netflix, Booking, PayPal, Adyen, UPS ORION and others could not be fetched and are left out.</span>

---

## What actually moved

| Lever | Typical published change | Confidence in the evidence |
|---|---|---|
| **Cost** | -30% to -88% | high for Jack & Jill, RouteLLM, Not Diamond chatbot |
| **Latency** | 2x (Jev), <100 ms (Stripe), <10 ms (COTA) | medium |
| **Quality** | held within ~1 point, or traded for cost | medium |
| **Safety / risk** | jailbreaks 86% → 4.4%, fraud -32% | medium, vendor evals |
| **Human time** | handle time -7% to -10% | high for Uber A/B |

**Pattern: the decision layer rarely improves the answer. It cuts cost and latency at about the same quality, and it makes risk measurable.**

<span class="small">Analyst judgment, not a sourced finding.</span>

--

## Measure it for your own use

1. Label a set of real decisions (a few hundred).
2. Run Jev and the current model on it: `examples/jev/06_eval_decisions.py`.
3. Report cost per 1,000, median latency, accuracy, and the **miss rate at your threshold**.
4. Shadow-run, then A/B, before switching 100%.

Note: Jack & Jill went offline test, then production in 10 days. Copy that sequence.

---

## Sources and gaps

- Jev: [case study](https://typesafe.ai/blog/jack-jill-jev-case-study), [launch post](https://typesafe.ai/blog/introducing-system-one-models-and-jev), [evals](https://evals.typesafe.ai/)
- Routing and guardrails: `research/production-cases-b.md`
- Classic models: `research/production-cases-c.md`

<span class="small">Not verified: any figure beyond the fetched pages. WebSearch was blocked, so coverage is limited to pages we could fetch. WebFetch summarizes pages, so re-check a number before quoting it. No sourced intent-triage case with before/after metrics was found for LLM classifiers.</span>

---
