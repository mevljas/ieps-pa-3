import sys
import time

from nltk import word_tokenize

from basic_search.retrival import search_files
from common.constants import RESULTS_LIMIT


def print_result(output: [], query: str, elapsed_time: int) -> None:
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
    for frequency, filename, snippet in output:
        print(f"{frequency:<12}{filename:<43}{snippet}")


def main() -> None:
    if len(sys.argv) != 2:
        print("Wrong number of command line arguments.", file=sys.stderr)
        return
    _, algorithm = sys.argv

    start_time = time.time_ns() // 1_000_000
    searched_words = word_tokenize(text=sys.argv[1].lower())
    print("Searching the documents...")
    output, end_time = search_files(query_words=searched_words)
    print()
    print()
    print_result(output=output,
                 query=sys.argv[1],
                 elapsed_time=end_time - start_time)


if __name__ == "__main__":
    main()
