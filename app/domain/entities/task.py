# domain/entities/task.py
from datetime import datetime
from app.domain.enums import TaskStatus

class Task:
    def __init__(
        self,
        *,
        id: int | None,
        project_id: int,
        sprint_id: int | None,
        title: str,
        description: str | None,
        assigned_user_id: int | None,
        current_status: TaskStatus,
        created_at: datetime | None = None,
        archived: bool = False,
    ):
        self.id = id
        self.project_id = project_id
        self.sprint_id = sprint_id
        self.title = title
        self.description = description
        self.assigned_user_id = assigned_user_id
        self.current_status = current_status
        self.created_at = created_at
        self.archived = archived
