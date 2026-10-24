from app.database.repositories.diagnosis_repository import (
    DiagnosisRepository
)

from app.database.repositories.evidence_repository import (
    EvidenceRepository
)


class RCATimelineService:

    def build_timeline(
        self,
        incident_id: str
    ) -> dict:

        diagnosis_repo = DiagnosisRepository()
        evidence_repo = EvidenceRepository()

        try:

            events = (
                diagnosis_repo
                .get_events_by_incident(
                    incident_id
                )
            )

            analyses = (
                diagnosis_repo
                .get_analyses_by_incident(
                    incident_id
                )
            )

            evidence = (
                evidence_repo
                .get_evidence_by_incident(
                    incident_id
                )
            )

            return {
                "incident_id": incident_id,
                "events": events,
                "evidence": evidence,
                "analyses": analyses
            }

        finally:

            evidence_repo.close()
            diagnosis_repo.close()