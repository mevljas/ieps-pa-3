import os
import sys

from database.Database import Database
from sqlite_search.processor import process_files
from sqlite_search.retrival import search


def init_database() -> Database:
    db_file = "inverted-index.db"
    # Remove old database if it exists.
    if os.path.isfile(db_file):
        os.remove(db_file)
    database = Database()
    database.connect(url=db_file)
    database.create_tables()
    return database


def print_result(result: list, query: str) -> None:
    print(f"Results for a query: {query}")
    print()
    print(" Results found in x ms.")
    print(" Frequencies Document                                   Snippet")
    print(" ----------- ------------------------------------------ "
          "-----------------------------------------------------------")
    for row in result:
        frequency, document, snippets = row
        print(f" {frequency:<12}{document:<43}{snippets}")


def find_snippets(document_tokens: dict, frequencies: []):
    result = []
    for row in frequencies:
        document, frequency, indexes = row
        snippets = find_snippet(tokens=document_tokens[document], indexes=[int(index) for index in indexes.split(",")])
        result.append((frequency, document, snippets))

    return result


def find_snippet(tokens: [], indexes: [int]):
    result = []
    new_indexes = set()
    for index in indexes:
        new_indexes = new_indexes.union(set(range(index - 3, index + 1)))
        new_indexes = new_indexes.union(set(range(index + 1, index + 4)))

    new_indexes = list(new_indexes)
    new_indexes.sort()
    for i in range(0, len(new_indexes)):
        current_index = new_indexes[i]
        if i == 0 and current_index > 0:
            result.append('...')
        elif i > 0 and current_index - new_indexes[i - 1] > 1:
            result.append('...')
        result.append(tokens[new_indexes[i]])

    if new_indexes[-1] != len(tokens) - 1:
        result.append('...')

    return " ".join(result)


def main() -> None:
    if len(sys.argv) != 2:
        print("Wrong number of command line arguments.", file=sys.stderr)
        return
    _, algorithm = sys.argv

    database = init_database()
    document_tokens = process_files(database=database)
    words = sys.argv[1].lower().split(" ")
    words = [f'{word}' for word in words]
    result = search(database=database, words=words)
    full_result = find_snippets(document_tokens=document_tokens, frequencies=result)
    print_result(result=full_result, query=sys.argv[1])
    database.close_connection()


if __name__ == "__main__":
    main()
