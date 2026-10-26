from typing import Any

from ..connection import get_connection


class EvidenceRepository:

    def __init__(self) -> None:

        self.conn = get_connection()
        self.cursor = self.conn.cursor()

    def create_evidence(
        self,
        incident_id: str,
        root_cause: str,
        evidence: str
    ) -> None:

        try:

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

        except Exception:

            self.conn.rollback()
            raise

    def get_evidence_by_incident(
        self,
        incident_id: str
    ) -> list[Any]:

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

    def get_all_evidence(
        self
    ) -> list[Any]:

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

    def close(self) -> None:

        try:
            self.cursor.close()
        except Exception:
            pass

        try:
            self.conn.close()
        except Exception:
            pass