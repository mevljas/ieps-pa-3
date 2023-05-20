from database.Database import Database


def search(database: Database, words: [str]) -> None:
    database.search(words=words)
