from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from motor.motor_asyncio import AsyncIOMotorDatabase

from api.dependencies.auth import verify_token, verify_token_from_websocket
from api.dependencies.db import get_database
from bson import ObjectId, json_util

from db.helpers.user import user_helper

router = APIRouter(prefix="/users")


@router.websocket("/ws/watch")
async def websocket_watch_user_info(websocket: WebSocket):
    await websocket.accept()

    db = get_database()
    user = await verify_token_from_websocket(websocket, db)

    if user is None:
        return

    collection = db["users"]
    await websocket.send_text(json_util.dumps(user))

    user_objectid = ObjectId(user["id"])
    pipeline = [{"$match": {"fullDocument._id": user_objectid}}]

    async with collection.watch(pipeline, full_document="updateLookup") as stream:
        try:
            async for change in stream:
                user_data = change["fullDocument"]
                await websocket.send_text(json_util.dumps(user_helper(user_data)))
        except WebSocketDisconnect:
            print("Client disconnected")
        except Exception as e:
            print(f"Error: {e}")
