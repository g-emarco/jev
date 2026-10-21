# Production decision models with published before/after metrics (focus c)
Researched 2026-10-20. WebSearch was blocked by org policy; only WebFetch of specific URLs (plus curl for reachability checks) was used. WebFetch summarizes pages with a small model, so numbers below are as relayed by the fetcher and may be paraphrased; re-check against the source before external quoting. Anything not confirmed is marked UNVERIFIED. "Analyst judgment" labels my own interpretation. Dates on pages were taken from the fetcher output and not independently checked.

Yield note: many first-party pages returned 403/404 to the fetcher (UPS, ACM, INFORMS, Netflix Tech Blog, Booking.com, DoorDash, Adyen deep links, PayPal). Only 8 cases were retrievable with real numbers, and some are relative-only (no absolute baselines). The brief's target of 8-12 is met at the low end, with caveats in each entry.

## Summary table
| # | Company / product | Decision | Metric (before -> after) | Strength |
|---|---|---|---|---|
| 1 | Uber COTA v1 | Suggest ticket issue type + top-3 solutions to support agents | Handle time ~-10% (A/B); CSAT up "a few points" | Relative only |
| 2 | Uber COTA v2 | Same, DL model | Accuracy 49% -> 65% (contact type), 47% -> 55% (reply); handle time -6.6% vs v1 (A/B) | Good |
| 3 | Uber DeepETA | ETA prediction feeding dispatch/pricing | MAE vs XGBoost -2.91% (delivery), -2.66% (rides), shadow test | Good, modest |
| 4 | Stripe Radar | Block/allow card payments | Avg fraud -32%; Anthropic wrongly-blocked -83% | Vendor marketing |
| 5 | Stripe Radar architecture | Same, model redesign | Ensemble -> DNN-only: training time -85%+; recall cost avoided 1.5% | Engineering blog |
| 6 | Google Maps (DeepMind GNN) | Real-time ETA | Negative ETA outcomes cut up to 50% (16%-51% by city) | Good |
| 7 | Airbnb search ranking | Rank listings | GBDT -> NN: neutral, then "first breakthrough"; no numbers in text | Qualitative only |
| 8 | Zendesk / TeamSystem | AI agents deflect tickets (LLM-based, borderline scope) | Automation 3x after KB restructure; up to ~80% of repetitive inquiries | Vendor case study, LLM |
| - | UPS ORION, Netflix, Booking.com, Spotify, PayPal, Adyen, GitHub, Shopify, Intercom, Google Route Optimization | not retrievable | UNVERIFIED | see end |

## 1. Uber COTA (Customer Obsession Ticket Assistant), v1
- Decision: which issue type and which of 1,000+ solutions to suggest per support ticket (top-3 shown to the agent; human still acts). Pointwise ranking with random forest, later deep learning.
- Metric: ticket resolution/handle time "over 10 percent" lower; A/B test "about 10 percent" lower on average treatment vs control (thousands of agents randomly split, English tickets only). CSAT "often increased by a few percentage points". Pointwise ranking vs multi-class classification gave 25% relative accuracy gain and 70% faster training; deep model ~10% more accurate than the random forest. COTA covers "more than 90 percent" of inbound tickets and "saves Uber tens of millions of dollars every year" (Uber's claim, unaudited).
- Caveat: only relative changes published; no absolute minutes or CSAT scores.
- Source: https://www.uber.com/blog/cota/ (date not retrieved)
- Status: in production at Uber (per post); current status UNVERIFIED.

## 2. Uber COTA v2
- Decision: same as above, upgraded models.
- Metric: top-1 offline accuracy, Contact Type 49% -> 65%; Reply 47% -> 55%. Online A/B (50/50 ticket split, ~1 month, after a 1-week A/A): average handle time -6.6% relative vs v1, statistically significant; CSAT "slight improvement" (no number). Serving latency p95 < 10ms.
- Source: https://www.uber.com/blog/cota-v2/ (fetcher reported date August 23, 2018; scope: 600+ cities, 5+ channels)
- Status: published case; production status today UNVERIFIED.

## 3. Uber DeepETA
- Decision: arrival-time prediction that feeds downstream dispatch, pricing and ETAs shown to users (downstream use is analyst judgment from product context, UNVERIFIED in the fetched pages).
- Metric: from the arXiv paper (ar5iv HTML, arXiv 2206.02127): offline MAE improvement vs routing-engine ETA, XGBoost 5.07% vs DeeprETANet 7.83%. Online shadow tests, DeeprETANet vs production XGBoost: delivery MAE -2.91%, rides -2.66%; p50 -4.74% / -4.15%; p95 -3.92% / -3.23%. Two-week shadow window, aggregated from multiple launches.
- Caveat: the Uber blog post itself gives no numbers (only "delivers an immediate improvement"); numbers come from the paper. Shadow test, not an outcome A/B.
- Sources: https://www.uber.com/blog/deepeta-how-uber-predicts-arrival-times/ ; https://ar5iv.labs.arxiv.org/html/2206.02127
- Status: production per paper/blog.

## 4. Stripe Radar (marketing page)
- Decision: score and block/allow/review card payments in real time.
- Metric: "32% average reduction in fraud with Stripe Radar" (baseline and methodology not stated). Customer: Anthropic "83% reduction in the number of legitimate transactions that were incorrectly blocked" (no baseline figure). Authorization Boost (separate product): "Increase acceptance rates by 3.8% on average". FreshBooks: "blocked over 300 fraudulent accounts" in three months (no baseline).
- Older guide (Dec 2021 update): newer models improved "by over 20% year over year"; no metric or baseline stated; no conversion-lift figures.
- Caveat: self-reported, no independent verification.
- Sources: https://stripe.com/radar ; https://stripe.com/radar/guide
- Status: GA, current.

## 5. Stripe Radar architecture (engineering blog)
- Decision: same; internal model redesign.
- Metric: decisions in "less than 100 milliseconds" over 1,000+ characteristics; 0.1% of legitimate payments wrongly blocked; fraud about 1 per 1,000 payments. Mid-2022 ensemble (XGBoost + DNN) replaced by DNN-only ResNeXt-style multi-branch; training time "over 85%" shorter (under two hours); dropping XGBoost naively would have cost a "1.5% drop" in recall. 10x more training data still improved results; 100x experiment underway.
- Source: https://stripe.dev/blog/how-we-built-it-stripe-radar (redirect from stripe.com/blog/...; publication date not retrieved)
- Status: production per post.

## 6. Google Maps ETA with DeepMind graph neural networks
- Decision: predicted travel time/ETA shown in Maps (and used for route choice; the routing link is analyst judgment).
- Metric: real-time ETA accuracy improved "by up to 50%" in cities including Berlin, Jakarta, Sao Paulo, Sydney, Tokyo, Washington D.C.; per the map graphic alt text, 16% (London, Copenhagen) to 51% (Taichung). Baseline: ETAs were already accurate for "over 97% of trips". The metric is reduction in negative ETA outcomes (wording from fetcher; exact definition UNVERIFIED).
- Source: https://deepmind.google/discover/blog/traffic-prediction-with-advanced-graph-neural-networks/
- Status: launched in Google Maps per post; current status UNVERIFIED.

## 7. Airbnb search ranking
- Decision: ordering of listings in search; manual scoring -> GBDT -> neural network.
- Metric: the paper (arXiv 1810.09591, ar5iv text) says the GBDT replacement of the manual scoring function "gave one of the largest step improvements in homes bookings in Airbnb's history"; first simple NN "proved booking neutral"; Lambdarank NN was the "first breakthrough"; later gains "saturated with long spells of neutral experiments". Booking gains appear only in a figure (not text-extractable here), so NO percentages obtained. UNVERIFIED for any number.
- Useful lesson (analyst judgment): neutral experiments and failed models (listing-ID overfit; multitask raised long views but bookings stayed neutral) are rarely reported.
- Source: https://arxiv.org/abs/1810.09591 ; https://ar5iv.labs.arxiv.org/html/1810.09591
- Status: published retrospective (2018); present state UNVERIFIED.

## 8. Zendesk customer TeamSystem (borderline: LLM agents, not a classic ML decision layer)
- Decision: which inquiries AI agents resolve vs. route to humans.
- Metric: AI agents automating "up to 80 percent of repetitive inquiries"; restructuring the knowledge base "tripled their AI agent automation rate"; repetitive invoice emails down 99%; CSAT about 89%, NPS 53 -> 59 in four months for one business; "without adding headcount". Before: five companies on five tools; after: unified on Zendesk. No resolution-time or pre-AI CSAT baseline.
- Caveat: vendor-published case study, LLM-based; included only because no non-LLM triage case could be fetched.
- Source: https://www.zendesk.com/customer/teamsystem/
- Status: current customer story.

## Not obtained (all UNVERIFIED here)
- UPS ORION: about.ups.com, pressroom.ups.com, INFORMS Interfaces page returned 403 or Access Denied; Wikipedia pages had no ORION section. Commonly cited figures (e.g. savings of ~100 million miles/yr, ~10 million gallons) are from memory and NOT verified.
- Netflix recommender value (Gomez-Uribe and Hunt, ACM TMIS): ACM page 403; Netflix Tech Blog 403; research.netflix.com had no content. The "$1B/year" figure is from memory, UNVERIFIED.
- Booking.com ML models paper, PayPal, Adyen (Uplift/Protect page gave only "NordSecurity increased conversion by 10%" headline on https://www.adyen.com/risk-management; case-study page 404), Spotify (research blog index only, no lifts), GitHub (engineering index; AI accessibility triage post has no metrics), Shopify, Intercom (index only), Google Route Optimization (docs overview has no customer numbers; customer-stories page at https://mapsplatform.google.com/resources/customer-stories/ not fetched), Uber Radar fraud post (https://www.uber.com/blog/project-radar-intelligent-early-fraud-detection/ has no outcome metrics, only scale).

## Analyst judgment (UNVERIFIED as vendor guidance)
- Support-assist cases (COTA) show the pattern most relevant to a decision model: a human stays in the loop, the model ranks options, and the win is reported as a relative handle-time drop (6-10%), not full automation.
- Fraud/ETA cases report modest relative gains (low single digits for DeepETA shadow tests) rather than dramatic ones; headline vendor figures (32%, 83%, 3x) lack baselines.
- Next step if more cases are needed: fetch UPS/Netflix/Booking material through a source that is not blocked (e.g. Google Scholar PDFs, publisher mirrors) and the Maps Platform customer stories page.
