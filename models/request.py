from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class IncidentRequest(BaseModel):

    model_config = ConfigDict(
        extra="forbid"
    )

    incident_id: str = Field(
        min_length=3,
        max_length=50
    )

    hostname: str

    os: str

    symptoms: list[str]

    driver: Optional[str] = None
    