from bson import ObjectId
from typing import Annotated
from pydantic import Field, BeforeValidator, PlainSerializer

PyObjectId = Annotated[
    ObjectId,
    BeforeValidator(lambda v: ObjectId(v) if ObjectId.is_valid(v) else v),
    PlainSerializer(lambda x: str(x), return_type=str, when_used="json"),
    Field(json_schema_extra={"type": "string", "example": "60d5ecf8b425ec3a20e54124"})
]
