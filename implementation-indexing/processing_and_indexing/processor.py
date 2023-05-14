from os import walk
from processing_and_indexing.helpers.reader import read_file
from processing_and_indexing.extractor import extract


def process_files() -> None:
    # Download punkt for tokenizing files if necesarry.
    # nltk.download('punkt')
    filenames: [str] = find_files()
    files: [str] = [read_file(path=f) for f in filenames]
    tokens: [str] = [extract(html=f) for f in files]
    print(tokens)


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
