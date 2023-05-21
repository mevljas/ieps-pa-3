import sys
import time

from nltk import word_tokenize
from common.constants import db_file
from sqlite_search.database.Database import Database
from sqlite_search.retrival import process_files


def init_database() -> Database:
    database = Database()
    database.connect(url=db_file)
    return database


def print_result(result: list, query: str, elapsed_time: int) -> None:
    print(f"Results for a query: {query}")
    print()
    print(f"Results found in {elapsed_time} ms.")
    print("Frequencies Document                                   Snippet")
    print("----------- ------------------------------------------ "
          "-----------------------------------------------------------")
    for row in result:
        frequency, document, snippets = row
        print(f"{frequency:<12}{document:<43}{snippets}")

    print()
    print("Snippet was generated in x ms.")


def find_snippets(document_texts: dict, frequencies: [], query: str):
    result = []
    for row in frequencies:
        document, frequency, indexes = row
        document_text = document_texts[document].split(" ")
        query_words = [x.lower() for x in query.split(" ")]
        indexes = [idx for idx, value in enumerate(document_text) if
                   value.lower().replace(",", "").replace(".", "") in query_words]
        snippets = find_snippet(document_text=document_text, indexes=indexes)
        result.append((frequency, document, snippets))

    return result


def find_snippet(document_text: [], indexes: [int]):
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
        result.append(document_text[new_indexes[i]])

    if new_indexes[-1] != len(document_text) - 1:
        result.append('...')

    return " ".join(result)


def main() -> None:
    if len(sys.argv) != 2:
        print("Wrong number of command line arguments.", file=sys.stderr)
        return
    _, algorithm = sys.argv

    database = init_database()
    print("Loading documents...")
    document_text = process_files()
    print("Documents loaded.")
    start_time = time.time_ns() // 1_000_000
    searched_words = word_tokenize(text=sys.argv[1].lower())
    print("Searching the database...")
    result = database.search(words=searched_words)
    print("Search complete.")
    end_time = time.time_ns() // 1_000_000
    print("Generating snippets...")
    full_result = find_snippets(document_texts=document_text, frequencies=result, query=sys.argv[1])
    print("Snippets generation complete.")
    print()
    print_result(result=full_result, query=sys.argv[1], elapsed_time=end_time - start_time)
    database.close_connection()


if __name__ == "__main__":
    main()
