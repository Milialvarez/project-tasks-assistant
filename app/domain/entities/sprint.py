from datetime import datetime
from app.domain.enums import SprintStatus

class Sprint:
    def __init__(
        self,
        *,
        id: int | None = None,
        project_id: int,
        name: str,
        description: str | None,
        started_at: datetime | None,
        ended_at: datetime | None,
        status: SprintStatus,
    ):
        self.id = id
        self.project_id = project_id
        self.name = name
        self.description = description
        self.started_at = started_at
        self.ended_at = ended_at
        self.status = status
