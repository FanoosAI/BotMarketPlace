import logging
import sys
import yaml
from . import sqlite_manager, mongo_manager


try:
    with open('config.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)
        database = config.get('database')
except FileNotFoundError:
    logging.error("config.yaml not found. please create one.")
    sys.exit(1)


def manager():
    if database == 'sqlite':
        sqlite_manager.setup()
        return sqlite_manager
    elif database == 'mongodb':
        mongo_manager.setup(config)
        return mongo_manager

    logging.error("Invalid database type: %s}", database)
    raise Exception("Invalid database type.")
