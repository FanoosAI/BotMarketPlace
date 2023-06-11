import re
import requests
from fastapi import HTTPException
from marketplace import config


def get_user_info(username: str):
    full_username_pattern = r'@([^:]+):(.+)'
    match = re.search(full_username_pattern, username)
    if match:
        username, home_server = match.group(1), match.group(2)
    else:
        home_server = config['homeserver']
    path = config['homeserver_url'] + config['paths']['user_info'].format(username, home_server)
    try:
        req = requests.get(path, timeout=5)
    except requests.exceptions.Timeout:
        raise HTTPException(408, "Timeout while trying to get user info.")
    return req.json()
