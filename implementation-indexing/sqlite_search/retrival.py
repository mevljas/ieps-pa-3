from typing import List, Tuple

from database.Database import Database


def search(database: Database, words: [str]) -> list[tuple[str, int, str]]:
    return database.search(words=words)
