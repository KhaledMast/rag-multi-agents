import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings
from helpers.database import ensure_database_indexes
from stores.llm.LLMProviderFactory import LLMProviderFactory
from stores.vectordb.VectorDBProviderFactory import VectorDBProviderFactory
from stores.llm.templates.template_parser import TemplateParser
from services.file_storage_service import FileStorageService 

logger = logging.getLogger('uvicorn.error')

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code executed at startup
    settings = get_settings()
    storage_service = FileStorageService()

    # MongoDB client & DB
    db_client = AsyncIOMotorClient(settings.MONGODB_URL)
    app.state.mongodb_client = db_client
    app.state.mongodb_database = db_client[settings.MONGODB_DATABASE]
    await ensure_database_indexes(db_client, settings.MONGODB_DATABASE)

    # LLM Factory & Clients
    llm_provider_factory = LLMProviderFactory(settings)
    app.state.llm_factory = llm_provider_factory

    app.state.generation_client = llm_provider_factory.create(provider=settings.GENERATION_BACKEND)
    app.state.generation_client.set_generation_model(model_id=settings.GENERATION_MODEL_ID)

    app.state.embedding_client = llm_provider_factory.create(provider=settings.EMBEDDING_BACKEND)
    app.state.embedding_client.set_embedding_model(
        model_id=settings.EMBEDDING_MODEL_ID,
        embedding_size=settings.EMBEDDING_MODEL_SIZE
    )

    # VectorDB Factory & Client
    vectordb_provider_factory = VectorDBProviderFactory(storage_service=storage_service,settings=settings)
    app.state.vectorDB_factory = vectordb_provider_factory
    app.state.vectordb_client = vectordb_provider_factory.create(provider=settings.VECTOR_DB_BACKEND)

    if app.state.vectordb_client is not None:
        app.state.vectordb_client.connect()

    app.state.template_parser = TemplateParser() 

    yield 
    
    # Code executed at shutdown
    if getattr(app.state, "mongodb_client", None) is not None:
        app.state.mongodb_client.close() 

    if getattr(app.state, "vectordb_client", None) is not None:
        app.state.vectordb_client.disconnect()
    
    logger.info("Application shut down cleanly.")
