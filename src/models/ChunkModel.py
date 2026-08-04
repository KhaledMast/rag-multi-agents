from typing import List, Tuple
from .BaseDataModel import BaseDataModel
from .db_schemes import DataChunk
from .enums.DataBaseEnum import DataBaseEnum
from pymongo import InsertOne

class ChunkModel(BaseDataModel):

    def __init__(self, db_client: object = None):
        super().__init__(db_client=db_client)
        
        self.db = self.db_client[self.settings.MONGODB_DATABASE]        
        self.collection = self.db[DataBaseEnum.COLLECTION_CHUNKS_NAME.value]


    async def create_chunk(self, chunk: DataChunk) -> DataChunk:
        """
        Create a new data chunk in the database.

        Args:
            chunk (DataChunk): The data chunk to be inserted.

        Returns:
            DataChunk: The newly created data chunk object.
        """
        chunk_data = chunk.model_dump(by_alias=True, exclude_none=True)
        result = await self.collection.insert_one(chunk_data)
        chunk.id = str(result.inserted_id)

        return chunk

    async def get_chunk(self, file_id: str) -> DataChunk:
        """
        Retrieve a data chunk by its file ID.

        Args:
            file_id (str): The ID of the data chunk to retrieve.

        Returns:
            DataChunk: The retrieved data chunk object.
        """
        record = await self.collection.find_one({
            "file_id": file_id
        })

        if record is None:
            return None

        return DataChunk(**record)

    async def insert_many_chunks(self, chunks: List[DataChunk], batch_size: int = 1000) -> int:
        """
        Insert multiple data chunks into the database.

        Args:
            chunks (List[DataChunk]): A list of data chunk objects to be inserted.

        Returns:
            int: The number of data chunk objects that were inserted.
        """
        if chunks is None or len(chunks) == 0:
            return 0
    
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]

            documents = [
                chunk.model_dump(by_alias=True, exclude_none=True)
                for chunk in batch
            ]

            await self.collection.insert_many(documents)

        return len(chunks)

    async def delete_chunks_by_project_id(self, project_id: str) -> int:
        result = await self.collection.delete_many({
            "chunk_project_id": project_id
        })

        return result.deleted_count