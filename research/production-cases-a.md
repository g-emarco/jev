# Jev (TypeSafe AI): public name meaning, customers, metrics (fetched 2026-10-20)

Note: all pages were read via WebFetch, which returns a small-model summary of the page, not verbatim text. Numbers below are as summarized and should be re-checked against the live pages before being quoted. Everything here is vendor-published; nothing is independently verified. Analyst judgment is labeled as such.

## 1. What it is / status
- Jev is TypeSafe AI's first public "System One Model": returns typed decisions (Noul = yes/no probability, Choice, Score) with probabilities and confidence, not prose. Trained with "RLCD" (Reinforcement Learning for Calibrated Decisions). Early access; waitlist. Versions: jev-1.13.0, jev-1.14.0 (released 2026-10-14); aliases jev-latest (1.13.0 at fetch time), jev-preview (1.14.0). Price $42 per billion input tokens ($0.042/M), output free. Context 64k default, 262k with long-context header. Not fine-tuned on customer data.
- Founder/author: Diogo Almeida (ex-OpenAI), per the launch post. "2 years in stealth".
- langchain-typesafe on PyPI: 0.0.1a3, pre-release, MIT, published 2026-09-20 (a1/a2 on 2026-09-17), maintainer account "langchain". Note: typesafe.com redirects to akka.io (the older Typesafe/Lightbend company); it is unrelated. The relevant domain is typesafe.ai.

## 2. (a) Meaning of the name
- Per the launch post: named after economist William Stanley Jevons (Jevons paradox: cheaper efficiency drives more demand; the team expects the same for machine intelligence). "System One" refers to Kahneman's System 1 / System 2. Source: https://typesafe.ai/blog/introducing-system-one-models-and-jev (post dated Sep 15, 2026; page metadata says Oct 19, a conflict).
- Not explained on the LangChain provider page, PyPI page, docs.typesafe.ai/models, typesafe.ai home, or the 1.14 post. Not an acronym per the sources found.

## 3. (b) Named customers in production
- One named customer: Jack & Jill (AI talent marketplace; self-reports 5,000+ companies, 400,000+ professionals, $60M raised, UNVERIFIED by me). Source: https://typesafe.ai/blog/jack-jill-jev-case-study (article dated Oct 7, 2026; metadata Oct 19). Vendor-published; quote from Jack & Jill co-founder/CEO Matthew Wilson.
  - Jev replaced Gemini 3.1 Flash Lite for 100% of calls in the first scoring stage of candidate matching (6,000 candidates/role/day scored, top 2,000 shortlisted, then a stronger model narrows). 10 days from first test to production.
  - Reported as used across 15+ workflows (also CV editor, company classification, marketplace filtering, profile check). UNVERIFIED beyond the vendor post.
- No other customers named anywhere: LangChain provider page, PyPI, docs.typesafe.ai/models, evals.typesafe.ai, the launch post, the 1.14 post, and the GitHub adapter repo ("Used by" empty) all name none. The home page lists only Jack & Jill. Docs mention enterprise plans/zero data retention but no names.
- The "Stripe" in the LangChain/PyPI examples is an illustrative support message, not a customer.

## 4. (c) Published metrics
Jack & Jill case study (Gemini -> Jev), offline test on 150 live roles with same candidates:
- Cost per 1,000 candidates $0.755 -> $0.092 (-88%, token cost only).
- Median screening time 20.3s -> 10.3s (about 2x).
- Winners retained in shortlist 93.9% -> 94.6% (+0.7 pts; 90% CI -0.4 to +1.8, NOT statistically significant). AUC 0.924 -> 0.933.
- Savings $265K/yr at current volume; ~$500K projected over 12 months with growth. Profile check about 3.6s -> about 0.2s "with better accuracy" (no figures).
- Inconsistency flagged by the fetch: Wilson quote "saved ~half a million dollars last week" vs the article's $265K/yr current and $500K 12-month projection. UNVERIFIED which is right.
- The post does not name or cost the stronger second-stage model. "No loss in quality" overstates a non-significant offline result (analyst judgment).

Vendor home page (https://typesafe.ai): "193.6x faster, 444.6x cheaper"; example $0.000081 / 0.114s for Jev vs $0.013880 / 8.566s for LLMs; "238x lower than Claude Fable 5.1" price; "zero hallucinations". Per the launch post, the 193.6x/444.6x comes from 4 vendor workflow evals and "is at the high end of real-world gains" (author's words); type errors "0%" is by schema construction, not empirical; latency 70-500ms measured from team laptops on the West Coast; author admits pricing cannot be proven unsubsidized.

Workflow evals (https://evals.typesafe.ai/, vendor-run, 4 tasks: security incidents, agent trace observability, invoice processing, customer service). Reference labels = average of GPT-6 Astra and Claude Fable 5.1, so accuracy is agreement with those models, not ground truth:
- Jev workflow accuracy 67.8% avg, $0.0004 and 0.4s per case; Sonnet 5 workflow 67.8% at $0.1174; Sol 74.1% ($0.0836); Opus 5 73.1% ($0.1761).
- Per task Jev: security 61.7%, trace observability 71.6%, invoice 61.8% (vs Sol 79.1%, Opus 5 78.4%), customer service 76.0%.
- Analyst judgment: Jev matches mid-tier LLMs on accuracy at roughly 100-400x lower cost, but trails the top models notably on invoice processing; claims are self-reported against LLM-derived labels.

docs.typesafe.ai/models: no benchmarks or latency figures, only pricing and limits.
LangChain provider page and PyPI: no customers, accuracy, latency or cost figures.

## 5. Not found
- No independent third-party benchmarks, reviews, or case studies.
- No other named production customers besides Jack & Jill; no named LangChain-based production deployments.
- No explanation of the name beyond the Jevons reference in one blog post.
- Not fetched: docs.typesafe.ai/confidence, /concepts/system-one, the Jev 1.13 "jaggedness" page, the llm-benchmarks site.

## Source URLs
- https://docs.langchain.com/oss/python/integrations/providers/typesafe
- https://pypi.org/project/langchain-typesafe/
- https://typesafe.ai
- https://typesafe.ai/blog/jack-jill-jev-case-study
- https://typesafe.ai/blog/introducing-system-one-models-and-jev
- https://typesafe.ai/blog/jev-1-14
- https://docs.typesafe.ai/models
- https://evals.typesafe.ai/
- https://github.com/typesafe-ai/system-one-adapter-python (398 stars, 61 forks at fetch; MIT)
- https://typesafe.com (301 to akka.io; unrelated)
