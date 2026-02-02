# RAG Full Stack

This project is my playground to learn about the recent AI Engineering - how to create, deploy, and maintain an RAG application in production.

This project is [MIT-licensed.](LICENSE)

This is the way.

## Prereqs

- Docker (Desktop on macOS/Windows, Engine on Linux) with Compose v2. Recommended: Docker Desktop 4.30+ or Compose v2.20+.
- Node 20+ (if you run the frontend without Docker).
- Python 3.11+ (if you run the backend without Docker).

Check versions:

```
docker --version
docker compose version
docker-compose version
```

- macOS (Homebrew docker-compose standalone): use `docker-compose up --build` instead of `docker compose up --build`. If you prefer the plugin form, run:

```
mkdir -p ~/.docker/cli-plugins
ln -s $(which docker-compose) ~/.docker/cli-plugins/docker-compose
docker compose version
```
Then `docker compose` works too.

- macOS with Colima: start the daemon before compose: `colima start` (and `docker context use colima` if needed). Check with `docker info`. Stop with `colima stop`.

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
or
```
docker-compose up --build
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
