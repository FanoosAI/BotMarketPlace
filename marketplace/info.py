import re
from typing import Tuple
import asyncio
import aiohttp
import requests
from fastapi import HTTPException
from marketplace import config


def get_username_and_server(username: str) -> Tuple[str, str]:
    full_username_pattern = r'@([^:]+):(.+)'
    match = re.search(full_username_pattern, username)
    if match:
        return match.group(1), match.group(2)

    return username, config['homeserver']


def get_user_info(username: str):
    user, server = get_username_and_server(username)
    path = config['homeserver_url'] + config['paths']['user_info'].format(user, server)
    try:
        req = requests.get(path, timeout=10)
    except requests.exceptions.Timeout as exc:
        raise HTTPException(408, "Timeout while trying to get user info.") from exc
    return req.json()


async def get_user_avatar(username: str) -> str:
    user, server = get_username_and_server(username)
    path = config['homeserver_url'] + config['paths']['user_avatar'].format(user, server)

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(path, timeout=10) as resp:
                if resp.status == 200:
                    response = await resp.json()
                    avatar_url = response['avatar_url']
                    return avatar_url
                raise Exception("User does not have an avatar.")
        except asyncio.TimeoutError as exc:
            raise Exception("Timeout while trying to get user avatar.") from exc
