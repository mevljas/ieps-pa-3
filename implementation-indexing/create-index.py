import os
import time

from common.constants import db_file
from sqlite_search.database.Database import Database
from sqlite_search.indexer import process_files


def init_database() -> Database:
    """
    Establishes database connection and creates the database if necessary.
    :return: Databse object.
    """
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
    start_time = time.time()
    print("Crating an inverse index...")
    process_files(database=database)
    end_time = time.time()
    print(f"Inverse index created in {(end_time - start_time)} s.")
    database.close_connection()


if __name__ == "__main__":
    main()
