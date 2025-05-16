import uuid
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from db.helpers.game import game_helper, games_helper
from db.models.game import GameInDB


async def create_game(db: AsyncIOMotorDatabase, game_data):
    collection = db["games"]

    game = await collection.insert_one(game_data)
    new_game = await collection.find_one({"_id": game.inserted_id})

    return game_helper(new_game)


async def get_games_by_user_id(db: AsyncIOMotorDatabase, user_id: str):
    collection = db["games"]

    if not ObjectId.is_valid(user_id):
        return None

    objectid_user_id = ObjectId(user_id)

    games_cursor = collection.find(
        {"$or": [{"player_1": objectid_user_id}, {"player_2": objectid_user_id}]}
    )

    games = await games_cursor.to_list()

    return games_helper(games)


# async def get_game_by_id(db: AsyncIOMotorDatabase, game_id: str, user_id: str):
#     collection = db["games"]

#     if not ObjectId.is_valid(game_id) or not ObjectId.is_valid(user_id):
#         return None

#     game_object_id = ObjectId(game_id)
#     player_object_id = ObjectId(user_id)
#     game = await collection.find_one(
#         {
#             "$and": [
#                 {
#                     "$or": [
#                         {"player_1": player_object_id},
#                         {"player_2": player_object_id},
#                     ],
#                 },
#                 {
#                     "_id": game_object_id,
#                 },
#             ]
#         }
#     )

#     if game is None:
#         return None

#     return game_helper(game)


async def get_game_by_id(db: AsyncIOMotorDatabase, game_id: str):
    if not ObjectId.is_valid(game_id):
        return None

    game = await db["games"].find_one({"_id": ObjectId(game_id)})

    if game is None:
        return None

    return game_helper(game)


async def get_game_by_join_code(db: AsyncIOMotorDatabase, join_code: str):
    collection = db["games"]

    game = await collection.find_one({"join_code": join_code, "status": "waiting"})

    if game is None:
        return None

    return game_helper(game)


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

    updated_game = await collection.find_one({"_id": ObjectId(game_id)})
    return game_helper(updated_game)
