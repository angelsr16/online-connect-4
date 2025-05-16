from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from api.dependencies.auth import verify_token
from api.dependencies.db import get_database

from db.crud import user as crud_user, game as crud_game
from db.helpers.user import user_helper

import random

router = APIRouter(prefix="/games")


@router.post("/")
async def register_game(
    db: AsyncIOMotorDatabase = Depends(get_database),
    username: str = Depends(verify_token),
):
    user = await crud_user.get_user_by_username(db, username)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    user_data = user_helper(user)

    game_data = await crud_game.create_game(db, user_data["id"])

    if game_data is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="There has been an error while creating a game, try again.",
        )

    return {"game": game_data}


@router.get("/")
async def get_games(
    db: AsyncIOMotorDatabase = Depends(get_database),
    username: str = Depends(verify_token),
):
    user = await crud_user.get_user_by_username(db, username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    user_data = user_helper(user)

    games = await crud_game.get_games_by_user_id(db, user_data["id"])

    return {"games": games}


@router.post("/{game_id}")
async def make_movement(
    game_id: str,
    column_index: int,
    db: AsyncIOMotorDatabase = Depends(get_database),
    username: str = Depends(verify_token),
):
    user = await crud_user.get_user_by_username(db, username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    user_data = user_helper(user)

    game_data = await crud_game.get_game_by_id(
        db, game_id=game_id, player_id=user_data["id"]
    )

    if game_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found in your games list",
        )

    if game_data["status"] != "active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="The game isn't active"
        )

    current_turn = 1

    disk_was_placed = False
    for row in reversed(range(len(game_data["game_state"]))):
        cell = game_data["game_state"][row][column_index]
        if cell == 0:
            game_data["game_state"][row][column_index] = current_turn
            disk_was_placed = True
            current_turn = 2 if current_turn == 1 else 1
            break

    if disk_was_placed:
        print("Disk placed")

    return {"game": game_data}


@router.post("/{join_code}")
async def join_game(
    join_code: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
    username: str = Depends(verify_token),
):
    user = await crud_user.get_user_by_username(db, username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    user_data = user_helper(user)

    game = await crud_game.get_game_by_join_code(db, join_code=join_code)

    if game is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Game not found"
        )

    if game["player_1"] == user_data["id"] or game["player_2"] == user_data["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You can't join your own game"
        )

    if game["status"] != "waiting" or game["player_2"] is not None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You can't join this game"
        )

    if not ObjectId.is_valid(user_data["id"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You couldn't join this game",
        )

    objectid_user_id = ObjectId(user_data["id"])
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
