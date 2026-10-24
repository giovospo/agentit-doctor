from app.agents.rca_engine import RCAEngine

from app.database.repositories.diagnosis_repository import (
    DiagnosisRepository
)


def test_save_rca_result():

    incident_id = "RCA_TEST_001"

    repo = DiagnosisRepository()

    repo.create_incident(
        incident_id,
        "Critical",
        "RCA Test"
    )

    RCAEngine().run_and_save(
        incident_id,
        [
            "KERNEL_POWER",
            "BUGCHECK"
        ]
    )

    details = repo.get_incident_details(
        incident_id
    )

    assert details is not None

    assert len(
        details["analyses"]
    ) > 0

    repo.close()