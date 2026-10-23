from app.database.connection import get_connection
from app.database.repositories.diagnosis_repository import (
    DiagnosisRepository
)


def test_database_connection():

    conn = get_connection()

    assert conn is not None

    conn.close()


def test_create_incident():

    repo = DiagnosisRepository()

    repo.create_incident(
        "TEST_INCIDENT",
        "Critical",
        "Pytest Incident"
    )

    incident = repo.get_incident(
        "TEST_INCIDENT"
    )

    assert incident is not None
    assert incident["id"] == "TEST_INCIDENT"

    repo.close()


def test_create_event():

    repo = DiagnosisRepository()

    repo.create_event(
        "TEST_INCIDENT",
        "TCPIP",
        "Critical",
        "TCPIP Driver Error"
    )

    repo.cursor.execute(
        """
        SELECT COUNT(*)
        FROM events
        WHERE incident_id = ?
        """,
        ("TEST_INCIDENT",)
    )

    count = repo.cursor.fetchone()[0]

    assert count > 0

    repo.close()


def test_create_analysis():

    repo = DiagnosisRepository()

    repo.create_analysis(
        "TEST_INCIDENT",
        "TCPIP Driver",
        90
    )

    repo.cursor.execute(
        """
        SELECT COUNT(*)
        FROM analyses
        WHERE incident_id = ?
        """,
        ("TEST_INCIDENT",)
    )

    count = repo.cursor.fetchone()[0]

    assert count > 0

    repo.close()


def test_save_diagnosis():

    repo = DiagnosisRepository()

    repo.save_diagnosis(
        incident_id="TEST_SAVE",
        severity="Critical",
        findings=[
            "KERNEL_POWER",
            "TCPIP"
        ],
        root_causes=[
            {
                "component": "Kernel Power",
                "probability": 85
            }
        ],
        recommendation="Review drivers"
    )

    details = repo.get_incident_details(
        "TEST_SAVE"
    )

    assert details is not None
    assert len(details["events"]) == 2
    assert len(details["analyses"]) == 1

    repo.close()