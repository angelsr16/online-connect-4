from bson import ObjectId
from fastapi import (
    APIRouter,
    Depends,
    WebSocket,
    WebSocketDisconnect,
)
from motor.motor_asyncio import AsyncIOMotorDatabase

from api.dependencies.auth import verify_token
from api.dependencies.db import get_database

from db.helpers.game import game_helper
from db.models.game import MoveRequest
from services import game as game_service
from bson import json_util

router = APIRouter(prefix="/games")


@router.post("/register")
async def register_game(
    db: AsyncIOMotorDatabase = Depends(get_database),
    user: dict = Depends(verify_token),
):
    game_data = await game_service.create_game(db, user["id"])

    return game_data


@router.get("/")
async def get_games(
    db: AsyncIOMotorDatabase = Depends(get_database),
    user: dict = Depends(verify_token),
):
    games = await game_service.get_games_by_user(db, user["id"])

    return games


@router.post("/join/{join_code}")
async def join_game(
    join_code: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
    user: dict = Depends(verify_token),
):
    updated_game = await game_service.join_game(db, user, join_code)
    return updated_game


@router.post("/{game_id}/move")
async def make_movement(
    game_id: str,
    move: MoveRequest,
    db: AsyncIOMotorDatabase = Depends(get_database),
    user: dict = Depends(verify_token),
):
    return await game_service.make_movement(db, user["id"], game_id, move.column_index)


@router.websocket("/ws/watch/{game_id}")
async def websocket_watch_game(
    websocket: WebSocket, game_id: str, db: AsyncIOMotorDatabase = Depends(get_database)
):
    await websocket.accept()

    collection = db["games"]
    if not ObjectId.is_valid(game_id):
        await websocket.close(code=4004, reason="Game not found")
        return

    game_objectid = ObjectId(game_id)

    game_data = await collection.find_one({"_id": game_objectid})
    populated_game = await game_service.populate_players(db, game_data)
    await websocket.send_text(json_util.dumps(game_helper(populated_game)))

    # Create change stream on the collection, filtering by _id
    pipeline = [{"$match": {"fullDocument._id": game_objectid}}]

    async with collection.watch(pipeline, full_document="updateLookup") as stream:
        try:
            async for change in stream:
                game_data = change["fullDocument"]
                populated_game = await game_service.populate_players(db, game_data)

                await websocket.send_text(json_util.dumps(game_helper(populated_game)))
        except WebSocketDisconnect:
            print("Client disconnected")
        except Exception as e:
            print(f"Error: {e}")
