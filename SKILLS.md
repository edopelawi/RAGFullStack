# SKILLS

Capabilities checklist by phase for the AI Knowledge Assistant.

## Blaster Mode (Local, Observable)
- Ingest: PDF/Markdown ingestion, chunking, embeddings; idempotent runs; metadata retained.
- Retrieve: vector similarity with Chroma/FAISS; returns scored chunks with IDs and source refs.
- Generate: grounded answers with citations; explicit "I don’t know" path; prompt/version tracked.
- Observability: Langfuse traces per request; token counts, latencies, retrieval spans, errors logged.
- API: FastAPI endpoints for ingest, query; simple health check; CORS configured for local frontend.
- Frontend: minimal chat UI with streaming responses and citation rendering.
- Tooling: Docker Compose for local; lint/format/test tasks; `.env.example` provided; no secrets committed.
- Tests: smoke test for ingest+query happy path; unit tests for chunking and retrieval.

## Beskar Mode (Deployed, Stable)
- Config: environment-based settings; secrets via env/manager; CORS allowlist.
- Reliability: `/healthz` and `/readyz`; request IDs across services; basic rate limiting; graceful fallbacks.
- Deploy: backend to Fly.io/Render; frontend to Vercel; persistent storage if needed.
- Observability: Langfuse cloud traces in prod; dashboards for latency, error rate, cost per query.
- Docs: ARCHITECTURE.md with diagram; docs/tradeoffs.md for key decisions; README updated for deploy.
- Tests: add integration tests against deployed env; measure cold-start latency and record.

## Darksaber Mode (Agentic, Adaptive)
- Advanced retrieval/decision: query planning or model routing; self-reflection on context sufficiency.
- Memory: session memory or history-aware retrieval; configurable retention.
- Evals: automated answer quality scoring; retrieval hit rate; user feedback loop.
- Observability: cost vs quality tracking; A/B harness; enhanced Langfuse dashboards.
- Resilience: stress-tested behavior; safe model swaps documented; rollback plan.

## How to Use This File
- When you add or change a capability, update the relevant phase checklist.
- Each PR should note which skills were touched and how they were tested.
- Keep scope tight: one evolution at a time.
- Maintain TODO.md with next steps/backlog so future runs have context.
