# AgentIT Doctor v0.9.5

## Overview

This release stabilizes and hardens the Evidence Engine persistence layer.

---

## New Features

### Evidence Engine

- Explainable RCA hypotheses
- Evidence collection integrated into RCA workflow
- Evidence persistence in SQLite

### Evidence Repository

- Evidence retrieval by incident
- Evidence retrieval across all incidents
- Duplicate protection via unique constraints

### Dashboard

- RCA Findings enriched with evidence
- Improved diagnosis transparency
- Evidence visualization in Streamlit

---

## Reliability Improvements

- Transaction rollback support
- Safe SQLite handling
- Duplicate evidence protection
- Improved repository robustness

---

## Developer Experience

- Added type hints
- Improved repository implementation
- Expanded automated test coverage

---

## Testing

Automated suite status:

38 tests passing

---

## Release Tags

- v0.9.5