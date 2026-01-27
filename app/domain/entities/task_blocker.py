from datetime import datetime
from app.domain.enums import BlockerStatus

class TaskBlocker:
    def __init__(
        self,
        *,
        id: int | None,
        task_id: int,
        cause: str,
        created_by: int,
        status: BlockerStatus,
        start_date: datetime,
        solved_at: datetime | None,
    ):
        self.id = id
        self.task_id = task_id
        self.cause = cause
        self.created_by = created_by
        self.status = status
        self.start_date = start_date
        self.solved_at = solved_at
