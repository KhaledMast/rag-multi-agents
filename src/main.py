from contextlib import asynccontextmanager
from fastapi import FastAPI
from pymongo import AsyncMongoClient
from helpers.config import get_settings
from routes import base, data

# Defining the lifecycle (lifespan) to manage the connection
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code executed at startup
    settings = get_settings()
    app.state.mongodb_client = AsyncMongoClient(settings.MONGODB_URL)
    app.state.mongodb_database = app.state.mongodb_client[settings.MONGODB_DATABASE]
    
    yield # The application is running here
    
    # Code executed at shutdown
    app.state.mongodb_client.close()

# Initialisation of FastAPI with the lifespan
app = FastAPI(lifespan=lifespan)

# Inclusion of routers
app.include_router(base.base_router)
app.include_router(data.data_router)
