from typing import Iterable, List

import chromadb
from chromadb.api.types import Embedding
from openai import OpenAI

from .config import Settings


class MissingAPIKeyError(RuntimeError):
    pass


def get_chroma_client(settings: Settings):
    return chromadb.HttpClient(host=settings.chroma_host, port=settings.chroma_port)


def get_openai_client(settings: Settings) -> OpenAI:
    if not settings.openai_api_key:
        raise MissingAPIKeyError("OPENAI_API_KEY is not configured")
    return OpenAI(api_key=settings.openai_api_key)


def embed_texts(client: OpenAI, texts: Iterable[str], model: str) -> List[Embedding]:
    response = client.embeddings.create(model=model, input=list(texts))
    return [item.embedding for item in response.data]
