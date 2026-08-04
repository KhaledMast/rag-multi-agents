from typing import Optional
from pydantic import BaseModel, Field
from helpers.database import PyObjectId 

class DataChunk(BaseModel):
    id: Optional[PyObjectId] = Field(None, alias="_id")
    chunk_text: str = Field(None,description="The text content of the data chunk.")
    chunk_metadata: dict = Field(default_factory=dict, description="metadata associated with the data chunk.")
    chunk_order: int = Field(None, gt=0, description="The order of the chunk in the original document.")
    chunk_project_id: str = Field(None, description="The unique identifier for the project.")


    model_config = {
        "arbitrary_types_allowed": True,
        "populate_by_name": True
    }