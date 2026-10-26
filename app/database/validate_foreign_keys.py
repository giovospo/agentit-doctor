import sqlite3

TABLE_PRAGMAS = {
    "events": "PRAGMA foreign_key_list(events)",
    "analyses": "PRAGMA foreign_key_list(analyses)",
    "diagnostics": "PRAGMA foreign_key_list(diagnostics)",
    "agent_runs": "PRAGMA foreign_key_list(agent_runs)"
}

conn = sqlite3.connect(
    "storage/diagnostics.db"
)

cursor = conn.cursor()

for table, pragma_query in TABLE_PRAGMAS.items():

    print(
        f"\nForeign Keys: {table}"
    )

    cursor.execute(
        pragma_query
    )

    for fk in cursor.fetchall():

        print(fk)

conn.close()