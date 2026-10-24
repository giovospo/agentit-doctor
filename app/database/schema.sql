PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS incidents (
    id TEXT PRIMARY KEY,
    hostname TEXT NOT NULL,
    status TEXT NOT NULL,
    severity TEXT NOT NULL,
    summary TEXT,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
);

CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    incident_id TEXT NOT NULL,

    event_time DATETIME NOT NULL,
    source TEXT NOT NULL,

    event_id INTEGER,
    level TEXT,
    provider TEXT,
    message TEXT,

    FOREIGN KEY (incident_id)
        REFERENCES incidents(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS analyses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    incident_id TEXT NOT NULL,

    root_cause TEXT,
    confidence REAL,
    recommendation TEXT,

    analyzed_at DATETIME,

    FOREIGN KEY (incident_id)
        REFERENCES incidents(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS diagnostics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    incident_id TEXT NOT NULL,

    cpu_usage REAL,
    memory_usage REAL,
    disk_usage REAL,

    network_status TEXT,

    collected_at DATETIME,

    FOREIGN KEY (incident_id)
        REFERENCES incidents(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS agent_runs (
    id TEXT PRIMARY KEY,

    incident_id TEXT,

    agent_name TEXT,
    execution_time_ms INTEGER,
    result TEXT,

    created_at DATETIME,

    FOREIGN KEY (incident_id)
        REFERENCES incidents(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    action TEXT NOT NULL,
    entity_type TEXT NOT NULL,
    entity_id TEXT,

    details TEXT,

    created_at DATETIME NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_incidents_status
ON incidents(status);

CREATE INDEX IF NOT EXISTS idx_incidents_severity
ON incidents(severity);

CREATE INDEX IF NOT EXISTS idx_events_incident
ON events(incident_id);

CREATE INDEX IF NOT EXISTS idx_events_eventid
ON events(event_id);

CREATE INDEX IF NOT EXISTS idx_analyses_incident
ON analyses(incident_id);

CREATE INDEX IF NOT EXISTS idx_agent_runs_incident
ON agent_runs(incident_id);

CREATE UNIQUE INDEX IF NOT EXISTS ux_events
ON events(
    incident_id,
    source,
    message
);

CREATE UNIQUE INDEX IF NOT EXISTS ux_analyses
ON analyses(
    incident_id,
    root_cause,
    confidence
);

CREATE INDEX IF NOT EXISTS idx_events_source
ON events(source);

CREATE INDEX IF NOT EXISTS idx_root_cause
ON analyses(root_cause);

CREATE INDEX IF NOT EXISTS idx_incident_created
ON incidents(created_at);