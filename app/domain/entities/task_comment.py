from datetime import datetime

class TaskComment:
    def __init__(
        self,
        *,
       id: int | None = None,
        task_id: int,
        user_id: int,
        content: str,
        created_at: datetime | None = None,
    ):
        self.id = id
        self.task_id = task_id
        self.user_id = user_id
        self.content = content
        self.created_at = created_at
