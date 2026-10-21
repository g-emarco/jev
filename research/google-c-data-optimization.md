# Google non-agent / decision-intelligence products (focus c)
Researched 2026-10-18. WebSearch was blocked by org policy; only WebFetch of official docs was used. Fetch tool summarizes pages, so some exact wording may be paraphrased. Claims without a source are marked UNVERIFIED. "When to use / not use" sections are analyst judgment (UNVERIFIED as Google guidance) unless a source is cited.

Note: Google has rebranded heavily. Docs now say "Gemini Enterprise Agent Platform" (formerly Vertex AI) and "Agent Search" (formerly Vertex AI Search). Old names still appear in older material.

## 1. Vertex AI Search -> "Agent Search" (AI Applications)
- What: Managed search and recommendations over websites/enterprise data, with semantic search, generative answers/summaries, embeddable widget, media and healthcare (FHIR) search, self-learning ranking from clickstream events. Uses Discovery Engine API. Being renamed Agent Search; docs mid-update. Source: https://docs.cloud.google.com/generative-ai-app-builder/docs/introduction
- Status: Only "custom recommendations" is labeled Preview on the intro page; page does not state GA for the rest (GA of core search UNVERIFIED from this page).
- Production use: site search, internal knowledge search, media recommendations, healthcare record search (same source).
- vs LLM agent: use when the job is retrieval/grounded answers over a corpus with ranking, ACLs and analytics out of the box; an agent adds multi-step action/tool use. Agent Search can be the retrieval tool for an agent. (judgment)
- Not for: computing/aggregating over structured data, optimization, or workflows needing actions. (judgment)
- Pricing/limits: pricing page returned no content to the fetcher (https://cloud.google.com/generative-ai-app-builder/pricing). Per-query/storage figures recalled from memory: UNVERIFIED.

## 2. Vertex AI RAG Engine
- What: Component of Gemini Enterprise Agent Platform for RAG: ingestion (local, GCS, Drive) -> chunking -> embedding -> indexing -> retrieval -> generation. Vector DB options include RagManagedDb (Spanner), Vector Search, Feature Store, Weaviate, Pinecone. VPC-SC and CMEK supported; data residency and AXT not. Source: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/rag-engine/rag-overview
- Status: GA in us-central1, us-east4 (allowlist for new projects), europe-west3, europe-west4 (open); Preview in many other regions (us-east1, europe-west1 allowlisted; asia-*, others open). Same source.
- Billing note: managed Spanner vector DB in GA locations is billed to you. Same source.
- vs agent: RAG Engine is the lower-level, developer-controlled retrieval layer (you build the app); Agent Search is the more turnkey option. (judgment)
- Not for: precise numeric/structured queries; low-latency deterministic decisions. (judgment)
- Limits: numeric quotas not obtained (page lists "Quotas and system limits" separately). UNVERIFIED.

## 3. BigQuery ML / BigQuery AI functions
- What: SQL-native generative and predictive functions. General-purpose: AI.GENERATE (text/image/audio/video/PDF in, optional structured output), AI.GENERATE_TEXT, AI.GENERATE_TABLE, AI.GENERATE_BOOL/DOUBLE/INT, AI.EMBED. Managed: AI.IF (filter), AI.SCORE (rank), AI.CLASSIFY, AI.AGG. Source: https://docs.cloud.google.com/bigquery/docs/generative-ai-overview
- Status (from release notes https://docs.cloud.google.com/bigquery/docs/release-notes, first 100k chars only):
  - AI.IF, AI.CLASSIFY, AI.SCORE: GA 2026-04-13; "optimized mode" for AI.IF/AI.CLASSIFY is Preview (also overview page).
  - AI.AGG: GA 2026-10-13 (output_schema arg GA 2026-10-14).
  - AI.FORECAST (TimesFM): univariate TimesFM 2.5 not marked Preview; TimesFM 3.0 and multivariate are Preview; TimesFM 3.0 moves to token-based pricing 2026-12-01. Source: https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-forecast
  - AI.GENERATE: GA/Preview status UNVERIFIED (not in the truncated portions read).
- AI.FORECAST limits: horizon 1-10,000 (2.5) / 1-1,024 (3.0); context up to 15,360 (2.5) / 2,048 (3.0); min 3 points per series; billed at BQML prediction rate. Source: forecast reference above.
- Cost/limits: pay for BigQuery compute plus Vertex charges for remote models; row-level failures (e.g. RESOURCE_EXHAUSTED) return NULL; max_error_ratio default 1.0 on AI.IF/CLASSIFY/SCORE; AI.COUNT_TOKENS to estimate. Source: generative-ai-overview URL.
- Production use: classify tickets, filter/rank reviews, extract fields from transcripts, demand forecasting at scale, embeddings/dedupe/semantic search (overview + forecast pages).
- vs agent: use for batch, set-based enrichment over many rows where data stays in the warehouse; no orchestration needed. (judgment)
- Not for: interactive multi-step tasks, tight per-row latency, or cases where silent NULLs on failure are unacceptable unless max_error_ratio is lowered.

## 4. Route Optimization API (successor of Cloud Fleet Routing)
- What: Google Maps Platform API producing optimized routes/assignments for vehicles and shipments under constraints (time windows, capacity, driver hours). Endpoints: OptimizeTours (blocking), OptimizeToursLongRunning, OptimizeToursUri (>8MB), BatchOptimizeTours. Some features (large vehicle routing, load costs, objectives, U-turn avoidance) are "Limited". Source: https://developers.google.com/maps/documentation/route-optimization/overview
- Relationship to Fleet Routing: the overview page does not mention it; claim that it succeeds Cloud Fleet Routing is UNVERIFIED here (the old cloud.google.com/optimization URL returned 404).
- Status: launch stage not stated on the overview page. Pricing page lists it as a billable SKU (see below), implying commercial availability; formal GA UNVERIFIED.
- Pricing (per 1,000 events): SingleVehicleRouting $10 first 100k, free 5,000/mo; FleetRouting $30 first 100k, free 1,000/mo, tiers decline to $2.10. Source: https://developers.google.com/maps/billing-and-pricing/pricing
- Production use: next-day logistics planning, on-demand delivery dispatch/insertion, field-service scheduling (overview).
- vs agent: use a solver for the combinatorial optimization itself; an LLM agent is the wrong tool for computing routes. Best pattern: agent gathers/validates inputs and calls this API as a tool. (judgment)
- Not for: non-routing optimization (scheduling without geography, general LP/MIP). (judgment)
- Size limits (vehicle/shipment counts): not stated. UNVERIFIED.

## 5. Vertex AI predictive: AutoML tabular, forecasting
- What: Tabular classification/regression (End-to-End AutoML workflow handles multi-TB, up to 1000 cols; managed AutoML), forecasting (Tabular Workflow for Forecasting is Preview, up to 1 TB / 200 cols; Forecasting with AutoML: TiDE, TFT, L2L, Seq2Seq+; BQML ARIMA_PLUS recommended as quick, cheap baseline; Prophet univariate). Source: https://docs.cloud.google.com/vertex-ai/docs/tabular-data/overview
- Status: current tabular AutoML/forecasting not on deprecations list. Legacy AutoML Tables shut down 2024-07-24; AutoML Text shut down 2025-06-15 (-> Gemini); AutoML Video shut down 2025-07-31. Source: https://docs.cloud.google.com/vertex-ai/docs/deprecations
  Caveat: the deprecation page was summarized by the fetcher; confirm no newer tabular entry.
- vs agent: use for numeric prediction (churn, demand, price) trained on your history; LLMs are poor and costly at this. Agent can call the model endpoint. (judgment)
- Not for: tiny datasets, or text/image tasks where AutoML Text/Video are gone (use Gemini). For simple time series, BigQuery AI.FORECAST/ARIMA_PLUS may be cheaper (judgment, supported by "recommended as baseline" in overview).
- Pricing/limits: not retrieved (pricing page too large). UNVERIFIED.

## 6. Document AI
- What: Extracts structured data from documents. Processors: Digitize (Enterprise Document OCR), Extract (Form Parser, Layout Parser, custom extractor, pretrained parsers), Classify (custom classifier/splitter). Integrates with GCS, BigQuery, Agent Search. Use cases: invoices, receipts, IDs, tax/loan forms, contracts. Source: https://docs.cloud.google.com/document-ai/docs/overview
- Status: overview page gives no GA/Preview per processor (UNVERIFIED); Gemini-based layout parser exists in docs nav, details not retrieved.
- vs agent: use as the deterministic-ish ingestion step with schemas, confidence scores, pre-trained parsers; agent consumes output. Direct Gemini extraction can be simpler for one-off/varied docs (judgment).
- Pricing: page returned no content; figures from memory UNVERIFIED. Quotas on separate page, UNVERIFIED.

## 7. Recommendations AI / Retail Search -> AI Commerce Search
- What: Ecommerce search and recommendations driven by catalog + user events. Renamed AI Commerce Search 2026-06-29 (earlier: Vertex AI Search for commerce, Vertex AI Search for retail, Retail Search), now in Gemini Enterprise for Customer Experience suite. Source: https://docs.cloud.google.com/retail/docs/release-notes
- Status: Recommendations AI GA 2021-01-15; Retail Search GA 2022-04-05; Conversational Commerce agent GA Sep 2025; old Recommendations Engine API frozen (migrate to Retail API). Same source.
- Integration: weeks; search migration to A/B test ~2-3 months; very sensitive to catalog/event data quality; never cache personalized results across users; sample of queries goes to third-party human raters (subprocessors). Source: https://docs.cloud.google.com/retail/docs/overview
- vs agent: use for ranking/personalization learned from behavior; an LLM agent has no click data. Use conversational layer on top where needed.
- Not for: low-traffic sites without event data (judgment, implied by data-sensitivity note). Pricing: not retrieved, UNVERIFIED.

## 8. Conversational Analytics (API and products)
- What: Conversational Analytics API (geminidataanalytics.googleapis.com) for building "data agents" answering natural-language questions over structured data using SQL, Python, visualization; multi-turn plus QueryData; A2A endpoints. v1 covers BigQuery, Looker, Data Studio; AlloyDB, Spanner, Cloud SQL (MySQL/Postgres) are Preview in v1beta, with no visualization for DB sources. Data QnA API is deprecated (migration guide). Source: https://docs.cloud.google.com/gemini/docs/conversational-analytics-api/overview
- Status: v1 endpoint for BQ/Looker/Data Studio suggests GA (page gives no explicit label; UNVERIFIED). BigQuery release notes mention conversational analytics GA covering agents using AI.IF/CLASSIFY/SCORE on 2026-06-23 (https://docs.cloud.google.com/bigquery/docs/release-notes). Looker Studio conversational analytics began Public Preview 2024-09-12 (https://docs.cloud.google.com/gemini/docs/release-notes; GA entry not found, may be truncated).
- vs agent: this is itself an LLM data-agent product; choose it over a custom agent for NL-to-SQL BI with governed semantics, build custom when you need actions beyond analysis. Google warns Gemini output may be plausible but wrong; validate.
- Not for: decisions needing guaranteed-correct numbers without review (Google's own validation warning). Pricing/quotas: separate pages, not retrieved (pricing URL 404). UNVERIFIED.

## Cross-cutting takeaways
- For decisions, pair a deterministic/statistical engine (Route Optimization, AutoML/BQML forecast, Commerce ranking) with an agent as orchestrator and explainer.
- Naming churn (Vertex AI -> Agent Platform, Vertex AI Search -> Agent Search, Search for commerce -> AI Commerce Search) means verify product names in contracts/IaC.
- Gaps to verify: AI.GENERATE stage, Agent Search core GA label, all pricing tables except Route Optimization and BQ AI.FORECAST, RAG Engine quotas, Route Optimization GA/Fleet Routing succession.
