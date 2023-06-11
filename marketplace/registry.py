"""
This module contains functions for registering bots in the marketplace.
"""

from typing import Optional
from datetime import datetime
from fastapi import HTTPException
from marketplace import get_db_cursor
from marketplace.info import get_user_info


def register_bot(username: str, name: str, description: Optional[str],
                 registered_at: datetime, registered_by: str):
    """
    Register a bot in the marketplace.
    """
    validate_username(username)
    check_username_existance(username, registered_by)
    check_for_repeated_registry(username)

    with get_db_cursor() as cursor:
        cursor.execute("INSERT INTO bots VALUES (?, ?, ?, ?, ?)",
                       (username, name, description, registered_at, registered_by))
        cursor.connection.commit()


def validate_username(username: str):
    # check if username conforms to the format
    if not username.startswith('bot_'):
        raise HTTPException(400, "Username must start with 'bot_'")
    if not username.islower():
        raise HTTPException(400, "Username must be all lowercase.")
    # check if username is alphanumeric except for underscores
    if not username.replace('_', '').isalnum():
        raise HTTPException(400, "Username must only contain alphanumerics or _.")


def check_username_existance(bot_username: str, registrar_username: str):
    # check if bot exists
    user_info = get_user_info(bot_username)
    if user_info.get('errcode') is not None:
        raise HTTPException(404, f"Bot username does not exists. ->"
                                 f" {user_info.get('errcode')}: {user_info.get('error')}")

    # check if registered_by is a valid user
    user_info = get_user_info(registrar_username)
    if user_info.get('errcode') is not None:
        raise HTTPException(404, f"Registrar username does not exists. ->"
                                 f" {user_info.get('errcode')}: {user_info.get('error')}")


def check_for_repeated_registry(bot_username: str):
    # check if bot is already registered
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM bots WHERE username=?", (bot_username,))
        if cursor.fetchone() is not None:
            raise HTTPException(400, "Bot is already registered.")
