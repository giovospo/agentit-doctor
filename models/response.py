from pydantic import BaseModel, Field


class RootCause(BaseModel):

    component: str

    probability: float = Field(
        ge=0,
        le=100
    )


class DiagnosisResult(BaseModel):

    severity: str

    diagnosis: str

    evidence: list[str]

    root_causes: list[RootCause]

    recommendations: list[str]
