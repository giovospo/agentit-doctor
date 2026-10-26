import sqlite3

from app.database.connection import get_connection


class DiagnosisRepository:

    def __init__(self):

        self.conn = get_connection()
        self.cursor = self.conn.cursor()

    def create_incident(
        self,
        incident_id,
        severity,
        summary
    ):

        self.cursor.execute(
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
                "OPEN",
                severity,
                summary
            )
        )

        self.conn.commit()

    def get_incident(
        self,
        incident_id
    ):

        self.cursor.execute(
            """
            SELECT *
            FROM incidents
            WHERE id = ?
            """,
            (incident_id,)
        )

        return self.cursor.fetchone()

    def close(self):

        self.conn.close()