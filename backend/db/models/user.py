from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

from db.models.pyobjectid import ObjectId


class UserModel(BaseModel):
    id: Optional[ObjectId] = Field(alias="_id")
    username: str
    hashed_password: str
    elo_rating: int = 1200
    games_played: int = 0
    wins: int = 0
    losses: int = 0
    draws: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str},
    }
