import sqlite3

conn = sqlite3.connect(
    "storage/diagnostics.db"
)

cursor = conn.cursor()

tables = [
    "incidents",
    "events",
    "analyses",
    "diagnostics",
    "agent_runs",
    "audit_log"
]

for table in tables:

    print(f"\n{'=' * 50}")
    print(f"TABLE: {table}")
    print(f"{'=' * 50}")

    cursor.execute(
        f"PRAGMA table_info({table})"
    )

    columns = cursor.fetchall()

    for column in columns:

        print(
            f"Column: {column[1]}"
            f" | Type: {column[2]}"
            f" | NotNull: {column[3]}"
            f" | PK: {column[5]}"
        )

conn.close()