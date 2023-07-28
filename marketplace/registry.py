"""
This module contains functions for registering bots in the marketplace.
"""
import logging
import os
from typing import Optional
from datetime import datetime

import yaml
from fastapi import HTTPException
from marketplace.info import get_user_info, get_username_and_server
from marketplace.database_manager import manager


def register_bot(authorization: Optional[str], username: str, name: str, description: Optional[str],
                 registered_at: datetime, registered_by: str):
    """
    Register a bot in the marketplace.
    """
    authenticate_api_key(registered_by, authorization)
    user, server = get_username_and_server(username)
    full_username = "@{}:{}".format(user, server)
    validate_username(user)
    check_username_existance(username, registered_by)
    check_for_repeated_registry(full_username)

    manager().register_bot(full_username, name, description, registered_at, registered_by)


def remove_bot(username: str, bot_username: str, api_key: Optional[str]):
    authenticate_api_key(username, api_key)
    if not _is_bot_registered(bot_username):
        raise HTTPException(404, "This bot is not registered!")
    manager().remove_bot(bot_username)


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


def _is_bot_registered(bot_username: str):
    return manager().get_bot(bot_username) is not None


def check_for_repeated_registry(bot_username: str):
    # check if bot is already registered
    if _is_bot_registered(bot_username):
        raise HTTPException(400, "Bot is already registered.")


def authenticate_api_key(username: str, api_key: Optional[str]):
    if not api_key:
        raise HTTPException(status_code=401, detail="Unauthorized")

    module_dir = os.path.dirname(os.path.abspath(__file__))
    try:
        with open(f"{module_dir}/data/api_keys.yaml") as f:
            api_keys = yaml.safe_load(f)
            print(username)
            print(api_keys)
            if username in api_keys:
                if api_keys[username] != api_key:
                    raise HTTPException(401, "Invalid API key.")
            else:
                raise HTTPException(401, f"Username {username} not allowed to register bots.")
    except FileNotFoundError as exc:
        logging.error("api_keys file not found at %s/data/api_keys", module_dir)
        raise HTTPException(500, "api_keys file not found.") from exc
