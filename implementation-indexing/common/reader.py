from os import walk


def read_file(path: str) -> str:
    with open(path, encoding='utf-8') as f:
        return f.read()


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
