from ..connection import get_connection


class DiagnosisRepository:

    def __init__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

    # ======================
    # INCIDENTS
    # ======================

    def create_incident(
        self,
        incident_id,
        severity,
        summary,
        hostname="LOCALHOST"
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
                'OPEN',
                ?,
                ?,
                datetime('now'),
                datetime('now')
            )
            """,
            (
                incident_id,
                hostname,
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

    # ======================
    # EVENTS
    # ======================

    def create_event(
        self,
        incident_id,
        source,
        level,
        message
    ):

        self.cursor.execute(
            """
            INSERT OR IGNORE INTO events(
                incident_id,
                event_time,
                source,
                level,
                message
            )
            VALUES(
                ?,
                datetime('now'),
                ?,
                ?,
                ?
            )
            """,
            (
                incident_id,
                source,
                level,
                message
            )
        )

        self.conn.commit()

    def get_events_by_incident(
        self,
        incident_id
    ):

        self.cursor.execute(
            """
            SELECT *
            FROM events
            WHERE incident_id = ?
            """,
            (incident_id,)
        )

        columns = [
            column[0]
            for column in self.cursor.description
        ]

        rows = self.cursor.fetchall()

        return [
            dict(
                zip(
                    columns,
                    row
                )
            )
            for row in rows
        ]

    # ======================
    # ANALYSES
    # ======================

    def create_analysis(
        self,
        incident_id,
        root_cause,
        confidence,
        recommendation=None
    ):

        self.cursor.execute(
            """
            INSERT OR IGNORE INTO analyses(
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
                ?,
                datetime('now')
            )
            """,
            (
                incident_id,
                root_cause,
                confidence,
                recommendation
            )
        )

        self.conn.commit()

    def get_analyses_by_incident(
        self,
        incident_id
    ):

        self.cursor.execute(
            """
            SELECT *
            FROM analyses
            WHERE incident_id = ?
            ORDER BY analyzed_at DESC
            """,
            (
                incident_id,
            )
        )

        columns = [
            column[0]
            for column in self.cursor.description
        ]

        rows = self.cursor.fetchall()

        return [
            dict(
                zip(
                    columns,
                    row
                )
            )
            for row in rows
        ]

        # ======================
    # SAVE COMPLETE DIAGNOSIS
    # ======================

    def save_diagnosis(
        self,
        incident_id,
        severity,
        findings,
        root_causes,
        recommendation
    ):

        self.create_incident(
            incident_id,
            severity,
            recommendation
        )

        for finding in findings:

            self.create_event(
                incident_id,
                finding,
                severity,
                finding
            )

        for cause in root_causes:

            self.create_analysis(
                incident_id,
                cause["component"],
                cause["probability"],
                recommendation
            )

    # ======================
    # DETAILS
    # ======================

    def get_incident_details(
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

        incident = self.cursor.fetchone()

        self.cursor.execute(
            """
            SELECT *
            FROM events
            WHERE incident_id = ?
            """,
            (incident_id,)
        )

        events = self.cursor.fetchall()

        self.cursor.execute(
            """
            SELECT *
            FROM analyses
            WHERE incident_id = ?
            """,
            (incident_id,)
        )

        analyses = self.cursor.fetchall()

        return {
            "incident": dict(incident),
            "events": [dict(e) for e in events],
            "analyses": [dict(a) for a in analyses]
        }

    def close(self):

        try:
            self.cursor.close()
        except Exception:
            pass

        try:
            self.conn.close()
        except Exception:
            pass