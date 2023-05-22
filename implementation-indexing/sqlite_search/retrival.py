from common.extractor import tokenize
from common.reader import read_file


def process_files(result: [str, int, str]) -> dict:
    """
    Find and proces all files in the input directory.
    """
    document_text_tokens: {} = dict()
    for row in result:
        filename, _, _ = row
        text_tokens = process_file(path=f"../input/{filename}")
        document_text_tokens[filename] = text_tokens

    return document_text_tokens


def process_file(path: str) -> [str]:
    """
    Processes a file at the path and calculates word frequencies.
    :param path: path of the file to be processed.
    """
    html = read_file(path=path)
    text_tokens = tokenize(html=html)
    return text_tokens
