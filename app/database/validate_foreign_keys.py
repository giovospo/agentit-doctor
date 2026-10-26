import sqlite3

VALID_TABLES = {
    "incidents",
    "events",
    "analyses",
    "diagnostics",
    "agent_runs",
    "audit_log",
    "evidence"
}

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

    if table not in VALID_TABLES:

        raise ValueError(
            f"Invalid table: {table}"
        )

    print(
        f"\nForeign Keys: {table}"
    )

    cursor.execute(
        f"PRAGMA foreign_key_list({table})"
    )

    for fk in cursor.fetchall():

        print(fk)

conn.close()