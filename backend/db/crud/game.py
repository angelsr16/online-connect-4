import uuid
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from db.helpers.game import game_helper, games_helper
from db.models.game import GameInDB


async def create_game(db: AsyncIOMotorDatabase, player_id: str):
    collection = db["games"]

    initial_game_state = [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
    ]

    join_code = str(uuid.uuid4())[:6]

    if not ObjectId.is_valid(player_id):
        return None

    player_object_id = ObjectId(player_id)

    game = GameInDB(
        player_1=player_object_id,
        current_turn=None,
        player_2=None,
        game_state=initial_game_state,
        join_code=join_code,
    )

    game_data = game.model_dump(by_alias=True, exclude={"id"})

    game_data["player_1"] = ObjectId(game_data["player_1"])
    if game_data.get("player_2"):
        game_data["player_2"] = ObjectId(game_data["player_2"])

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


async def get_game_by_id(db: AsyncIOMotorDatabase, game_id: str, player_id: str):
    collection = db["games"]

    if not ObjectId.is_valid(game_id) or not ObjectId.is_valid(player_id):
        return None

    game_object_id = ObjectId(game_id)
    player_object_id = ObjectId(player_id)
    game = await collection.find_one(
        {
            "$and": [
                {
                    "$or": [
                        {"player_1": player_object_id},
                        {"player_2": player_object_id},
                    ],
                },
                {
                    "_id": game_object_id,
                },
            ]
        }
    )

    if game is None:
        return None

    return game_helper(game)


async def get_game_by_join_code(db: AsyncIOMotorDatabase, join_code: str):
    collection = db["games"]

    game = await collection.find_one({"join_code": join_code})

    if game is None:
        return None

    return game_helper(game)


async def update_game(db: AsyncIOMotorDatabase, game_id: str, update_fields: dict):
    collection = db["games"]

    if not ObjectId.is_valid(game_id):
        return None

    result = await collection.update_one(
        {"_id": ObjectId(game_id)}, {"$set": update_fields}
    )

    if result.modified_count < 1:
        return None

    updated_game = await collection.find_one({"_id": ObjectId(game_id)})
    return game_helper(updated_game)
