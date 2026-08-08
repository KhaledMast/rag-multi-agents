from contextlib import asynccontextmanager
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings
from helpers.database import ensure_database_indexes
from routes import base, data, nlp
from stores.llm.LLMProviderFactory import LLMProviderFactory
from stores.vectordb.VectorDBProviderFactory import VectorDBProviderFactory

# Defining the lifecycle (lifespan) to manage the connection
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code executed at startup
    settings = get_settings()

    # MongoDB client
    db_client = AsyncIOMotorClient(settings.MONGODB_URL)
    app.state.mongodb_client = db_client
    app.state.mongodb_database = app.state.mongodb_client[settings.MONGODB_DATABASE]
    # Calling the centralized index configuration
    await ensure_database_indexes(db_client, settings.MONGODB_DATABASE)

    # LLM Factory
    llm_provider_factory = LLMProviderFactory(settings)
    app.state.llm_factory = llm_provider_factory

    # generation
    app.state.generation_client = llm_provider_factory.create(
        provider=settings.GENERATION_BACKEND
    )
    app.state.generation_client.set_generation_model(
        model_id=settings.GENERATION_MODEL_ID
    )

    # embedding
    app.state.embedding_client = llm_provider_factory.create(
        provider=settings.EMBEDDING_BACKEND
    )
    app.state.embedding_client.set_embedding_model(
        model_id=settings.EMBEDDING_MODEL_ID,
        embedding_size=settings.EMBEDDING_MODEL_SIZE
    )

    # VectorDB Factory
    vectordb_provider_factory = VectorDBProviderFactory(settings)
    app.state.vectorDB_factory = vectordb_provider_factory

    # vector db client
    app.state.vectordb_client = vectordb_provider_factory.create(
        provider=settings.VECTOR_DB_BACKEND
    )

    if app.state.vectordb_client is not None:
        app.state.vectordb_client.connect()

    yield # The application is running here
    
    # Code executed at shutdown
    if app.state.mongodb_client is not None:
        app.state.mongodb_client.close() 

    if app.state.vectordb_client is not None:
        app.state.vectordb_client.disconnect()

# Initialisation of FastAPI with the lifespan
app = FastAPI(lifespan=lifespan)

# TODO: Add middleware

# Inclusion of routers
app.include_router(base.base_router)
app.include_router(data.data_router)
app.include_router(nlp.nlp_router)
