import sqlite3

DB_PATH = "storage/diagnostics.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)

    conn.execute(
        "PRAGMA foreign_keys = ON"
    )

    conn.row_factory = sqlite3.Row

    return conn