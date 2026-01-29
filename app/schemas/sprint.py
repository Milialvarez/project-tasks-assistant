from datetime import datetime
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