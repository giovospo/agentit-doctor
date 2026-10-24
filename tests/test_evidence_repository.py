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
        summary="Evidence test"
    )

    evidence_repo = EvidenceRepository()

    evidence_repo.create_evidence(
        incident_id=incident_id,
        root_cause="SYSTEM_CRASH",
        evidence="BUGCHECK"
    )

    evidence = (
        evidence_repo.get_evidence_by_incident(
            incident_id
        )
    )

    assert len(evidence) >= 1

    evidence_repo.close()
    diagnosis_repo.close()


def test_duplicate_evidence_is_ignored():

    incident_id = (
        f"INC-{uuid.uuid4()}"
    )

    diagnosis_repo = DiagnosisRepository()

    diagnosis_repo.create_incident(
        incident_id=incident_id,
        severity="HIGH",
        summary="Duplicate evidence test"
    )

    evidence_repo = EvidenceRepository()

    evidence_repo.create_evidence(
        incident_id,
        "SYSTEM_CRASH",
        "BUGCHECK"
    )

    evidence_repo.create_evidence(
        incident_id,
        "SYSTEM_CRASH",
        "BUGCHECK"
    )

    evidence = (
        evidence_repo.get_evidence_by_incident(
            incident_id
        )
    )

    assert len(evidence) == 1

    evidence_repo.close()
    diagnosis_repo.close()