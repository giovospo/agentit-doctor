import json
import sqlite3
from pathlib import Path

DB_FILE = "storage/diagnostics.db"

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

history_dir = Path("history")

for json_file in history_dir.glob("*.json"):

    print(f"Migrating {json_file.name}")

    with open(
        json_file,
        "r",
        encoding="utf-8"
    ) as f:

        data = json.load(f)

    incident_id = json_file.stem

    severity = data.get(
        "severity",
        "Unknown"
    )

    version = data.get(
        "version",
        "Unknown"
    )

    generated_by = data.get(
        "generated_by",
        "AgentIT Doctor"
    )

    summary = (
        f"{generated_by} - "
        f"Version {version}"
    )

    cursor.execute(
        """
        INSERT OR IGNORE INTO incidents(
            id,
            hostname,
            status,
            severity,
            summary,
            created_at,
            updated_at
        )
        VALUES(
            ?,
            ?,
            ?,
            ?,
            ?,
            datetime('now'),
            datetime('now')
        )
        """,
        (
            incident_id,
            "LOCALHOST",
            "CLOSED",
            severity,
            summary
        )
    )

    findings = data.get(
        "findings",
        []
    )

    for finding in findings:

        cursor.execute(
            """
            INSERT INTO events(
                incident_id,
                event_time,
                source,
                event_id,
                level,
                provider,
                message
            )
            VALUES(
                ?,
                datetime('now'),
                ?,
                NULL,
                ?,
                NULL,
                ?
            )
            """,
            (
                incident_id,
                finding,
                severity,
                finding
            )
        )

    root_causes = data.get(
        "root_causes",
        []
    )

    for cause in root_causes:

        cursor.execute(
            """
            INSERT INTO analyses(
                incident_id,
                root_cause,
                confidence,
                recommendation,
                analyzed_at
            )
            VALUES(
                ?,
                ?,
                ?,
                NULL,
                datetime('now')
            )
            """,
            (
                incident_id,
                cause["component"],
                cause["probability"]
            )
        )

conn.commit()
conn.close()

print("Migration completed")