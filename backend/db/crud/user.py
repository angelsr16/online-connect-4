from bson import ObjectId
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from db.helpers.user import user_helper


async def get_user_by_username(db: AsyncIOMotorDatabase, username: str):
    collection = db["users"]
    user = await collection.find_one({"username": username})
    return user


async def create_user(db: AsyncIOMotorDatabase, user: dict) -> dict:
    collection = db["users"]
    user = await collection.insert_one(user)
    new_user = await collection.find_one({"_id": user.inserted_id})
    return user_helper(new_user)


async def update_user(db: AsyncIOMotorDatabase, user_id: str, update_fields: dict):
    collection = db["users"]

    if not ObjectId.is_valid(user_id):
        return None

    result = await collection.update_one({"_id": ObjectId(user_id)}, update_fields)

    if result.modified_count < 1:
        return None

    return await collection.find_one({"_id": ObjectId(user_id)})
