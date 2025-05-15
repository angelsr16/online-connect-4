from motor.motor_asyncio import AsyncIOMotorDatabase
from db.database import client


def get_database() -> AsyncIOMotorDatabase:
    return client["connect_4"]
