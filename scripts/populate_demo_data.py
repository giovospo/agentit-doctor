import sqlite3
from datetime import datetime, timedelta

DB_PATH = "storage/diagnostics.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

now = datetime.now()

incidents = [
    (
        "INC_20261026_001",
        "WIN-CLIENT-01",
        "OPEN",
        "CRITICAL",
        "Windows Update Failure"
    ),
    (
        "INC_20261026_002",
        "WIN-SRV-01",
        "OPEN",
        "HIGH",
        "Network Connectivity Issue"
    ),
    (
        "INC_20261026_003",
        "WIN-APP-01",
        "INVESTIGATING",
        "MEDIUM",
        "High CPU Usage"
    ),
]

for incident in incidents:
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
        incident[0],
        incident[1],
        incident[2],
        incident[3],
        incident[4],
        now.isoformat(),
        now.isoformat()
    ))

events = [
    ("INC_20261026_001","System",1001,"Error","WindowsUpdate","Windows Update installation failed"),
    ("INC_20261026_001","System",1002,"Warning","WindowsUpdate","Update package validation failed"),
    ("INC_20261026_001","System",1003,"Error","DISM","Component store corruption detected"),
    ("INC_20261026_001","System",1004,"Error","CBS","Servicing stack inconsistency"),

    ("INC_20261026_002","Network",2001,"Error","TCPIP","Network adapter disconnected"),
    ("INC_20261026_002","Network",2002,"Warning","DNS","DNS resolution timeout"),
    ("INC_20261026_002","Network",2003,"Error","TCPIP","TCP reset detected"),
    ("INC_20261026_002","Network",2004,"Warning","DHCP","DHCP renewal failure"),

    ("INC_20261026_003","Application",3001,"Warning","Performance","CPU usage exceeded 95%"),
    ("INC_20261026_003","Application",3002,"Warning","Performance","Application response degradation"),
    ("INC_20261026_003","Application",3003,"Error","ProcessMonitor","Resource intensive process detected"),
    ("INC_20261026_003","Application",3004,"Warning","Performance","Sustained high CPU utilization")
]

for idx, event in enumerate(events):

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
        event[0],
        (now + timedelta(minutes=idx)).isoformat(),
        event[1],
        event[2],
        event[3],
        event[4],
        event[5]
    ))

    analyses = [
    (
        "INC_20261026_001",
        "Corrupted Windows Update cache",
        0.92,
        "Reset Windows Update components"
    ),
    (
        "INC_20261026_002",
        "Network adapter driver corruption",
        0.88,
        "Reinstall network adapter drivers"
    ),
    (
        "INC_20261026_003",
        "Background process saturation",
        0.79,
        "Optimize background services"
    )
]

for analysis in analyses:

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
        analysis[0],
        analysis[1],
        analysis[2],
        analysis[3],
        now.isoformat()
    ))

    evidences = [
    (
        "INC_20261026_001",
        "Corrupted Windows Update cache",
        "Event ID 1001 detected"
    ),
    (
        "INC_20261026_001",
        "Corrupted Windows Update cache",
        "CBS corruption detected"
    ),
    (
        "INC_20261026_002",
        "Network adapter driver corruption",
        "TCP reset events registered"
    ),
    (
        "INC_20261026_002",
        "Network adapter driver corruption",
        "Multiple DNS failures detected"
    ),
    (
        "INC_20261026_003",
        "Background process saturation",
        "CPU usage above 95 percent"
    ),
    (
        "INC_20261026_003",
        "Background process saturation",
        "Performance counters exceeded threshold"
    )
]

for evidence in evidences:

    cursor.execute("""
    INSERT OR IGNORE INTO evidence (
        incident_id,
        root_cause,
        evidence
    )
    VALUES (?, ?, ?)
    """, (
        evidence[0],
        evidence[1],
        evidence[2]
    ))

    conn.commit()

print("✅ Demo dataset loaded")

conn.close()