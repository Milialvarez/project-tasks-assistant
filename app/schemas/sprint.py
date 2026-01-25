from datetime import datetime
from pydantic import BaseModel

from app.infrastructure.db.enums import SprintStatus


class SprintCreate(BaseModel):
    project_id: int
    name: str
    description: str | None
    started_at: datetime | None
    status: SprintStatus = SprintStatus.planned
