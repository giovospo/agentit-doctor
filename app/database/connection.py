from pathlib import Path
import sqlite3

DB_PATH = "storage/diagnostics.db"


def get_connection():
    Path(DB_PATH).parent.mkdir(
        parents=True,
        exist_ok=True
    )

    conn = sqlite3.connect(DB_PATH)

    conn.execute(
        "PRAGMA foreign_keys = ON"
    )

    conn.row_factory = sqlite3.Row

    return conn