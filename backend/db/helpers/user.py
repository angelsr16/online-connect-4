from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

from db.models.pyobjectid import ObjectId
from db.models.user import UserInDB


def user_helper(user: dict) -> dict:
    return {
        "id": str(user["_id"]),
        "username": str(user["username"]),
        "elo_rating": int(user["elo_rating"]),
        "games_played": int(user["games_played"]),
        "wins": int(user["wins"]),
        "losses": int(user["losses"]),
        "draws": int(user["draws"]),
    }


# class UserBase(BaseModel):
#     username: str
#     elo_rating: int = 1200
#     games_played: int = 0
#     wins: int = 0
#     losses: int = 0
#     draws: int = 0


# class UserCreate(UserBase):
#     password: str


# class UserInDB(UserBase):
#     # id: Optional[ObjectId] = Field(default=None, alias="_id")
#     hashed_password: str
#     created_at: datetime = Field(default_factory=datetime.utcnow)
#     last_login: Optional[datetime] = None

#     model_config = {
#         "validate_by_name": True,
#         "arbitrary_types_allowed": True,
#         "json_encoders": {ObjectId: str},
#     }


# class UserPublic(UserBase):
#     id: Optional[ObjectId] = Field(alias="_id")

#     model_config = {
#         "validate_by_name": True,
#         "arbitrary_types_allowed": True,
#         "json_encoders": {ObjectId: str},
#     }
