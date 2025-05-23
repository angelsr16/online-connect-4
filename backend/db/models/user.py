from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field
from datetime import datetime

from db.models.pyobjectid import PyObjectId


class UserBase(BaseModel):
    username: str
    elo_rating: float = 1200
    games_played: int = 0
    wins: int = 0
    losses: int = 0
    draws: int = 0


class UserCreate(UserBase):
    password: str


class UserInDB(UserBase):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {
            ObjectId: str,
            datetime: lambda v: v.replace(microsecond=0).isoformat() + "Z",
        },
    }
