from typing import Optional
from pydantic import BaseModel, Field, field_validator
from helpers.fields import PyObjectId


class Project(BaseModel):
    id: Optional[PyObjectId] = Field(None, alias="_id")
    project_id: str = Field(min_length=1, description="The unique identifier for the project.")

    @field_validator('project_id')
    def validate_project_id(cls, v: str) -> str:
        if not v.isalnum():
            raise ValueError('project_id must contain only alphanumeric characters')
        return v

    model_config = {
        "arbitrary_types_allowed": True,
        "populate_by_name": True,
    }

    @classmethod
    def get_indexes(cls):

        return [
            {
                "key": [
                    ("project_id", 1)
                ],
                "name": "project_id_index_1",
                "unique": True
            }
        ]