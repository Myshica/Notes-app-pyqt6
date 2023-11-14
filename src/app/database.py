import sqlite3


class Database:
    def __init__(self, path):

        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()

    def add_note(self, title, content):
        with self.connection:
            return self.cursor.execute(
                "INSERT INTO notes_all (title, content) VALUES (?, ?)", (title, content)
            )

    def get_note(self, keyword):
        with self.connection:
            return self.cursor.execute(
                f"SELECT * FROM notes_all WHERE title LIKE ?", (f"%{keyword}%",)
            ).fetchall()

    def get_notes(self):
        with self.connection:
            return self.cursor.execute(
                "SELECT * FROM notes_all"
            ).fetchall()

    def del_note(self, id):
        with self.connection:
            return self.cursor.execute(
                "DELETE FROM notes_all WHERE id = ?", (id,)
            )
