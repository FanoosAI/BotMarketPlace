import requests
from marketplace import config


def get_user_info(username: str):
    path = config['homeserver'] + config['paths']['user_info']
    params = {'user_id': username}
    req = requests.get(path, params=params, timeout=5)
    return req.json()
