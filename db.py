from enum import Enum

import motor.motor_asyncio

from settings import default_settings

client = motor.motor_asyncio.AsyncIOMotorClient(default_settings.MONGODB_URL)

default_db = client.plixa_db


class DBCollection(str, Enum):
    USER = "users"
    ORGANIZATION = "organizations"
    CLUSTER = "clusters"


def get_collection(collection_name: DBCollection):
    return default_db.get_collection(collection_name)
