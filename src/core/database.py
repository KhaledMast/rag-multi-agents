import logging
from pymongo import IndexModel
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from fastapi import Request
from repositories.db_schemes import Project, DataChunk, Asset
from repositories.enums.DataBaseEnum import DataBaseEnum


logger = logging.getLogger('uvicorn.error')

# The global index initialization function
async def ensure_database_indexes(db_client: AsyncIOMotorClient, database_name: str):
    """
    Centrally and efficiently configure all
    MongoDB collections and indexes at server startup.
    """
    db = db_client[database_name]

    collections_config = [
        (DataBaseEnum.COLLECTION_PROJECTS_NAME.value, Project, True),
        (DataBaseEnum.COLLECTION_CHUNKS_NAME.value, DataChunk, False),
        (DataBaseEnum.COLLECTION_ASSETS_NAME.value, Asset, False),
    ]

    try:
        for collection_name, model_cls, default_unique in collections_config:
            collection = db[collection_name]
            indexes = [
                IndexModel(
                    idx["key"],
                    name=idx["name"],
                    unique=idx.get("unique", default_unique),
                )
                for idx in model_cls.get_indexes()
            ]
            if indexes:
                created = await collection.create_indexes(indexes)
                logger.info(f"Indexes created for {collection_name}: {created}")

        logger.info("MongoDB database successfully initialized!")

    except Exception as e:
        logger.error(f"Error initializing MongoDB indexes: {e}")
        raise