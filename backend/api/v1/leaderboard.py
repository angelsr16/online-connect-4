from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from motor.motor_asyncio import AsyncIOMotorDatabase

from api.dependencies.db import get_database


router = APIRouter(prefix="/leaderboard")


@router.websocket("/ws/watch")
async def websocket_leaderboard(
    websocket: WebSocket,
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    await websocket.accept()
    collection = db["users"]

    users_cursor = collection.find().sort("elo_rating", -1).limit(10)
    users = []
    async for user in users_cursor:
        users.append(
            {
                "id": str(user["_id"]),
                "username": user["username"],
                "elo_rating": user["elo_rating"],
            }
        )
    await websocket.send_json(users)

    pipeline = [
        {
            "$match": {
                "operationType": {"$in": ["insert", "update", "replace"]},
                "updateDescription.updatedFields.elo_rating": {"$exists": True},
            }
        }
    ]

    change_stream = collection.watch(pipeline, full_document="updateLookup")

    try:
        async for change in change_stream:
            top_users_cursor = collection.find().sort("elo_rating", -1).limit(10)
            users = []
            async for user in top_users_cursor:
                users.append(
                    {
                        "id": str(user["_id"]),
                        "username": user["username"],
                        "elo_rating": user["elo_rating"],
                    }
                )

            await websocket.send_json(users)

    except WebSocketDisconnect:
        print("Leaderboard websocket disconnected.")
    except Exception as e:
        print(f"Error in leaderboard websocket: {e}")
    finally:
        await change_stream.close()
