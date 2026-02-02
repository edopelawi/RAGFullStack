# RAG Full Stack

This project is my playground to learn about the recent AI Engineering - how to create, deploy, and maintain an RAG application in production.

This project is [MIT-licensed.](LICENSE)

This is the way.

## Local run (Docker Compose)

1) Copy env template and set keys:

```
cp .env.example .env.local
# set OPENAI_API_KEY, LANGFUSE_PUBLIC_KEY/SECRET_KEY (if using Langfuse Cloud)
```

2) Start services:

```
docker compose up --build
```

3) Test health:

- Backend: http://localhost:8000/healthz
- Chroma: http://localhost:8001/api/v1/heartbeat

4) Ingest docs (example request):

```
curl -X POST http://localhost:8000/ingest \
	-H "Content-Type: application/json" \
	-d '{
				"documents": [
					{"id": "doc1", "content": "The sky is blue", "metadata": {"source": "demo"}}
				]
			}'
```

5) Query:

```
curl -X POST http://localhost:8000/query \
	-H "Content-Type: application/json" \
	-d '{"question": "What color is the sky?"}'
```

6) Frontend UI: http://localhost:5173 (uses the same backend). Enter a question and optionally override the model.
