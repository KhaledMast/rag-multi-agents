from helpers.config import get_settings
from motor.motor_asyncio import AsyncIOMotorClient

class BaseDataModel:
    def __init__(self, db_client: AsyncIOMotorClient):
        self.settings = get_settings()
        self.db_client = db_client