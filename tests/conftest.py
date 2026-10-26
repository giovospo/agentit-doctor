import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

sys.path.insert(
    0,
    str(ROOT_DIR)
)

from app.database.connection import get_connection


def pytest_sessionstart(session):
    conn = get_connection()

    with open(
        ROOT_DIR / "app/database/schema.sql",
        encoding="utf-8"
    ) as schema_file:
        conn.executescript(schema_file.read())

    for incident_number in range(3):
        incident_id = f"TEST_BASELINE_{incident_number}"
        conn.execute(
            """
            INSERT OR IGNORE INTO incidents(
                id, hostname, status, severity, summary, created_at, updated_at
            )
            VALUES(?, 'LOCALHOST', 'CLOSED', 'Test', 'Test fixture',
                   datetime('now'), datetime('now'))
            """,
            (incident_id,)
        )

        for event_number in range(5):
            event_source = f"TEST_EVENT_{event_number}"
            conn.execute(
                """
                INSERT OR IGNORE INTO events(
                    incident_id, event_time, source, level, message
                )
                VALUES(?, datetime('now'), ?, 'Test', ?)
                """,
                (incident_id, event_source, event_source)
            )

        for analysis_number in range(4):
            conn.execute(
                """
                INSERT OR IGNORE INTO analyses(
                    incident_id, root_cause, confidence, analyzed_at
                )
                VALUES(?, ?, 1, datetime('now'))
                """,
                (incident_id, f"TEST_CAUSE_{analysis_number}")
            )

    conn.commit()
    conn.close()
