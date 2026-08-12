from stores.vectordb.providers import QdrantDBProvider
from stores.llm.LLMInterface import LLMInterface
from fastapi import Request

# Qdrant
def get_vectordb_client(request: Request) -> QdrantDBProvider:
    return request.app.state.vectordb_client

def get_generation_client(request: Request) -> LLMInterface:
    return request.app.state.generation_client

def get_embedding_client(request: Request) -> LLMInterface:
    return request.app.state.embedding_client
