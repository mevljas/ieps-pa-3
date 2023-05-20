import os
import sys

from database.Database import Database
from sqlite_search.processor import process_files
from sqlite_search.retrival import search


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


def print_result(result: dict, query: str) -> None:
    print(f"Results for a query: {query}")
    print()
    print(" Results found in 4ms.")
    print(" Frequencies Document                                  Snippet")
    print("----------- ----------------------------------------- "
          "-----------------------------------------------------------")

def main() -> None:
    if len(sys.argv) != 2:
        print("Wrong number of command line arguments.", file=sys.stderr)
        return
    _, algorithm = sys.argv

    database = init_database()
    process_files(database=database)
    words = sys.argv[1].lower().split(" ")
    words = [f'{word}' for word in words]
    search(database=database, words=words)
    database.close_connection()


if __name__ == "__main__":
    main()
