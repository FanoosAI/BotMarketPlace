import os
from os import getenv
from typing import List, Optional
import datetime

import pymongo
from pymongo import database

from marketplace.database_manager.bot_info import BotInfo

client: Optional[pymongo.MongoClient] = None
db: Optional[pymongo.database.Database] = None
collection: Optional[pymongo.database.Collection] = None


def setup():
    global client, db, collection
    mongo_uri = os.getenv("MONGO_URI")
    if mongo_uri is None:
        raise Exception("Mongo uri was not provided!")
    client = pymongo.MongoClient(mongo_uri)
    db = client["botMarketplace"]
    collection = db["registeredBots"]


def get_bot(username: str) -> Optional[BotInfo]:
    if collection is None:
        raise Exception("Please setup mongo manager first!")
    document = collection.find_one({'username': username}, {'_id': 0})

    if document is not None:
        return BotInfo(*document)
    return None


def get_all_bots() -> List[BotInfo]:
    if collection is None:
        raise Exception("Please setup mongo manager first!")
    return [BotInfo(**document) for document in collection.find({}, {'_id': 0})]


def register_bot(username: str, name: str, description: Optional[str],
                 registered_at: datetime, registered_by: str):
    if collection is None:
        raise Exception("Please setup mongo manager first!")
    collection.insert_one(locals())  # a dictionary from all input values
