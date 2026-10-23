import sqlite3

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

    cursor.execute(
        f"SELECT COUNT(*) FROM {table}"
    )

    count = cursor.fetchone()[0]

    print(
        f"{table}: {count}"
    )

conn.close()