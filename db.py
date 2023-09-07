import logging
from enum import Enum

import motor.motor_asyncio

from settings import default_settings

logger = logging.getLogger(__name__)
logger.error(default_settings.MONGODB_URL)
client = motor.motor_asyncio.AsyncIOMotorClient(default_settings.MONGODB_URL)

default_db = client.plixa_db


class DBCollection(str, Enum):
    USER = "users"


user_collection = default_db.get_collection(DBCollection.USER)
