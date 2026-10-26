from app.agents.rca_engine import RCAEngine

from app.database.repositories.diagnosis_repository import (
    DiagnosisRepository
)


def test_rca_from_incident():

    incident_id = "RCA_AUTO_001"

    repo = DiagnosisRepository()

    repo.create_incident(
        incident_id,
        "Critical",
        "Auto RCA"
    )

    repo.create_event(
        incident_id,
        "KERNEL_POWER",
        "Critical",
        "Power event"
    )

    repo.create_event(
        incident_id,
        "BUGCHECK",
        "Critical",
        "Bugcheck event"
    )

    result = (
        RCAEngine()
        .run_from_incident(
            incident_id
        )
    )

    assert len(result) > 0

    assert (
        result[0]["root_cause"]
        ==
        "SYSTEM_CRASH"
    )

    repo.close()