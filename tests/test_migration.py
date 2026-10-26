import sqlite3


def test_migration_counts():

    conn = sqlite3.connect(
        "storage/diagnostics.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM incidents"
    )

    incidents = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM events"
    )

    events = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM analyses"
    )

    analyses = cursor.fetchone()[0]

    assert incidents >= 3
    assert events >= 14
    assert analyses >= 12

    conn.close()