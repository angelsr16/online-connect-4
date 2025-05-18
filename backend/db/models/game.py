from datetime import datetime
from typing import List, Optional
from bson import ObjectId
from pydantic import BaseModel, Field

from db.models.pyobjectid import PyObjectId


class GameBase(BaseModel):
    player_1: PyObjectId
    current_turn: Optional[PyObjectId]
    player_2: Optional[PyObjectId]
    game_state: List[List[int]]
    status: str = "waiting"
    moves: List[dict] = []


class GameInDB(GameBase):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    join_code: str

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {
            ObjectId: str,
            datetime: lambda v: v.replace(microsecond=0).isoformat() + "Z",
        },
    }


class MoveRequest(BaseModel):
    column_index: int
