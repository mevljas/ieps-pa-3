from common.constants import RESULTS_LIMIT
from common.extractor import tokenize
from common.helpers import find_snippet
from common.reader import read_file, find_files


def search_files(searched_word: [str]) -> []:
    """
    Process all files in the 'input' directory.
    """
    filenames: [str] = find_files()
    document_tokens: {} = dict()
    search_result = []
    temp_results = []
    for filename in filenames:
        indexes, tokens = search_file(path=filename, searched_word=searched_word)
        short_filename = filename[9:]
        temp_results.append((short_filename, len(indexes), indexes))
        document_tokens[short_filename] = tokens

    temp_results = sorted(temp_results, key=lambda item: item[1], reverse=True)
    temp_results = temp_results[:RESULTS_LIMIT]

    print("Search complete.")
    print("Generating snippets...")

    for result in temp_results:
        filename, frequency, indexes = result
        if frequency > 0:
            snippets = find_snippet(document_text_tokens=document_tokens[filename], indexes=indexes)
            search_result.append((frequency, filename, snippets))

    print("Snippets generation complete.")
    return search_result


def search_file(path: str, searched_word: [str]) -> ([int], [str]):
    """
    Processes a file at the path and calculates word frequencies.
    :param searched_word:
    :param path: path of the file to be processed.
    """
    html = read_file(path=path)
    tokens = tokenize(html=html)
    return search(document_text=tokens, query_words=searched_word), tokens


def search(document_text: [str], query_words: []) -> [int]:
    return [idx for idx, value in enumerate(document_text) if
            value.lower() in query_words]
