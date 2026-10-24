from app.database.repositories.diagnosis_repository import (
    DiagnosisRepository
)

repo = DiagnosisRepository()

incident = repo.get_incident(
    "INC_TEST_001"
)

if incident:
    print(dict(incident))
else:
    print("Incident not found")

repo.close()