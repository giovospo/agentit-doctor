import sqlite3

conn = sqlite3.connect(
    "storage/diagnostics.db"
)

cursor = conn.cursor()

for table in [
    "events",
    "analyses",
    "diagnostics",
    "agent_runs"
]:

    print(
        f"\nForeign Keys: {table}"
    )

    cursor.execute(
        f"PRAGMA foreign_key_list({table})"
    )

    for fk in cursor.fetchall():

        print(fk)

conn.close()