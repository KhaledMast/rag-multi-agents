from helpers.config import Settings
from motor.motor_asyncio import AsyncIOMotorClient

class BaseDataModel:
    def __init__(self, db_client: AsyncIOMotorClient, settings: Settings):
        self.db_client = db_client
        self.settings = settings
        