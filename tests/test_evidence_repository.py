import uuid

from app.database.repositories.diagnosis_repository import (
    DiagnosisRepository
)

from app.database.repositories.evidence_repository import (
    EvidenceRepository
)


def test_create_evidence():

    incident_id = (
        f"INC-{uuid.uuid4()}"
    )

    diagnosis_repo = DiagnosisRepository()

    diagnosis_repo.create_incident(
        incident_id=incident_id,
        severity="HIGH",
        summary="Evidence repository test"
    )

    evidence_repo = EvidenceRepository()

    try:

        evidence_repo.create_evidence(
            incident_id=incident_id,
            root_cause="SYSTEM_CRASH",
            evidence="BUGCHECK"
        )

        assert True

    finally:

        evidence_repo.close()
        diagnosis_repo.close()