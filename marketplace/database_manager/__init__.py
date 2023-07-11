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
        return sqlite_manager
    if database == 'mongo':
        return mongo_manager
    else:
        logging.error("Invalid database type: %s}", database)
        raise Exception("Invalid database type.")
