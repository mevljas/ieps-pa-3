import sys
import time

from nltk import word_tokenize
from common.constants import db_file
from common.helpers import find_snippet
from sqlite_search.database.Database import Database
from sqlite_search.retrival import process_files


def init_database() -> Database:
    """
    Establishes database connection.
    :return: Database object.
    """
    database = Database()
    database.connect(url=db_file)
    return database


def print_result(output: list, query: str, elapsed_time: int) -> None:
    """
    Prints the results to the standard output.
    :param output: list of results.
    :param query: user defines query.
    :param elapsed_time: Measured time for this searched.
    """
    print(f'Results for a query: "{query}"')
    print(f"Results found in {elapsed_time} ms.")
    print()
    print("Frequencies Document                                   Snippet")
    print("-" * 11 + " " + "-" * 42 + " " + "-" * 80)
    for row in output:
        frequency, document, snippets = row
        print(f"{frequency:<12}{document:<43}{snippets}")


def find_snippets(all_tokens: dict, result: []) -> []:
    """
    Finds snippets for all results.
    :param all_tokens: dictionary of all tokens by document name.
    :param result: result of the database query.
    :return: Generated list of outputs contain frequency, document name and snippets.
    """
    output = []
    for row in result:
        document, frequency, indexes = row
        indexes = [int(x) for x in indexes.split(",")]
        tokens = all_tokens[document]
        snippets = find_snippet(tokens=tokens, indexes=indexes)
        output.append((frequency, document, snippets))

    return output


def main() -> None:
    if len(sys.argv) != 2:
        print("Wrong number of command line arguments.", file=sys.stderr)
        return
    _, algorithm = sys.argv

    database = init_database()
    start_time = time.time_ns()
    searched_words = word_tokenize(text=sys.argv[1].lower())
    print("Searching the database...")
    result = database.search(words=searched_words)
    print("Search complete.")
    end_time = time.time_ns()
    print("Loading documents...")
    documents_tokens = process_files(result=result)
    print("Documents loaded.")
    print("Generating snippets...")
    output = find_snippets(all_tokens=documents_tokens, result=result)
    print("Snippets generation complete.")
    print()
    print()
    print_result(output=output, query=sys.argv[1], elapsed_time=(end_time - start_time) // 1_000_000)
    database.close_connection()


if __name__ == "__main__":
    main()
