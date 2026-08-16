import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app_state import AppState
from helpers.config import get_settings
from helpers.database import ensure_database_indexes
from motor.motor_asyncio import AsyncIOMotorClient
from services.file_storage_service import FileStorageService
from stores.llm.LLMProviderFactory import LLMProviderFactory
from stores.llm.templates.template_parser import TemplateParser
from stores.vectordb.VectorDBProviderFactory import VectorDBProviderFactory

logger = logging.getLogger("uvicorn.error")


class AppLifespan:

    async def build_state(self) -> AppState:
        settings = get_settings()

        storage_service = FileStorageService()

        mongodb_client = AsyncIOMotorClient(settings.MONGODB_URL)
        mongodb_database = mongodb_client[settings.MONGODB_DATABASE]
        await ensure_database_indexes(mongodb_client, settings.MONGODB_DATABASE)

        llm_provider_factory = LLMProviderFactory(settings)

        generation_client = llm_provider_factory.create(provider=settings.GENERATION_BACKEND)
        generation_client.set_generation_model(model_id=settings.GENERATION_MODEL_ID)

        embedding_client = llm_provider_factory.create(provider=settings.EMBEDDING_BACKEND)
        embedding_client.set_embedding_model(
            model_id=settings.EMBEDDING_MODEL_ID,
            embedding_size=settings.EMBEDDING_MODEL_SIZE,
        )

        vectordb_provider_factory = VectorDBProviderFactory(
            storage_service=storage_service,
            settings=settings,
        )
        vectordb_client = vectordb_provider_factory.create(provider=settings.VECTOR_DB_BACKEND)
        if vectordb_client is not None:
            vectordb_client.connect()

        template_parser = TemplateParser()

        return AppState(
            storage_service=storage_service,
            mongodb_client=mongodb_client,
            mongodb_database=mongodb_database,
            generation_client=generation_client,
            embedding_client=embedding_client,
            vectordb_client=vectordb_client,
            template_parser=template_parser,
        )


@asynccontextmanager
async def lifespan(app: FastAPI):
    manager = AppLifespan()

    try:
        app.state.app_state = await manager.build_state()
    except Exception as e:
        logger.error(f"Critical error occurred while starting the application: {e}")
        raise

    yield

    await app.state.app_state.shutdown()
    logger.info("Application shut down cleanly.")
