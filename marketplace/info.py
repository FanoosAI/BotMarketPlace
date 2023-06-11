import re
from typing import Tuple

import requests
from fastapi import HTTPException
from marketplace import config


def get_username_and_server(username: str) -> Tuple[str, str]:
    full_username_pattern = r'@([^:]+):(.+)'
    match = re.search(full_username_pattern, username)
    if match:
        return match.group(1), match.group(2)
    else:
        return username, config['homeserver']


def get_user_info(username: str):
    user, server = get_username_and_server(username)
    path = config['homeserver_url'] + config['paths']['user_info'].format(user, server)
    try:
        req = requests.get(path, timeout=5)
    except requests.exceptions.Timeout:
        raise HTTPException(408, "Timeout while trying to get user info.")
    return req.json()


def get_user_avatar(username: str) -> str:
    user, server = get_username_and_server(username)
    path = config['homeserver_url'] + config['paths']['user_avatar'].format(user, server)
    try:
        # TODO: make this async
        req = requests.get(path, timeout=5)
        avatar_url = req.json()['avatar_url']
        return avatar_url
    except requests.exceptions.Timeout:
        raise Exception("Timeout while trying to get user avatar.")
    except KeyError:
        raise Exception("User does not have an avatar.")
