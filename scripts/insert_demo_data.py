import sqlite3
from datetime import datetime

DB_PATH = "storage/diagnostics.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

now = datetime.now().isoformat()

# --------------------------------------------------
# INCIDENT
# --------------------------------------------------

cursor.execute("""
INSERT OR IGNORE INTO incidents (
    id,
    hostname,
    status,
    severity,
    summary,
    created_at,
    updated_at
)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", (
    "INC_20261026_001",
    "WIN-CLIENT-01",
    "OPEN",
    "CRITICAL",
    "Windows Update Failure",
    now,
    now
))

# --------------------------------------------------
# EVENT
# --------------------------------------------------

cursor.execute("""
INSERT OR IGNORE INTO events (
    incident_id,
    event_time,
    source,
    event_id,
    level,
    provider,
    message
)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", (
    "INC_20261026_001",
    now,
    "System",
    1001,
    "Error",
    "WindowsUpdate",
    "Windows Update installation failed"
))

# --------------------------------------------------
# ANALYSIS
# --------------------------------------------------

cursor.execute("""
INSERT OR IGNORE INTO analyses (
    incident_id,
    root_cause,
    confidence,
    recommendation,
    analyzed_at
)
VALUES (?, ?, ?, ?, ?)
""", (
    "INC_20261026_001",
    "Corrupted Windows Update cache",
    0.92,
    "Reset Windows Update components",
    now
))

# --------------------------------------------------
# EVIDENCE
# --------------------------------------------------

cursor.execute("""
INSERT OR IGNORE INTO evidence (
    incident_id,
    root_cause,
    evidence
)
VALUES (?, ?, ?)
""", (
    "INC_20261026_001",
    "Corrupted Windows Update cache",
    "Event ID 1001 detected"
))

conn.commit()

print("✅ Demo data inserted successfully")

conn.close()