import os

from common.constants import db_file
from sqlite_search.database.Database import Database
from sqlite_search.indexer import process_files


def init_database() -> Database:
    # Remove old database if it exists.
    if os.path.isfile(db_file):
        print("Deleting old database...")
        os.remove(db_file)
        print("Old database deleted.")
    database = Database()
    database.connect(url=db_file)
    database.create_tables()
    return database


def main() -> None:
    database = init_database()
    print("Crating an inverse index...")
    process_files(database=database)
    print("Inverse index created.")
    database.close_connection()


if __name__ == "__main__":
    main()
