from common.extractor import extract_text
from common.reader import read_file, find_files


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
