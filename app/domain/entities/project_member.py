# domain/entities/project_member.py
from datetime import datetime
from app.domain.enums import ProjectRole

class ProjectMember:
    def __init__(
        self,
        *,
        id: int | None,
        project_id: int,
        user_id: int,
        role: ProjectRole,
        joined_at: datetime | None = None,
    ):
        self.id = id
        self.project_id = project_id
        self.user_id = user_id
        self.role = role
        self.joined_at = joined_at
