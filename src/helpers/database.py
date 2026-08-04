from typing import Annotated
from bson import ObjectId
from pydantic import Field, BeforeValidator

PyObjectId = Annotated[
    ObjectId, 
    BeforeValidator(lambda v: ObjectId(v) if ObjectId.is_valid(v) else v),
    Field(json_schema_extra={"type": "string", "example": "60d5ecf8b425ec3a20e54124"})
]
