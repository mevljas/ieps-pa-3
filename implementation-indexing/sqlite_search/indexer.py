from os import walk

from common.reader import read_file
from sqlite_search.database import Database
from common.extractor import tokenize, remove_stopwords


def process_files(database: Database):
    """
    Proces all files in the input directory.
    """
    filenames: [str] = find_files()
    all_word_tokens: {} = set()
    all_frequencies: {} = dict()
    for filename in filenames:
        word_tokens, frequencies = process_file(path=filename)
        all_word_tokens = all_word_tokens.union(set(word_tokens))
        short_filename = filename[9:]
        all_frequencies[short_filename] = frequencies

    database.save_words(words=all_word_tokens)
    database.save_frequencies(frequencies=all_frequencies)


def process_file(path: str) -> ([str], {}):
    """
    Processes a file at the path and calculates word frequencies.
    :param path: path of the file to be processed.
    """
    html = read_file(path=path)
    all_tokens = tokenize(html=html)
    # Convert to lower case.
    all_tokens = [x.lower() for x in all_tokens]
    filtered_tokens = remove_stopwords(tokens=all_tokens)
    frequencies = count_frequencies(all_tokens=all_tokens, filtered_tokens=filtered_tokens)
    return filtered_tokens, frequencies


def count_frequencies(all_tokens: [str], filtered_tokens: [str]):
    frequencies = dict()
    for unique_token in set(filtered_tokens):
        frequencies[unique_token] = find_indices(list_to_check=all_tokens, item_to_find=unique_token)
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
