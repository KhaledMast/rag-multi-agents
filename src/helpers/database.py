import logging
from pymongo import IndexModel
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import Request
from models.db_schemes import Project, DataChunk, Asset
from models.enums.DataBaseEnum import DataBaseEnum

logger = logging.getLogger('uvicorn.error')

async def get_db(request: Request) -> AsyncIOMotorClient:
    return request.app.state.mongodb_database

# The global index initialization function
async def ensure_database_indexes(db_client: AsyncIOMotorClient, database_name: str):
    """
    Centrally and efficiently configure all
    MongoDB collections and indexes at server startup.
    """
    db = db_client[database_name]

    try:
        # ---- Index of the PROJECTS collection----
        project_collection = db[DataBaseEnum.COLLECTION_PROJECTS_NAME.value]
        project_indexes = [
            IndexModel(
                idx["key"], 
                name=idx["name"], 
                unique=idx.get("unique", True)
            ) 
            for idx in Project.get_indexes()
        ]
        if project_indexes:
            created = await project_collection.create_indexes(project_indexes)
            logger.info(f"Indexes created for projects: {created}")

        # ---- Index de la collection CHUNKS ----
        chunk_collection = db[DataBaseEnum.COLLECTION_CHUNKS_NAME.value]
        chunk_indexes = [
            IndexModel(
                idx["key"], 
                name=idx["name"], 
                unique=idx.get("unique", False)
            ) 
            for idx in DataChunk.get_indexes()
        ]
        if chunk_indexes:
            created = await chunk_collection.create_indexes(chunk_indexes)
            logger.info(f"Indexes created for chunks: {created}")

        # ---- Index de la collection ASSETS ----
        asset_collection = db[DataBaseEnum.COLLECTION_ASSETS_NAME.value]
        asset_indexes = [
            IndexModel(
                idx["key"], 
                name=idx["name"], 
                unique=idx.get("unique", False)
            )
            for idx in Asset.get_indexes()
        ]
        if asset_indexes:
            created = await asset_collection.create_indexes(asset_indexes)
            logger.info(f"Indexes created for assets: {created}")

        logger.info("MongoDB database successfully initialized!")

    except Exception as e:
        logger.error(f"Error initializing MongoDB indexes: {e}")
        raise e