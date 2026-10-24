from app.database.repositories.diagnosis_repository import (
    DiagnosisRepository
)

repo = DiagnosisRepository()

repo.save_diagnosis(
    incident_id="INC_20261023_001",
    severity="Critical",
    findings=[
        "KERNEL_POWER",
        "TCPIP",
        "BUGCHECK"
    ],
    root_causes=[
        {
            "component": "Kernel-Power",
            "probability": 85
        },
        {
            "component": "TCPIP Driver",
            "probability": 90
        }
    ],
    recommendation="Review drivers and TCP/IP stack."
)

details = repo.get_incident_details(
    "INC_20261023_001"
)

print(details)

repo.close()