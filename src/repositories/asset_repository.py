from .base_repository import BaseRepository
from helpers.config import Settings
from .db_schemes import Asset
from .enums.DataBaseEnum import DataBaseEnum
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import DuplicateKeyError

class AssetRepository(BaseRepository):

    def __init__(self, db_client: AsyncIOMotorClient, settings: Settings):
        super().__init__(db_client=db_client, settings=settings)
                
        # self.collection = self.db_client[DataBaseEnum.COLLECTION_ASSETS_NAME.value]

        self.db = self.db_client[self.settings.MONGODB_DATABASE]
        self.collection = self.db[DataBaseEnum.COLLECTION_ASSETS_NAME.value]

    async def create_asset(self, asset: Asset):

        try:
            asset_data = asset.model_dump(by_alias=True, exclude_none=True)
                    
            result = await self.collection.insert_one(asset_data)
            asset.id = result.inserted_id  
    
            return asset
        
        except DuplicateKeyError:
            raise ValueError(f"Asset with id {asset.asset_project_id} already exists")


    async def get_all_project_assets(self, asset_project_id: str, asset_type: str):

        records = await self.collection.find({
            "asset_project_id": asset_project_id,
            "asset_type": asset_type,
        }).to_list(length=None)

        return [
            Asset(**record)
            for record in records
        ]

    async def get_asset_record(self, asset_project_id: str, asset_name: str):

        record = await self.collection.find_one({
            "asset_project_id": asset_project_id,
            "asset_name": asset_name
        })

        if record:
            return Asset(**record)

        return None