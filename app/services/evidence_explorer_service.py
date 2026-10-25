from app.database.repositories.evidence_repository import (
    EvidenceRepository
)


class EvidenceExplorerService:

    def get_all_evidence(self):

        repo = EvidenceRepository()

        try:

            return (
                repo.get_all_evidence()
            )

        finally:

            repo.close()