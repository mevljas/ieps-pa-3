from common.extractor import tokenize
from common.reader import read_file


def process_files(result: [str, int, str]) -> dict:
    """
    Find and proces all files in the input directory. Saves document tokens to a dictionary and returns it.
    :param result: result of the database query.
    :return: a dictionary of documents with their tokens.
    """
    all_tokens: {} = dict()
    for row in result:
        filename, _, _ = row
        tokens = process_file(filename=f"../input/{filename}")
        all_tokens[filename] = tokens

    return all_tokens


def process_file(filename: str) -> [str]:
    """
    Processes a file and returns document tokens.
    :param filename: path of the file to be processed.
    :return: a list of document tokens.
    """
    html = read_file(path=filename)
    return tokenize(html=html)
