import uuid
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase


async def create_game(db: AsyncIOMotorDatabase, game_data):
    collection = db["games"]

    game = await collection.insert_one(game_data)
    return await collection.find_one({"_id": game.inserted_id})


async def get_games_by_user_id(db: AsyncIOMotorDatabase, user_id: str):
    collection = db["games"]

    if not ObjectId.is_valid(user_id):
        return None

    objectid_user_id = ObjectId(user_id)

    games_cursor = collection.find(
        {"$or": [{"player_1": objectid_user_id}, {"player_2": objectid_user_id}]}
    )

    return await games_cursor.to_list()


async def get_game_by_id(db: AsyncIOMotorDatabase, game_id: str):
    if not ObjectId.is_valid(game_id):
        return None

    return await db["games"].find_one({"_id": ObjectId(game_id)})


async def get_game_by_join_code(db: AsyncIOMotorDatabase, join_code: str):
    collection = db["games"]

    game = await collection.find_one({"join_code": join_code, "status": "waiting"})

    if game is None:
        return None

    return game


async def update_game(
    db: AsyncIOMotorDatabase,
    game_id: str,
    update_fields: dict,
    push_fields: dict = None,
):
    collection = db["games"]

    if not ObjectId.is_valid(game_id):
        return None

    update_query = {"$set": update_fields}
    if push_fields:
        update_query["$push"] = push_fields

    result = await collection.update_one({"_id": ObjectId(game_id)}, update_query)

    if result.modified_count < 1:
        return None

    return await collection.find_one({"_id": ObjectId(game_id)})
