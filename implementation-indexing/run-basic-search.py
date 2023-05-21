import sys
import time

from nltk import word_tokenize

from basic_search.retrival import search_files


def print_result(document_frequencies: dict, document_snippets: dict, query: str, elapsed_time: int) -> None:
    print(f"Results for a query: {query}")
    print()
    print(f"Results found in {elapsed_time} ms.")
    print("Frequencies Document                                   Snippet")
    print("----------- ------------------------------------------ "
          "-----------------------------------------------------------")
    for document in document_frequencies.keys():
        frequency = document_frequencies[document]
        snippet = document_snippets[document]
        print(f"{frequency:<12}{document:<43}{snippet}")
    print()
    print("Snippet was generated in x ms.")


def main() -> None:
    if len(sys.argv) != 2:
        print("Wrong number of command line arguments.", file=sys.stderr)
        return
    _, algorithm = sys.argv

    start_time = time.time_ns() // 1_000_000
    searched_words = word_tokenize(text=sys.argv[1].lower())
    print("Searching the database...")
    document_frequencies, document_snippets = search_files(searched_word=searched_words)
    document_frequencies = dict(sorted(document_frequencies.items(), key=lambda item: item[1], reverse=True))
    print("Search complete.")
    end_time = time.time_ns() // 1_000_000
    print()
    print_result(document_frequencies=document_frequencies,
                 document_snippets=document_snippets,
                 query=sys.argv[1],
                 elapsed_time=end_time - start_time)


if __name__ == "__main__":
    main()
