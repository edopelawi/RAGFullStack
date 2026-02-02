from typing import Any, Dict, List, Optional

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field

from .clients import MissingAPIKeyError, embed_texts, get_chroma_client, get_openai_client
from .config import Settings, get_settings

app = FastAPI(title="RAG Full Stack", version="0.1.0")


class DocumentInput(BaseModel):
    id: str = Field(..., description="Unique document identifier")
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class IngestRequest(BaseModel):
    collection: str | None = Field(default=None, description="Target collection name")
    documents: List[DocumentInput]


class QueryRequest(BaseModel):
    question: str
    top_k: int = Field(default=4, ge=1, le=20)
    model: Optional[str] = Field(default=None, description="Override the generation model")


class RetrievedContext(BaseModel):
    id: str
    content: str
    metadata: Dict[str, Any]
    score: Optional[float] = None


class QueryResponse(BaseModel):
    answer: str
    contexts: List[RetrievedContext]


@app.get("/healthz")
def healthcheck() -> Dict[str, str]:
    return {"status": "ok"}


@app.get("/readyz")
def readycheck(settings: Settings = Depends(get_settings)) -> Dict[str, str]:
    client = get_chroma_client(settings)
    try:
        client.heartbeat()
    except Exception as exc:  # pragma: no cover - best-effort readiness
        raise HTTPException(status_code=503, detail=f"Chroma not reachable: {exc}")
    return {"status": "ready"}


@app.post("/ingest")
def ingest(request: IngestRequest, settings: Settings = Depends(get_settings)) -> Dict[str, int]:
    chroma = get_chroma_client(settings)
    collection_name = request.collection or settings.chroma_collection
    collection = chroma.get_or_create_collection(name=collection_name)

    try:
        openai_client = get_openai_client(settings)
    except MissingAPIKeyError as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    contents = [doc.content for doc in request.documents]
    ids = [doc.id for doc in request.documents]
    metadatas = [doc.metadata for doc in request.documents]

    embeddings = embed_texts(openai_client, contents, settings.openai_embedding_model)
    collection.add(ids=ids, documents=contents, metadatas=metadatas, embeddings=embeddings)

    return {"ingested": len(ids)}


def _format_context_block(contexts: List[RetrievedContext]) -> str:
    lines = []
    for idx, ctx in enumerate(contexts, start=1):
        meta = ", ".join(f"{k}={v}" for k, v in ctx.metadata.items()) if ctx.metadata else ""
        header = f"[{idx}] (id={ctx.id}{', ' + meta if meta else ''})"
        lines.append(f"{header}\n{ctx.content}")
    return "\n\n".join(lines)


def _generate_answer(question: str, contexts: List[RetrievedContext], model: str, settings: Settings) -> str:
    try:
        openai_client = get_openai_client(settings)
    except MissingAPIKeyError as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    context_block = _format_context_block(contexts)
    system_prompt = (
        "You are a concise assistant. Use the provided context. "
        "If the answer is not in the context, say you don't know."
    )
    user_prompt = (
        f"Context:\n{context_block or 'No context'}\n\n"
        f"Question: {question}\n"
        "Answer with citations like [1], [2] tied to the context order."
    )

    completion = openai_client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    return completion.choices[0].message.content or ""


@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest, settings: Settings = Depends(get_settings)) -> QueryResponse:
    chroma = get_chroma_client(settings)
    collection = chroma.get_or_create_collection(name=settings.chroma_collection)

    try:
        openai_client = get_openai_client(settings)
    except MissingAPIKeyError as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    query_embedding = embed_texts(openai_client, [request.question], settings.openai_embedding_model)[0]
    results = collection.query(query_embeddings=[query_embedding], n_results=request.top_k)

    raw_docs = results.get("documents", [[]])[0]
    raw_metas = results.get("metadatas", [[]])[0]
    raw_ids = results.get("ids", [[]])[0]
    raw_distances = results.get("distances", [[]])[0]

    contexts: List[RetrievedContext] = []
    for doc_id, doc, meta, dist in zip(raw_ids, raw_docs, raw_metas, raw_distances):
        contexts.append(
            RetrievedContext(
                id=str(doc_id),
                content=doc,
                metadata=meta or {},
                score=float(dist) if dist is not None else None,
            )
        )

    generation_model = request.model or settings.openai_model
    answer = _generate_answer(request.question, contexts, generation_model, settings)

    return QueryResponse(answer=answer, contexts=contexts)
