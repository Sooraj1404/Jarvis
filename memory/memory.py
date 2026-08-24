import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).parent / "jarvis_memory.db"


class Memory:
    def __init__(self):
        self.connection = sqlite3.connect(DB_PATH)

        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT UNIQUE NOT NULL,
                value TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        self.connection.commit()

    def remember(self, key, value):
        self.connection.execute(
            """
            INSERT INTO memories (key, value)
            VALUES (?, ?)
            ON CONFLICT(key)
            DO UPDATE SET
                value = excluded.value,
                updated_at = CURRENT_TIMESTAMP
            """,
            (key, value),
        )

        self.connection.commit()

    def recall(self, key):
        cursor = self.connection.execute(
            "SELECT value FROM memories WHERE key = ?",
            (key,),
        )

        result = cursor.fetchone()

        if result:
            return result[0]

        return None

    def get_all(self):
        cursor = self.connection.execute(
            "SELECT key, value FROM memories ORDER BY key"
        )

        return cursor.fetchall()

    def forget(self, key):
        cursor = self.connection.execute(
            "DELETE FROM memories WHERE key = ?",
            (key,),
        )

        self.connection.commit()

        return cursor.rowcount > 0

    def close(self):
        self.connection.close()