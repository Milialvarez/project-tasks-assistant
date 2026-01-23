from pydantic import BaseModel

from app.infrastructure.db.enums import TaskStatus

class TaskCreate(BaseModel):
    project_id: int
    sprint_id: int | None
    title: str
    description: str | None
    assigned_user_id: int | None
    current_status: TaskStatus | TaskStatus.pending
