from datetime import datetime

class Decision:
    def __init__(
        self,
        *,
        id: int | None,
        project_id: int,
        task_id: int | None,
        title: str,
        context: str,
        impact: str | None,
        chosen_by: int,
        created_at: datetime | None = None,
    ):
        self.id = id
        self.project_id = project_id
        self.task_id = task_id
        self.title = title
        self.context = context
        self.impact = impact
        self.chosen_by = chosen_by
        self.created_at = created_at
