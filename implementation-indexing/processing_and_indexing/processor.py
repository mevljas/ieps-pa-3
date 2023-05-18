from os import walk
from processing_and_indexing.helpers.reader import read_file
from processing_and_indexing.extractor import extract, remove_stopwords


def process_files() -> None:
    """
    Find all proces all files in the input directory.
    """
    filenames: [str] = find_files()
    for filename in filenames:
        process_file(path=filename)


def process_file(path: str) -> None:
    """
    Processes a file at path.
    :param path: path of the file to be processed.
    """
    html = read_file(path=path)
    tokens: [str] = extract(html=html)
    filtered_tokens = remove_stopwords(tokens=tokens)
    print(filtered_tokens)


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
