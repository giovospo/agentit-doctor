from ..connection import get_connection


class AuditRepository:

    def __init__(self):

        self.conn = get_connection()
        self.cursor = self.conn.cursor()

    def log(
        self,
        action,
        entity_type,
        entity_id,
        details=""
    ):

        self.cursor.execute(
            """
            INSERT INTO audit_log(
                action,
                entity_type,
                entity_id,
                details,
                created_at
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
                action,
                entity_type,
                entity_id,
                details
            )
        )

        self.conn.commit()

    def close(self):

        self.conn.close()