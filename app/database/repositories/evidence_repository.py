from ..connection import get_connection


class EvidenceRepository:

    def __init__(self):

        self.conn = get_connection()
        self.cursor = self.conn.cursor()

    def create_evidence(
        self,
        incident_id,
        root_cause,
        evidence
    ):

        self.cursor.execute(
            """
            INSERT OR IGNORE INTO evidence(
                incident_id,
                root_cause,
                evidence
            )
            VALUES(
                ?,
                ?,
                ?
            )
            """,
            (
                incident_id,
                root_cause,
                evidence
            )
        )

        self.conn.commit()

    def get_evidence_by_incident(
        self,
        incident_id
    ):

        self.cursor.execute(
            """
            SELECT
                id,
                incident_id,
                root_cause,
                evidence,
                created_at
            FROM evidence
            WHERE incident_id = ?
            ORDER BY created_at DESC
            """,
            (
                incident_id,
            )
        )

        return self.cursor.fetchall()

    def get_all_evidence(self):

        self.cursor.execute(
            """
            SELECT
                id,
                incident_id,
                root_cause,
                evidence,
                created_at
            FROM evidence
            ORDER BY created_at DESC
            """
        )

        return self.cursor.fetchall()

    def close(self):

        try:

            self.cursor.close()

        except Exception:
            pass

        try:

            self.conn.close()

        except Exception:
            pass