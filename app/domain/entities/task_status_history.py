from datetime import datetime
from app.domain.enums import TaskStatus

class TaskStatusHistory:
    def __init__(
        self,
        *,
        id: int | None = None,
        task_id: int,
        previous_status: TaskStatus,
        new_status: TaskStatus,
        changed_by: int,
        changed_at: datetime | None = None,
    ):
        self.id = id
        self.task_id = task_id
        self.previous_status = previous_status
        self.new_status = new_status
        self.changed_by = changed_by
        self.changed_at = changed_at