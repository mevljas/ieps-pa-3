import nltk
from bs4 import BeautifulSoup, Comment
from nltk.tokenize import word_tokenize
from sqlite_search.helpers.constants import IGNORED_TAGS, stop_words_slovene


def create_soup(html: str) -> BeautifulSoup:
    """
    Creates a BeautifulSoup object with the provided html.
    :param html: html data to be used.
    :return: generated BeautifulSoup object.
    """
    return BeautifulSoup(html, "html.parser")


def clean_html(soup: BeautifulSoup) -> BeautifulSoup:
    """
    Removes unnecessary tags and comments from the HTML.
    :param soup: beautifulSoup object with html data to be cleaned.
    :return: beautifulSoup object with cleaned html data.
    """
    # Remove tags.
    [x.extract() for x in soup.findAll(IGNORED_TAGS)]
    # Find comments.
    comments = soup.findAll(string=lambda text: isinstance(text, Comment))
    # Remove comments.
    [comment.extract() for comment in comments]
    return soup


def tokenize(soup: BeautifulSoup) -> [str]:
    """
    Generate tokens from the HTML page using html_parser.
    :param soup: beautifulSoup object with html data to be cleaned.
    :return: a list of tokens.
    """
    text = soup.get_text(separator=' ')
    # Remove some characters.
    text = text.replace("'", "")
    text = text.replace('"', "")
    tokens = word_tokenize(text=text)
    return tokens


def extract(html: str) -> [str]:
    """
    Extract data from the html page.
    :param html: page HTML.
    :return: page tokens.
    """

    # Create the Beautiful soup object.
    soup = create_soup(html=html)

    # Clean HTML.
    soup = clean_html(soup=soup)

    # Generate tokens from HTML.
    tokens = tokenize(soup=soup)

    # Convert to lower case.
    tokens = [x.lower() for x in tokens]
    return tokens


def remove_stopwords(tokens: [str]) -> [str]:
    """
    Removes all stopwords from the list of tokens.
    :param tokens: a list of tokens.
    :return: filtered list of tokens.
    """
    return [token for token in tokens if token not in list(stop_words_slovene)]