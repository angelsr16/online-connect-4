from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from api.dependencies.db import get_database
from db.schemas.user import UserCreate


async def get_user_by_username(db: AsyncIOMotorDatabase, username: str):
    print(db)
    collection = db["users"]
    user = await collection.find_one({"username": username})
    return user


async def create_user(db: AsyncIOMotorDatabase, user: dict):
    collection = db["users"]
    await collection.insert_one(user)
