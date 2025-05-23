from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from api.v1 import auth, games, leaderboard, users

from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.include_router(auth.router)
app.include_router(games.router)
app.include_router(leaderboard.router)
app.include_router(users.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"msg": "Hello from the server"}
