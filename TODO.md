# TODO / Next Tweaks

- Add Langfuse tracing around ingest/query; capture prompts, contexts, token usage, latencies.
- Add a simple ingest helper (CLI script or frontend form) to send docs to /ingest.
- Enable streaming answers (server-sent events or chunked responses) for better UX.
- Add tests: pytest for ingestion/retrieval happy path, frontend smoke, and CI to run lint/tests.
- Document deployment steps for Beskar (Fly.io/Render backend, Vercel frontend) and env mappings.
- Add persistence notes: confirm Chroma volume and backup/restore steps.
