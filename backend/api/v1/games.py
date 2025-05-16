from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from api.dependencies.auth import verify_token
from api.dependencies.db import get_database

from services import game as game_service
from db.helpers.user import user_helper

import random

router = APIRouter(prefix="/games")


@router.post("/")
async def register_game(
    db: AsyncIOMotorDatabase = Depends(get_database),
    user: dict = Depends(verify_token),
):
    game_data = await game_service.create_game(db, user["id"])

    return game_data


@router.get("/")
async def get_games(
    db: AsyncIOMotorDatabase = Depends(get_database),
    user: str = Depends(verify_token),
):
    games = await game_service.get_games_by_user(db, user["id"])

    return games


@router.post("/{game_id}")
async def make_movement(
    game_id: str,
    column_index: int,
    db: AsyncIOMotorDatabase = Depends(get_database),
    user: str = Depends(verify_token),
):
    return await game_service.make_movement(db, user["id"], game_id, column_index)


@router.post("/{join_code}")
async def join_game(
    join_code: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
    user: str = Depends(verify_token),
):
    updated_game = await game_service.join_game(db, user, join_code)
    return updated_game
