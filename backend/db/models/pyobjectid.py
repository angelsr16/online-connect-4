from typing import Annotated
from bson import ObjectId as _ObjectId
from pydantic import AfterValidator, GetJsonSchemaHandler
from pydantic_core import core_schema


def check_object_id(value: str) -> str:
    if not _ObjectId.is_valid(value):
        raise ValueError("Invalid ObjectId")
    return value


ObjectId = Annotated[str, AfterValidator(check_object_id)]


# class PyObjectId(ObjectId):
#     @classmethod
#     def __get_pydantic_json_schema__(
#         cls, core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
#     ):
#         return {"type": "string"}

#     @classmethod
#     def __get_pydantic_core_schema__(cls, source_type, handler):
#         return core_schema.no_info_after_validator_function(
#             cls.validate, core_schema.str_schema()
#         )

#     @classmethod
#     def validate(cls, v):
#         if not ObjectId.is_valid(v):
#             raise ValueError("Invalid ObjectId")
#         return ObjectId(v)
