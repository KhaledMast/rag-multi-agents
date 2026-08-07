from contextlib import asynccontextmanager
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings
from helpers.database import ensure_database_indexes
from routes import base, data
from stores.llm.LLMProviderFactory import LLMProviderFactory

# Defining the lifecycle (lifespan) to manage the connection
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code executed at startup
    settings = get_settings()
    db_client = AsyncIOMotorClient(settings.MONGODB_URL)
    app.state.mongodb_client = db_client
    app.state.mongodb_database = app.state.mongodb_client[settings.MONGODB_DATABASE]

    # Calling the centralized index configuration
    await ensure_database_indexes(db_client, settings.MONGODB_DATABASE)

    # LLM Factory
    app.state.llm_factory = LLMProviderFactory(settings)

    yield # The application is running here
    
    # Code executed at shutdown
    if app.state.mongodb_client is not None:
        app.state.mongodb_client.close() 

# Initialisation of FastAPI with the lifespan
app = FastAPI(lifespan=lifespan)

# TODO: Add middleware

# Inclusion of routers
app.include_router(base.base_router)
app.include_router(data.data_router)
