import sqlite3


class Database:
    def __init__(self):
        self.conn = None

    def connect(self, url: str):
        self.conn = sqlite3.connect(url)

    def create_tables(self):
        # Create table
        c = self.conn.cursor()

        c.execute('''
            CREATE TABLE IndexWord (
                word TEXT PRIMARY KEY
            );
        ''')

        c.execute('''
            CREATE TABLE Posting (
                word TEXT NOT NULL,
                documentName TEXT NOT NULL,
                frequency INTEGER NOT NULL,
                indexes TEXT NOT NULL,
                PRIMARY KEY(word, documentName),
                FOREIGN KEY (word) REFERENCES IndexWord(word)
            );
        ''')

        # Save (commit) the changes
        self.conn.commit()

    def save_words(self, words: []):
        c = self.conn.cursor()
        for word in words:
            value = f"('{word}')"
            c.execute(f"INSERT INTO IndexWord VALUES {value};")
        self.conn.commit()

    def save_frequencies(self, frequencies: {}):
        c = self.conn.cursor()
        for file in frequencies.items():
            values = ""
            filename, indexes = file
            for index in indexes:
                values += f"('{index}', '{filename}', {len(indexes[index])}, '{','.join(map(str, indexes[index]))}'),"
            # Check whether the string is not empty.
            if values:
                # Remove the last character
                values = values[:-1]
                c.execute(f"INSERT INTO Posting VALUES {values};")

        self.conn.commit()

    def search(self, words: [str]) -> list[tuple[str, int, str]]:
        c = self.conn.cursor()
        values = ""
        for word in words:
            values += f"'{word}',"
        if values:
            # Remove the last character
            values = values[:-1]
        cursor = c.execute(f"""
            SELECT p.documentName AS docName, SUM(frequency) AS freq, GROUP_CONCAT(indexes) AS idxs
            FROM Posting p
            WHERE p.word IN ({values}) AND frequency > 0
            GROUP BY p.documentName
            ORDER BY freq DESC;
        """)
        result = []
        for row in cursor:
            document, frequency, indexes = row
            result.append((document, frequency, indexes))

        return result

    def close_connection(self):
        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        self.conn.close()
