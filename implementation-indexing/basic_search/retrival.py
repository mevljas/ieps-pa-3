from common.extractor import extract_text
from common.reader import read_file, find_files


def search_files(searched_word: [str]) -> (dict, dict):
    """
    Find all proces all files in the input directory.
    """
    filenames: [str] = find_files()
    document_snippets: {} = dict()
    document_frequencies: {} = dict()
    for filename in filenames:
        frequencies, snippets = search_file(path=filename, searched_word=searched_word)
        short_filename = filename[9:]
        if frequencies > 0:
            document_frequencies[short_filename] = frequencies
            document_snippets[short_filename] = snippets

    return document_frequencies, document_snippets


def search_file(path: str, searched_word: [str]) -> (int, str):
    """
    Processes a file at the path and calculates word frequencies.
    :param searched_word:
    :param path: path of the file to be processed.
    """
    html = read_file(path=path)
    text = extract_text(html=html)
    query_words = [x.lower() for x in searched_word]
    frequencies, snippets = search(document_text=text.split(" "), query_words=query_words)
    return frequencies, snippets


def search(document_text: str, query_words: []) -> (int, str):
    indexes = [idx for idx, value in enumerate(document_text) if
               value.lower().replace(",", "").replace(".", "") in query_words]
    frequencies = len(indexes)
    if frequencies > 0:
        snippets = find_snippet(document_text=document_text, indexes=indexes)
    else:
        snippets = ""

    return frequencies, snippets


def find_snippet(document_text: [str], indexes: [int]) -> str:
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
