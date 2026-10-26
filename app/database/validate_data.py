import sqlite3

VALID_TABLES = {
    "incidents",
    "events",
    "analyses",
    "evidence"
}

conn = sqlite3.connect(
    "storage/diagnostics.db"
)

cursor = conn.cursor()

tables = [
    "incidents",
    "events",
    "analyses"
]

for table in tables:

    if table not in VALID_TABLES:

        raise ValueError(
            f"Invalid table: {table}"
        )

    cursor.execute(
        f"SELECT COUNT(*) FROM {table}"
    )

    count = cursor.fetchone()[0]

    print(
        f"{table}: {count}"
    )

conn.close()