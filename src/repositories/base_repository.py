from helpers.config import Settings
from motor.motor_asyncio import AsyncIOMotorClient

class BaseRepository:
    def __init__(self, db_client: AsyncIOMotorClient, settings: Settings):
        self.db_client = db_client
        self.settings = settings
        