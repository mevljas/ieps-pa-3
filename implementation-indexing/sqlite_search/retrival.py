from common.extractor import tokenize
from common.reader import read_file, find_files


def process_files() -> dict:
    """
    Find and proces all files in the input directory.
    """
    filenames: [str] = find_files()
    document_text_tokens: {} = dict()
    for filename in filenames:
        text_tokens = process_file(path=filename)
        short_filename = filename[9:]
        document_text_tokens[short_filename] = text_tokens

    return document_text_tokens


def process_file(path: str) -> [str]:
    """
    Processes a file at the path and calculates word frequencies.
    :param path: path of the file to be processed.
    """
    html = read_file(path=path)
    text_tokens = tokenize(html=html)
    return text_tokens
