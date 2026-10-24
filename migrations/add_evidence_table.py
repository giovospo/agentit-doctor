import sqlite3

conn = sqlite3.connect(
    "storage/diagnostics.db"
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS evidence (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    incident_id TEXT NOT NULL,

    root_cause TEXT NOT NULL,

    evidence TEXT NOT NULL,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (incident_id)
        REFERENCES incidents(id)
        ON DELETE CASCADE
)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_evidence_incident
ON evidence(incident_id)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_evidence_root_cause
ON evidence(root_cause)
""")

cursor.execute("""
CREATE UNIQUE INDEX IF NOT EXISTS ux_evidence
ON evidence(
    incident_id,
    root_cause,
    evidence
)
""")

conn.commit()

conn.close()

print(
    "Evidence table created successfully."
)