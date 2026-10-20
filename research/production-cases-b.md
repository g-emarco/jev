# Production cases B: small/fast "decision" models in LLM systems (fetched 2026-10-20)

Scope: model routing, guardrail/safety classifiers gating inputs or tool calls, intent/triage. Method: WebFetch only (it summarizes pages with a small model, so quotes are the summarizer's rendering of the page, not verbatim copies) plus curl of arXiv HTML for two papers, which I read directly. Anything marked UNVERIFIED could not be confirmed. "Analyst judgment" labels are mine.

## Summary table

| # | Product | Decision | Headline metric | Evidence type |
|---|---|---|---|---|
| 1 | RouteLLM (LMSYS/UC Berkeley/Anyscale) | strong vs weak LLM | up to 85% cost cut (MT Bench) at 95% GPT-4 quality | research, public benchmarks |
| 2 | Not Diamond, own chatbot | cheaper vs quality-max model | 51% inference cost cut, about $750k/yr | vendor self-report, observational |
| 3 | Not Diamond Code | model per coding-agent step | 20-80% cost reduction vs Opus xhigh | vendor benchmarks, 2026 |
| 4 | AWS Bedrock Intelligent Prompt Routing | Sonnet vs Haiku / Llama 70B vs 8B | "up to 30%" cost cut | vendor claim, preview at announcement |
| 5 | Azure Foundry model router | pick model per prompt | no numbers published on fetched pages | docs only |
| 6 | Anthropic Constitutional Classifiers v1 | block jailbreak in/out | jailbreak success 86% to 4.4% | vendor eval + red team |
| 7 | Anthropic Constitutional Classifiers++ | same, cascaded | overhead 23.7% to about 1%; refusals 0.05% | vendor, production traffic |
| 8 | Claude Code auto mode | allow/block tool call | FPR 0.4%, FNR 17% (real overeager actions) | vendor engineering post |
| 9 | Meta Llama Guard | prompt/response safety | AUPRC 0.945 vs 0.764 (OpenAI API), own set | paper |
| 10 | NVIDIA NeMo Guardrails safety recipe | safety gate with NemoGuard NIMs | content safety 88% to 94% | vendor blog |
| 11 | Cloudflare AI Gateway Guardrails | block/flag by hazard category | none published | product blog |

## Cases

### 1. RouteLLM (routing, research with open-source release)
- Decision: per query, send to a strong model (GPT-4 Turbo) or weak model (Mixtral 8x7B). Routers: similarity-weighted ranking, matrix factorization, BERT classifier, causal-LLM classifier, trained on Chatbot Arena preference data.
- Metrics (LMSYS blog, 2024-07-01): "cost reductions of over 85% on MT Bench, 45% on MMLU, and 35% on GSM8K" vs GPT-4 only, while reaching 95% of GPT-4 performance.
  - MT Bench, Arena data only: matrix factorization reaches 95% of GPT-4 quality with 26% GPT-4 calls (about 48% cheaper than random). With LLM-judge augmentation: 14% GPT-4 calls, 75% cheaper than random.
  - MMLU: Arena-only routers near random; with about 1500 golden-label samples (under 2% of training data) the causal-LLM router needs 54% GPT-4 calls for 95% quality (14% cheaper than random).
  - Versus commercial routers (Martian, Unify): matched on MT Bench while "over 40% cheaper".
  - Transfer: same routers, no retraining, Claude 3 Opus / Llama 3 8B pair gave comparable results.
- Paper (arXiv 2406.18665, read directly via HTML, v4 Feb 2025): abstract says "reduce costs by over 2 times without sacrificing response quality". Table 6 cost-saving ratio vs GPT-4: MT Bench 3.66x at 95% GPT-4 quality; MMLU 1.41x at 92%; GSM8K 1.49x at 87%. Cost assumption: GPT-4 $24.7/M tokens, Mixtral $0.24/M. Router overhead (Table 7): $3.19 to $39.26 per million requests; matrix factorization 155 req/s on one L4 GPU.
- Caveat (analyst judgment): the 85% headline is MT Bench, which is in-distribution for Arena data; MMLU/GSM8K needed data augmentation, and the 35% GSM8K figure has 87% quality, not 95%. The paper's Table 6 is more conservative than the blog headline.
- Sources: https://lmsys.org/blog/2024-07-01-routellm/ ; https://arxiv.org/abs/2406.18665
- Status: research + open-source framework; not a documented production deployment by one company. CONFIRMED numbers.

### 2. Not Diamond running its own chatbot (routing, production, vendor self-report)
- Decision: when a request carries a cost tradeoff, check whether a cheaper or faster model can handle it without lowering quality. Change on Sept 12 (2024) replaced default quality-only routing, described as one edited line of code.
- Metrics (post dated 2024-10-15): "51% in inference costs", "$750,000 in savings on an annualized basis". Quality proxy is engagement only: 90th-percentile user 23 to 21 messages/day; median 5 to 4; week-over-week message growth 43% vs 16% the week before.
- Caveats: no controlled experiment (post admits this); models in the pool not named; no absolute baseline cost; promotional source. Analyst judgment: the engagement drop at p90 and median is small but nonzero, so "no impact" is an interpretation.
- Source: https://www.notdiamond.ai/blog/using-not-diamond-to-reduce (title: "Using Not Diamond to reduce Not Diamond's inference costs by 51% (with one line of code)")
- Status: production at the vendor; numbers CONFIRMED as stated by the vendor, not independently validated.

### 3. Not Diamond Code (routing for coding agents, vendor, 2026)
- Decision: choose model per step in a coding-agent trajectory, cache-aware.
- Metrics (Sept 2026 post): router scores 50.7% at $4.28/attempt (SWE-Interact), 67.6% at $4.16 (SWE-Together), 57.6% at $3.00 (Dialogue SWE-Bench-Pro); described as Pareto dominant, matching or beating Opus xhigh with "20-80% cost reduction". Adding GLM 5.2 and DeepSeek V4 Flash to the pool (internal Poly-SWE-Bench): accuracy +3.6%, savings vs Opus xhigh 39% to 66%.
- Baseline single-model numbers only appear in scatter plots, so not quotable. A July 2026 post from the same vendor claims "cuts inference cost by 30%+ without lowering quality" with no data, and a May 2026 post gives "30-90%" savings for techniques generally with no router-specific numbers (UNVERIFIED, marketing).
- Sources: https://www.notdiamond.ai/blog/interactive-benchmarks-a-new-methodology-for-evaluating-model-routing ; https://www.notdiamond.ai/blog/how-to-control-coding-agent-costs-with-intelligent-model-routing ; https://www.notdiamond.ai/blog/how-to-reduce-claude-code-costs-without-sacrificing-output-quality
- Status: product; benchmarks are vendor-authored, newly designed ("interactive benchmarks"). Treat as vendor claim.

### 4. AWS Bedrock Intelligent Prompt Routing
- Decision: route between Claude 3.5 Sonnet and Claude 3 Haiku (Sonnet fallback), or Llama 3.1 70B and 8B (70B fallback), using predicted response-quality difference (criterion 0.26 Anthropic, 0.0 Meta in the post's example).
- Metric: "reduce costs by up to 30 percent without compromising on accuracy." (Prompt caching, separate feature: up to 90% cost and 85% latency.) No methodology or benchmark given in the post. Demo: complex "Alice" question went to Sonnet; "hello world" to Haiku.
- Constraints: English only; no routing surcharge during preview.
- Source: https://aws.amazon.com/blogs/aws/reduce-costs-and-latency-with-amazon-bedrock-intelligent-prompt-routing-and-prompt-caching-preview/ (2024-12-04)
- Status: preview at announcement; current GA status UNVERIFIED (not fetched). "Up to 30%" is a ceiling claim, not an average.

### 5. Azure / Microsoft Foundry model router
- Decision: a "trained language model" / "purpose-built ML model" picks an underlying model per prompt (complexity, reasoning, task type). Modes: Balanced (default; picks cheapest within about 1-2% quality of best), Cost (within about 5-6%), Quality.
- Metrics: no cost, latency or accuracy numbers on either fetched page. Docs claim "negligible fraction of the LLM inference time" overhead and savings "validated on both in-domain and out-of-domain benchmarks" without figures. Pool (version 2025-11-18, updated in place) spans OpenAI, Anthropic, xAI, DeepSeek, Meta and Fireworks models.
- Sources: https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/model-router ; https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/model-router-how-it-works (pages updated 2026-10-19)
- Status: active product. Before/after metrics UNVERIFIED (none found). Include only as an existence proof of a managed small router; analyst judgment: the 1-2% / 5-6% quality bands are design parameters, not measured outcomes.

### 6. Anthropic Constitutional Classifiers (guardrail, input and output)
- Decision: classifier models screen prompts and completions against a constitution; block on violation.
- Metrics (10,000 synthetic jailbreak prompts): jailbreak success 86% without classifiers to 4.4% with; over-refusal +0.38% (not statistically significant, 5,000 conversations); compute overhead 23.7%. Red team: 183 participants, over 3,000 hours, up to $15,000 rewards, no universal jailbreak on the prototype. Public demo (Feb 2025): 339 jailbreakers, over 300,000 interactions, about 3,700 hours; four cleared all eight levels, one found a universal jailbreak; $55K paid out.
- Source: https://www.anthropic.com/research/constitutional-classifiers
- Status: deployed for ASL-3 protections per Anthropic (deployment claim not verified from this page; UNVERIFIED). Numbers CONFIRMED as vendor-reported.

### 7. Anthropic Constitutional Classifiers++ (cascade)
- Decision: stage 1 linear probe on model activations screens all traffic; flagged exchanges go to a probe-classifier ensemble using a single "exchange" classifier (sees output together with input).
- Metrics (post dated 2026-01-09): compute overhead about 1% (on Opus 4.0 traffic) vs 23.7% before; refusal on harmless production queries 0.05% over one month on Sonnet 4.5 traffic ("87% drop" from original); over 1,700 red-team hours, 198,000 attempts, no universal jailbreak found; one high-risk vulnerability at 0.005 per thousand queries. Exchange classifier alone cut successful jailbreaks by more than half at +50% compute.
- Source: https://www.anthropic.com/research/next-generation-constitutional-classifiers
- Status: production-traffic measured refusal rate; CONFIRMED as vendor-reported. Analyst judgment: the cascade pattern (cheap probe first, expensive classifier on flagged traffic) is the transferable idea, and it matches the auto mode design below.

### 8. Claude Code auto mode (gating tool calls)
- Decision: per tool call, a transcript classifier (Sonnet 4.6) returns block/allow. Stage 1 is a single-token fast filter; stage 2 adds chain-of-thought only on stage-1 flags. It sees user messages and tool calls only (assistant text and tool results stripped, as a prompt-injection defense). Escalates to the human after 3 consecutive or 20 total denials.
- Problem stated: users approve "93%" of permission prompts (approval fatigue). The post gives no figure for how many prompts auto mode removes (UNVERIFIED).
- Metrics (post dated 2026-03-25):

| Stage | FPR, real traffic (n=10,000) | FNR, real overeager actions (n=52) | FNR, synthetic exfiltration (n=1,000) |
|---|---|---|---|
| Stage 1 | 8.5% | 6.6% | 1.8% |
| Full pipeline | 0.4% | 17% | 5.7% |

- The authors call the 17% miss rate "the honest number". Small n=52 means wide uncertainty (analyst judgment).
- Source: https://www.anthropic.com/engineering/claude-code-auto-mode (the /news/ URL variant returned 404)
- Status: shipped feature; metrics vendor-reported.

### 9. Meta Llama Guard (open input/output safeguard)
- Decision: Llama2-7b instruction-tuned classifier labels prompt or response safe/unsafe against a customizable taxonomy.
- Metrics (arXiv 2312.06674 HTML, Table 2, AUPRC): own test set prompts 0.945 (Llama Guard) vs 0.764 (OpenAI Mod API) vs 0.728 (Perspective); OpenAI Mod dataset 0.847 vs 0.856 vs 0.787; ToxicChat 0.626 vs 0.588 vs 0.532; own test set responses 0.953 vs 0.769 vs 0.699. Few-shot prompting reaches 0.872 on OpenAI Mod, above the OpenAI API's 0.856.
- Caveat: own-test-set wins are on the taxonomy it was trained for; on OpenAI Mod zero-shot it is slightly below the API. This is a benchmark, not a production before/after.
- Source: https://arxiv.org/abs/2312.06674 (numbers from https://arxiv.org/html/2312.06674)
- Status: open weights; deployed downstream (see case 11).

### 10. NVIDIA safety recipe with NemoGuard NIMs (NeMo Guardrails ecosystem)
- Decision: content-safety, topic-control and jailbreak-detect small models (Llama 3.1 Nemoguard 8B Content Safety / Topic Control, Nemoguard Jailbreak Detect) gate inputs/outputs; recipe also evaluates and post-trains a baseline open-weights model.
- Metrics: content safety 88% to 94% ("6% improvement ... no measurable accuracy degradation"); product security (garak) 56% to 63%. No latency figure in the post. Baseline model not named.
- Source: https://developer.nvidia.com/blog/safeguard-agentic-ai-systems-with-the-nvidia-safety-recipe/
- Status: vendor blog. The NeMo Guardrails overview page (docs.nvidia.com) had no effectiveness or latency numbers. Earlier NVIDIA NIM guardrail launch blogs (compliance-rate, latency claims) I tried returned 404, so those claims are UNVERIFIED.

### 11. Cloudflare AI Gateway Guardrails
- Decision: Llama Guard 3 8B on Workers AI classifies prompts and/or responses; each hazard category set to ignore, flag, or block. Example: a request categorized S2 (Non-Violent Crimes), `safe: false`, blocked before reaching `gpt-4o-mini`; user sees "Prompt blocked due to security configurations"; no tokens incurred.
- Metrics: none published (no latency, accuracy, or flag rates). Text-only; billed as Workers AI usage.
- Source: https://blog.cloudflare.com/guardrails-in-ai-gateway/
- Status: product. Before/after metrics UNVERIFIED (none found).

## Gaps and what I could not confirm
- Intent/triage classifiers: no sourced case with before/after metrics found in the pages I could reach. Not claiming any.
- Not reachable (404 or no data): Martian router benchmark page, OpenRouter Auto Router docs (tried two URLs), Databricks, Cursor, NVIDIA NIM guardrail launch blogs, Azure techcommunity GA post (login redirect). All UNVERIFIED; do not cite.
- WebFetch could not parse PDFs; arXiv HTML was used instead for cases 1 and 9.
- Analyst judgment (overall): published metrics split into (a) vendor self-reports with weak quality evidence (cases 2, 3, 4, 10), (b) research with public benchmarks (1, 9), (c) vendor safety evals with explicit error rates (6, 7, 8). Only 7 and 8 report error rates measured on real production traffic, and only 2 reports a real-world cost before/after.
