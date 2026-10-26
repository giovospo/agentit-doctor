import sqlite3

conn = sqlite3.connect("storage/diagnostics.db")
cursor = conn.cursor()

tables = [
    "incidents",
    "events",
    "analyses",
    "evidence"
]

for table in tables:

    cursor.execute(
        f"SELECT COUNT(*) FROM {table}"
    )

    total = cursor.fetchone()[0]

    print(
        f"{table}: {total}"
    )

conn.close()