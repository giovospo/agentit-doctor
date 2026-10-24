from app.database.repositories.diagnosis_repository import (
    DiagnosisRepository
)

repo = DiagnosisRepository()

data = repo.get_incident_details(
    "INC_20261023_001"
)

print(data)

repo.close()