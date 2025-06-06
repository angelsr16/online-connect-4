import random
import uuid
from bson import ObjectId
from fastapi import HTTPException, WebSocket, WebSocketDisconnect, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from db.crud import game as crud_game, user as crud_user
from db.helpers.game import game_helper
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

    populated_game_data = await populate_players(db, new_game_data)

    return game_helper(populated_game_data)


async def get_games_by_user(db: AsyncIOMotorDatabase, player_id: str):
    games_list = await crud_game.get_games_by_user_id(db, player_id)

    games = []
    for game in games_list:
        games.append(game_helper(await populate_players(db, game)))

    return games


async def join_game(db: AsyncIOMotorDatabase, user, join_code: str):
    game = await crud_game.get_game_by_join_code(db, join_code=join_code)

    if game is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Game not found"
        )

    populated_game = await populate_players(db, game)

    if populated_game["player_1"]["id"] == user["id"] or (
        populated_game["player_2"] is not None
        and populated_game["player_2"]["id"] == user["id"]
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You can't join your own game"
        )

    if populated_game["status"] != "waiting" or populated_game["player_2"] is not None:
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
        objectid_user_id if random_number > 0.5 else populated_game["player_1"]["id"]
    )

    updated_game = await crud_game.update_game(
        db, str(populated_game["_id"]), update_fields
    )

    if updated_game == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Couldn't join the game"
        )

    populated_game = await populate_players(db, updated_game)
    return game_helper(populated_game)


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

    populated_game_data = await populate_players(db, game_data)

    if populated_game_data["status"] != "active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="The game isn't active"
        )

    current_turn = str(populated_game_data["current_turn"])
    player_1 = populated_game_data["player_1"]
    player_2 = (
        populated_game_data["player_2"]
        if populated_game_data["player_2"] is not None
        else None
    )

    if player_1["id"] != player_id and player_2["id"] != player_id:
        raise HTTPException(status_code=403, detail="You're not part of this game")

    if current_turn != player_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not your turn"
        )

    row_position = 0
    disk_was_placed = False
    for row in reversed(range(len(populated_game_data["game_state"]))):
        cell = populated_game_data["game_state"][row][column_index]
        if cell == 0:
            populated_game_data["game_state"][row][column_index] = (
                1 if current_turn == player_1["id"] else 2
            )
            row_position = row
            disk_was_placed = True

            game_status = check_game_status(
                populated_game_data["game_state"],
                1 if current_turn == player_1["id"] else 2,
            )

            if game_status == None:
                current_turn = (
                    player_2["id"] if current_turn == player_1["id"] else player_1["id"]
                )

            break

    if disk_was_placed:
        update_fields = {
            "game_state": populated_game_data["game_state"],
            "current_turn": ObjectId(current_turn),
        }

        if game_status != None:
            current_player = player_1 if player_1["id"] == player_id else player_2
            another_player = player_2 if player_1["id"] == player_id else player_1

            await end_game(
                db, game_status, update_fields, current_player, another_player
            )

        push_fields = {
            "moves": {
                "player": str(player_id),
                "column": column_index,
                "row": row_position,
            }
        }

        updated_game = await crud_game.update_game(
            db, game_id, update_fields, push_fields
        )

        if updated_game == None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="There has been an error"
            )

        populated_updated_game = await populate_players(db, updated_game)

        return game_helper(populated_updated_game)

    return None


async def populate_players(db: AsyncIOMotorDatabase, game):
    users_collection = db["users"]

    player_1 = await users_collection.find_one({"_id": game["player_1"]})
    player_2 = await users_collection.find_one({"_id": game["player_2"]})

    game["player_1"] = (
        {
            "id": str(player_1["_id"]),
            "username": player_1["username"],
            "elo_rating": player_1["elo_rating"],
        }
        if player_1
        else None
    )

    game["player_2"] = (
        {
            "id": str(player_2["_id"]),
            "username": player_2["username"],
            "elo_rating": player_2["elo_rating"],
        }
        if player_2
        else None
    )

    return game


def check_game_status(game_grid, player):
    rows = len(game_grid)
    cols = len(game_grid[0])

    # Horizontal
    for row in range(rows):
        for col in range(cols - 3):
            if all(game_grid[row][col + i] == player for i in range(4)):
                return "win"

    # Vertical
    for row in range(rows - 3):
        for col in range(cols):
            if all(game_grid[row + i][col] == player for i in range(4)):
                return "win"

    # Diagonal (\)
    for row in range(rows - 3):
        for col in range(cols - 3):
            if all(game_grid[row + i][col + i] == player for i in range(4)):
                return "win"

    # Diagonal (/)
    for row in range(rows - 3):
        for col in range(3, cols):
            if all(game_grid[row + i][col - i] == player for i in range(4)):
                return "win"

    # Check for draw (no empty spaces, i.e., no 0s)
    if all(cell != 0 for row in game_grid for cell in row):
        return "draw"

    return None


async def end_game(
    db: AsyncIOMotorDatabase, game_status, update_fields, current_player, another_player
):
    if game_status == "draw" or game_status == "win":
        update_fields["status"] = "game_over"

    if game_status == "win":
        update_fields["winner"] = current_player["id"]

        new_elo_rating_1, new_elo_rating_2 = calculate_elo(
            current_player["elo_rating"], another_player["elo_rating"], 1
        )

        await crud_user.update_user(
            db,
            current_player["id"],
            {
                "$inc": {"wins": 1},
                "$set": {"elo_rating": new_elo_rating_1},
            },
        )
        await crud_user.update_user(
            db,
            another_player["id"],
            {
                "$inc": {"losses": 1},
                "$set": {"elo_rating": new_elo_rating_2},
            },
        )

    if game_status == "draw":
        update_fields["status"] = "game_over"

        new_elo_rating_1, new_elo_rating_2 = calculate_elo(
            current_player["elo_rating"], another_player["elo_rating"], 0.5
        )

        await crud_user.update_user(
            db,
            current_player["id"],
            {
                "$inc": {"draws": 1},
                "$set": {"elo_rating": new_elo_rating_1},
            },
        )
        await crud_user.update_user(
            db,
            another_player["id"],
            {
                "$inc": {"draws": 1},
                "$set": {"elo_rating": new_elo_rating_2},
            },
        )


def calculate_elo(rating1, rating2, score1, k=32):
    expected1 = 1 / (1 + 10 ** ((rating2 - rating1) / 400))
    expected2 = 1 - expected1
    score2 = 1 - score1

    # New Ratings
    new_rating1 = rating1 + k * (score1 - expected1)
    new_rating2 = rating2 + k * (score2 - expected2)

    return round(new_rating1, 2), round(new_rating2, 2)
