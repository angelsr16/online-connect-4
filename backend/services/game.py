import random
import uuid
from bson import ObjectId
from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from db.crud import game as crud_game
from db.models.game import GameInDB


async def create_game(db: AsyncIOMotorDatabase, player_id: str) -> dict:
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

    new_game_data = await crud_game.create_game(db, game_data=game_data)
    if new_game_data is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="There has been an error while creating a game, try again.",
        )
    return new_game_data


async def get_games_by_user(db: AsyncIOMotorDatabase, player_id: str):
    return await crud_game.get_games_by_user_id(db, player_id)


async def join_game(db: AsyncIOMotorDatabase, user, join_code: str):
    game = await crud_game.get_game_by_join_code(db, join_code=join_code)

    if game is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Game not found"
        )

    if game["player_1"] == user["id"] or game["player_2"] == user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You can't join your own game"
        )

    if game["status"] != "waiting" or game["player_2"] is not None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You can't join this game"
        )

    if not ObjectId.is_valid(user["id"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You couldn't join this game",
        )

    objectid_user_id = ObjectId(user["id"])
    update_fields = {
        "player_2": objectid_user_id,
        "status": "active",
    }

    random_number = random.random()

    update_fields["current_turn"] = (
        objectid_user_id if random_number > 0.5 else game["player_1"]
    )

    updated_game = await crud_game.update_game(db, game["id"], update_fields)

    if updated_game == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Couldn't join the game"
        )

    return updated_game


async def make_movement(
    db: AsyncIOMotorDatabase, player_id: str, game_id: str, column_index: int
):
    if column_index >= 7 or column_index < 0:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid movement"
        )

    game_data = await crud_game.get_game_by_id(db, game_id=game_id)

    if not game_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found in your games list",
        )

    if game_data["status"] != "active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="The game isn't active"
        )

    if game_data["player_1"] != player_id and game_data.get("player_2") != player_id:
        raise HTTPException(status_code=403, detail="You're not part of this game")

    if game_data["current_turn"] != player_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not your turn"
        )

    current_turn = game_data["current_turn"]
    player_1 = game_data["player_1"]
    player_2 = game_data["player_2"]
    column_movement = 0
    row_movement = 0

    disk_was_placed = False
    for row in reversed(range(len(game_data["game_state"]))):
        cell = game_data["game_state"][row][column_index]
        if cell == 0:
            game_data["game_state"][row][column_index] = (
                1 if current_turn == player_1 else 2
            )
            column_movement = column_index
            row_movement = row
            disk_was_placed = True
            current_turn = player_2 if current_turn == player_1 else player_1
            break

    if disk_was_placed:
        update_fields = {
            "game_state": game_data["game_state"],
            "current_turn": current_turn,
        }

        push_fields = {
            "moves": {
                "player": str(player_id),
                "column": column_movement,
                "row": row_movement,
            }
        }

        updated_game = await crud_game.update_game(
            db, game_id, update_fields, push_fields
        )

        if updated_game == None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Couldn't join the game"
            )

        return updated_game

    return None
