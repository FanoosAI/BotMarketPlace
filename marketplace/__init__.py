"""
This module contains general functions for the marketplace.
"""

import logging
import os
import sqlite3
import sys
from contextlib import contextmanager

import yaml

module_dir = os.path.dirname(os.path.abspath(__file__))

@contextmanager
def get_db_cursor():
    cursor = sqlite3.connect(f"{module_dir}/botmarketplace.db").cursor()
    try:
        yield cursor
    finally:
        cursor.close()


def setup_db_file():
    with get_db_cursor() as cursor:
        with open(f'{module_dir}/db_setup.sql', 'r') as file:
            sql_query = file.read()
            cursor.executescript(sql_query)
            cursor.connection.commit()
            logging.info("Database setup complete.")



# check if botmarketplace.db file exists. if not, create one and setup the tables
try:
    with open(f"{module_dir}/botmarketplace.db", 'r'):
        logging.info("botmarketplace.db detected. skipping db setup.")
except FileNotFoundError:
    setup_db_file()

try:
    with open('config.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)
except FileNotFoundError:
    logging.error("config.yaml not found. please create one.")
    sys.exit(1)
