from common.extractor import extract_text
from common.helpers import find_snippet
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
    frequencies, snippets = search(document_text=text.split(" "), query_words=searched_word)
    return frequencies, snippets


def search(document_text: [str], query_words: []) -> (int, str):
    print(document_text)
    # TODO: replacing chars doesnt work -> we have to use tokens.
    indexes = [idx for idx, value in enumerate(document_text) if
               value.lower().replace(",", "").replace(".", "") in query_words]
    frequencies = len(indexes)
    if frequencies > 0:
        snippets = find_snippet(document_text=document_text, indexes=indexes)
    else:
        snippets = ""

    return frequencies, snippets

