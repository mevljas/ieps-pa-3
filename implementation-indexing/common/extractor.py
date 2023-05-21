from bs4 import BeautifulSoup, Comment
from nltk.tokenize import word_tokenize

from common.constants import IGNORED_TAGS, stop_words_slovene


def create_soup(html: str) -> BeautifulSoup:
    """
    Creates a BeautifulSoup object with the provided html.
    :param html: html data to be used.
    :return: generated BeautifulSoup object.
    """
    return BeautifulSoup(html, "html.parser")


def clean_html(soup: BeautifulSoup) -> str:
    """
    Removes unnecessary tags and comments from the HTML.
    :param soup: beautifulSoup object with html data to be cleaned.
    :return: cleaned text.
    """
    # Remove tags.
    [x.extract() for x in soup.findAll(IGNORED_TAGS)]
    # Find comments.
    comments = soup.findAll(string=lambda txt: isinstance(txt, Comment))
    # Remove comments.
    [comment.extract() for comment in comments]
    text = soup.get_text(separator=' ')
    # Remove some characters.
    text = text.replace("'", "")
    text = text.replace('"', "")
    # text = text.replace('\n', "")
    # Remove multiple spaces
    # text = re.sub(' +', ' ', text)
    text = " ".join(text.split())
    return text


def tokenize(html: str) -> (str, [str]):
    """
    Extract data from the html page and tokenize it.
    :param html: page HTML.
    :return: page text and page tokens.
    """

    # Create the Beautiful soup object.
    soup = create_soup(html=html)

    # Clean HTML.
    text = clean_html(soup=soup)

    # Generate tokens from HTML.
    tokens = word_tokenize(text=text)

    # Convert to lower case.
    tokens = [x.lower() for x in tokens]

    return text, tokens


def extract_text(html: str) -> (str, [str]):
    """
    Extract data from the html page.
    :param html: page HTML.
    :return: page text.
    """

    # Create the Beautiful soup object.
    soup = create_soup(html=html)

    # Clean HTML.
    text = clean_html(soup=soup)

    return text


def remove_stopwords(tokens: [str]) -> [str]:
    """
    Removes all stopwords from the list of tokens.
    :param tokens: a list of tokens.
    :return: filtered list of tokens.
    """
    return [token for token in tokens if token not in list(stop_words_slovene)]
