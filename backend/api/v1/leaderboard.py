from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from api.dependencies.db import get_database


router = APIRouter(prefix="/leaderboard")


@router.get("/")
async def get_leaderboard(db: AsyncIOMotorDatabase = Depends(get_database)):
    collection = db["users"]

    users_cursor = collection.find().sort("elo_rating", -1).limit(10)
    users = []
    async for user in users_cursor:
        users.append(
            {
                "id": str(user["_id"]),
                "username": user["username"],
                "elo_rating": user["elo_rating"],
            }
        )
    return users
