import sqlite3


def get_db_cursor():
    return sqlite3.connect("botmarketplace.db").cursor()


def setup_db_file():
    cursor = get_db_cursor()
    with open('db_setup.sql', 'r') as f:
        sql_query = f.read()
        cursor.executescript(sql_query)
        cursor.connection.commit()


# check if botmarketplace.db file exists. if not, create one and setup the tables
try:
    open("botmarketplace.db")
except FileNotFoundError:
    setup_db_file()
