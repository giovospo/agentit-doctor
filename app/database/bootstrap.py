from pathlib import Path

from app.database.connection import get_connection

SCHEMA_FILE = "app/database/schema.sql"


def bootstrap_database():
    db_path = Path("storage/diagnostics.db")

    if db_path.exists() and db_path.stat().st_size > 0:
        return

    conn = get_connection()

    try:
        with open(
            SCHEMA_FILE,
            "r",
            encoding="utf-8"
        ) as schema_file:

            schema = schema_file.read()

        conn.executescript(schema)

        conn.commit()

    finally:
        conn.close()