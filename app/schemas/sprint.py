from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from app.domain.enums import SprintStatus


class SprintCreate(BaseModel):
    project_id: int
    name: str
    description: str | None

class SprintUpdate(BaseModel):
    sprint_id: int
    name: str | None
    description: str | None = None
    ended_at: datetime | None = None

class SprintResponse(BaseModel):
    id: int
    project_id: int
    name: str
    description: Optional[str]
    started_at: Optional[datetime]
    ended_at: Optional[datetime]
    status: SprintStatus

    class Config:
        from_attributes = True  