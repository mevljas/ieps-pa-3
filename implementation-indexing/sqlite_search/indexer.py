from os import walk

from database.Database import Database
from sqlite_search.extractor import tokenize, remove_stopwords
from sqlite_search.helpers.reader import read_file


def process_files(database: Database):
    """
    Proces all files in the input directory.
    """
    filenames: [str] = find_files()
    all_tokens: {} = set()
    all_frequencies: {} = dict()
    for filename in filenames:
        tokens, frequencies = process_file(path=filename)
        all_tokens = all_tokens.union(set(tokens))
        short_filename = filename[9:]
        all_frequencies[short_filename] = frequencies

    database.save_words(words=all_tokens)
    database.save_frequencies(frequencies=all_frequencies)


def process_file(path: str) -> ([str], {}):
    """
    Processes a file at the path and calculates word frequencies.
    :param path: path of the file to be processed.
    """
    html = read_file(path=path)
    _, tokens = tokenize(html=html)
    tokens = remove_stopwords(tokens=tokens)
    frequencies = count_frequencies(tokens)
    return tokens, frequencies


def count_frequencies(tokens: [str]):
    frequencies = dict()
    for unique_token in set(tokens):
        frequencies[unique_token] = find_indices(list_to_check=tokens, item_to_find=unique_token)
    return frequencies


def find_indices(list_to_check: [str], item_to_find: str) -> [int]:
    return [idx for idx, value in enumerate(list_to_check) if value == item_to_find]


def find_files() -> [str]:
    """
    Find all input files in the input directory.
    :return: a list of filenames.
    """
    filenames: [str] = []
    for (path, directories, _) in walk('../input'):
        for directory in directories:
            for (path2, _, files) in walk(path + '/' + directory):
                filenames.extend([f'{path2}/{f}' for f in files])
    return filenames
