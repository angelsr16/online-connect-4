from pymongo.mongo_client import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from core.config import MONGO_URL

import os

MONGO_DETAILS = MONGO_URL
client = AsyncIOMotorClient(MONGO_DETAILS)
