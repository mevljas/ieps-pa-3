import os
import sys

from database.Database import Database
from sqlite_search.processor import process_files


def init_database() -> Database:
    # Remove old database if it exists.
    db_file = "inverted-index.db"
    # If file exists, delete it.
    if os.path.isfile(db_file):
        os.remove(db_file)
    database = Database()
    database.connect(url=db_file)
    database.create_tables()
    return database


def main() -> None:
    database = init_database()
    process_files(database=database)
    database.close_connection()


if __name__ == "__main__":
    main()
