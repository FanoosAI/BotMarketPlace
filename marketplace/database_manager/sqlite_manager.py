"""
Deprecated.
This Project is now using MongoDB instead of SQLite.
This file is kept for reference purposes only.
"""

from .bot_info import BotInfo
from typing import List, Optional
import datetime
import os
import sqlite3
import logging
from contextlib import contextmanager

module_dir = os.path.dirname(os.path.abspath(__file__))


@contextmanager
def get_db_cursor():
    cursor = sqlite3.connect(f"{module_dir}/../data/botmarketplace.db").cursor()
    try:
        yield cursor
    finally:
        cursor.close()


def setup_db_file():
    with get_db_cursor() as cursor:
        with open(f'{module_dir}/../data/db_setup.sql', 'r') as file:
            sql_query = file.read()
            cursor.executescript(sql_query)
            cursor.connection.commit()
            logging.info("Database setup complete.")


def setup():
    # check if botmarketplace.db file exists. if not, create one and set up the tables
    try:
        with open(f"{module_dir}/../data/botmarketplace.db", 'r'):
            logging.info("botmarketplace.db detected. skipping db setup.")
    except FileNotFoundError:
        setup_db_file()


def get_bot(username: str) -> Optional[BotInfo]:
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM bots WHERE username=?", (username,))
        bot = cursor.fetchone()
        if bot is None:
            return None
        return BotInfo(username=bot[0], name=bot[1], description=bot[2], registered_at=bot[3], registered_by=bot[4])


def get_all_bots() -> List[BotInfo]:
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM bots")
        bots = cursor.fetchall()

    return [BotInfo(username=bot[0],
                    name=bot[1],
                    description=bot[2],
                    registered_at=bot[3],
                    registered_by=bot[4])
            for bot in bots]


def register_bot(username: str, name: str, description: Optional[str],
                 registered_at: datetime, registered_by: str):
    with get_db_cursor() as cursor:
        cursor.execute("INSERT INTO bots VALUES (?, ?, ?, ?, ?)",
                       (username, name, description, registered_at, registered_by))
        cursor.connection.commit()


def remove_bot(username: str):
    with get_db_cursor() as cursor:
        cursor.execute("DELETE FROM bots WHERE username=?", (username,))
        cursor.commit()
