import sys
import time

from nltk import word_tokenize

from basic_search.retrival import search_files
from common.constants import RESULTS_LIMIT


def print_result(result: [], query: str, elapsed_time: int) -> None:
    print(f'Results for a query: "{query}"')
    print(f"Results found in {elapsed_time} ms.")
    print()
    print("Frequencies Document                                   Snippet")
    print("-" * 11 + " " + "-" * 42 + " " + "-" * 80)
    for frequency, filename, snippet in result:
        print(f"{frequency:<12}{filename:<43}{snippet}")


def main() -> None:
    if len(sys.argv) != 2:
        print("Wrong number of command line arguments.", file=sys.stderr)
        return
    _, algorithm = sys.argv

    start_time = time.time_ns() // 1_000_000
    searched_words = word_tokenize(text=sys.argv[1].lower())
    print("Searching the documents...")
    result = search_files(searched_word=searched_words)
    end_time = time.time_ns() // 1_000_000
    print()
    print()
    print_result(result=result,
                 query=sys.argv[1],
                 elapsed_time=end_time - start_time)


if __name__ == "__main__":
    main()
