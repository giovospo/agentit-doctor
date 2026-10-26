import sqlite3

TABLE_QUERIES = {
    "incidents": "SELECT COUNT(*) FROM incidents",
    "events": "SELECT COUNT(*) FROM events",
    "analyses": "SELECT COUNT(*) FROM analyses"
}

conn = sqlite3.connect(
    "storage/diagnostics.db"
)

cursor = conn.cursor()

for table, query in TABLE_QUERIES.items():

    cursor.execute(query)

    count = cursor.fetchone()[0]

    print(
        f"{table}: {count}"
    )

conn.close()
