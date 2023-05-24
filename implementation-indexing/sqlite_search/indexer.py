from os import walk

from common.reader import read_file
from sqlite_search.database import Database
from common.extractor import tokenize, remove_stopwords


def process_files(database: Database) -> None:
    """
    Processes all files in the input directory one by one and saved their filtered words and indexes to the database.
    :param database: Database object.
    """
    filenames: [str] = find_files()
    all_filtered_tokens: {} = set()
    all_frequencies: {} = dict()
    for filename in filenames:
        filtered_tokens, indexes = process_file(filename=filename)
        all_filtered_tokens = all_filtered_tokens.union(set(filtered_tokens))
        short_filename = filename[9:]
        all_frequencies[short_filename] = indexes

    database.save_words(words=all_filtered_tokens)
    database.save_frequencies(frequencies=all_frequencies)


def process_file(filename: str) -> ([str], dict):
    """
    Processes a file and finds word indexes.
    :param filename: path of the file to be processed.
    :return: a list of filtered tokens and a dictionary of word indexes.
    """
    html = read_file(path=filename)
    all_tokens = tokenize(html=html)
    # Convert to lower case.
    all_tokens = [x.lower() for x in all_tokens]
    filtered_tokens = remove_stopwords(tokens=all_tokens)
    indexes = find_indexes(all_tokens=all_tokens, filtered_tokens=filtered_tokens)
    return filtered_tokens, indexes


def find_indexes(all_tokens: [str], filtered_tokens: [str]) -> [dict]:
    """
    Find and returns word indexes.
    :param all_tokens: all document tokens.
    :param filtered_tokens: filtered document tokens, used for search query loop.
    :return: a dictionary of document indexes.
    """
    indexes = dict()
    for word in set(filtered_tokens):
        indexes[word] = [idx for idx, value in enumerate(all_tokens) if value == word]
    return indexes


def find_files() -> [str]:
    """
    Finds all input files in the input directory.
    :return: a list of filenames.
    """
    filenames: [str] = []
    for (path, directories, _) in walk('../input'):
        for directory in directories:
            for (path2, _, files) in walk(path + '/' + directory):
                filenames.extend([f'{path2}/{f}' for f in files])
    return filenames
