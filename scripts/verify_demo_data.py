import sqlite3

DB_PATH = "storage/diagnostics.db"

QUERIES = {
    "incidents": "SELECT COUNT(*) FROM incidents",
    "events": "SELECT COUNT(*) FROM events",
    "analyses": "SELECT COUNT(*) FROM analyses",
    "evidence": "SELECT COUNT(*) FROM evidence",
}


def main():
    conn = sqlite3.connect(DB_PATH)

    try:
        cursor = conn.cursor()

        for table_name, query in QUERIES.items():
            cursor.execute(query)

            total = cursor.fetchone()[0]

            print(f"{table_name}: {total}")

    finally:
        conn.close()


if __name__ == "__main__":
    main()