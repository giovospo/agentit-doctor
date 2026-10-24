import sqlite3


def test_no_orphan_events():

    conn = sqlite3.connect(
        "storage/diagnostics.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM events e
        LEFT JOIN incidents i
        ON e.incident_id = i.id
        WHERE i.id IS NULL
        """
    )

    count = cursor.fetchone()[0]

    assert count == 0

    conn.close()


def test_no_orphan_analyses():

    conn = sqlite3.connect(
        "storage/diagnostics.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM analyses a
        LEFT JOIN incidents i
        ON a.incident_id = i.id
        WHERE i.id IS NULL
        """
    )

    count = cursor.fetchone()[0]

    assert count == 0

    conn.close()