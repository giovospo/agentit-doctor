import sqlite3

conn = sqlite3.connect(
    "storage/diagnostics.db"
)

cursor = conn.cursor()

cursor.execute(
    """
    SELECT *
    FROM incidents
    """
)

rows = cursor.fetchall()

print(f"Registros encontrados: {len(rows)}")

for row in rows:
    print(row)

conn.close()