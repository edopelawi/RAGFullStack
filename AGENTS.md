# AGENTS

Shared rules and roles for building the AI Knowledge Assistant (RAG) system.

## Principles
- Clarity over cleverness; small, reviewable changes.
- Instrument before deploying; traces are part of the feature.
- No secrets in git. Use `.env.local` and secret managers; commit `.env.example` only.
- Deterministic, typed, and tested code where possible.
- Cost-aware by default; choose the cheapest tool that meets requirements.
- Keep TODO.md current: add new work, remove or mark done anything obsolete, and update next steps as you make changes.

## Default Stack (Blaster Mode)
- Backend: FastAPI (Python), async-first.
- Vector DB: Chroma (local) or FAISS (in-process) for zero-cost local.
- LLM: API-based (e.g., OpenAI-compatible endpoint) or local model if available.
- Frontend: Vite + React (lightweight) or Next.js if SSR is needed later.
- Observability: Langfuse (cloud free tier) with traces for each request.
- Packaging: Docker Compose for local orchestration.

## Coding Standards
- Language: Python 3.11+ backend; TypeScript frontend.
- Style: black + isort; ruff for linting; mypy for backend typing (strict-ish, allow untyped deps); eslint + prettier for frontend.
- Tests: pytest with unit and light integration; 1–2 happy-path smoke tests per service; contract tests for API schemas where possible.
- Docs: keep READMEs per service; update SKILLS.md when capabilities change.
- Reviews: require at least one review (self-review if solo: checklist + trace of what was tested).

## Security & Ops Defaults
- Secrets: never commit keys; use env vars; provide `.env.example` without secrets.
- Logging: avoid PII; redact user inputs if sensitive; include request IDs and latency.
- Network: enable CORS with allowlist; set basic rate limits in the API.
- Health: `/healthz` lightweight; `/readyz` checks downstreams when added.
- CI: run lint + tests on PRs; fail on missing format/lint.

## Observability Requirements (Blaster)
- For each request: trace spans for ingestion, retrieve, rerank (if any), generate.
- Capture: prompt, model, token usage, retrieval chunk IDs and scores, latency per step, success/error status.
- Store evaluation-ready data: question, answer, cited sources, trace ID.

## Roles
- Ingestion Agent: handles document intake, chunking, metadata, embeddings; exposes idempotent ingestion jobs.
- Retrieval Agent: designs vector schema, similarity search, filters, rerank (optional); returns scored contexts.
- Generation Agent: prompt templates, guardrails, citation formatting; enforces "I don’t know" path.
- Frontend Agent: chat UI, streaming UX, citation display, latency surfacing; minimal local-first UI.
- Infra/DevEx Agent: Docker Compose, env wiring, Makefile/task runner, CI, lint/format hooks.
- Observability/Evals Agent: Langfuse setup, trace coverage, basic eval harness (golden Q&A set), cost/latency dashboards.

## Handoffs & Checks
- Ingestion → Retrieval: schema and metadata contract documented.
- Retrieval → Generation: context format and ranking contract documented.
- Backend → Frontend: typed API schema (OpenAPI/TS types) and error shapes agreed.
- Before merge: lint, tests, smoke run (local), trace captured for a sample query.
