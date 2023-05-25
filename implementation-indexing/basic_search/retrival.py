import time

from common.constants import RESULTS_LIMIT
from common.extractor import tokenize
from common.helpers import find_snippet
from common.reader import read_file, find_files


def search_files(query_words: [str]) -> ([], int):
    """
    Searches all files in the 'input' directory. Returns a list that of consists of frequencies, filename and snippets.
    :param query_words: a list of words we're searching for.
    :return: a list of search results and end search time.
    """
    filenames: [str] = find_files()
    document_tokens: {} = dict()
    search_result = []
    temp_results = []
    for filename in filenames:
        indexes, tokens = search_file(filename=filename, query_words=query_words)
        short_filename = filename[9:]
        temp_results.append((short_filename, len(indexes), indexes))
        document_tokens[short_filename] = tokens

    temp_results = sorted(temp_results, key=lambda item: item[1], reverse=True)
    # Limit number of results.
    temp_results = temp_results[:RESULTS_LIMIT]
    end_time = time.time_ns() // 1_000_000

    print("Search complete.")
    print("Generating snippets...")

    for result in temp_results:
        filename, frequency, indexes = result
        if frequency > 0:
            snippets = find_snippet(tokens=document_tokens[filename], indexes=indexes)
            search_result.append((frequency, filename, snippets))

    print("Snippets generation complete.")
    return search_result, end_time


def search_file(filename: str, query_words: [str]) -> ([int], [str]):
    """
    Reads a file and finds word indexes.
    :param query_words: a list of words we're searching for.
    :param filename: path of the file to be searched.
    """
    html = read_file(path=filename)
    tokens = tokenize(html=html)
    return search(tokens=tokens, query_words=query_words), tokens


def search(tokens: [str], query_words: []) -> [int]:
    """
    Find and returns indexes of document tokens that match the searched words.
    :param tokens: a list of document tokens.
    :param query_words: a list of words we're searching for.
    :return: a list of indexes.
    """
    return [idx for idx, value in enumerate(tokens) if
            value.lower() in query_words]
