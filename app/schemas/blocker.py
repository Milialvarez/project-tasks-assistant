from datetime import datetime
from pydantic import BaseModel

from app.domain.enums import BlockerStatus


class TaskBlockerCreate(BaseModel):
    cause: str

class TaskBlockerResponse(BaseModel):
    id: int
    task_id: int
    cause: str
    created_by: int
    status: BlockerStatus
    start_date: datetime
    solved_at: datetime | None = None

    class Config:
        from_attributes = True  

class BlockerUpdate(BaseModel):
    cause: str | None = None
    status: BlockerStatus | None = None