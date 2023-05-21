from os import walk

from sqlite_search.extractor import extract_text
from sqlite_search.helpers.reader import read_file


def process_files() -> dict:
    """
    Find all proces all files in the input directory.
    """
    filenames: [str] = find_files()
    document_text: {} = dict()
    for filename in filenames:
        text = process_file(path=filename)
        short_filename = filename[9:]
        document_text[short_filename] = text

    return document_text


def process_file(path: str) -> str:
    """
    Processes a file at the path and calculates word frequencies.
    :param path: path of the file to be processed.
    """
    html = read_file(path=path)
    text = extract_text(html=html)
    return text


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
