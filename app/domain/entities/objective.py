from app.domain.enums import ObjectiveStatus

class Objective:
    def __init__(
        self,
        *,
        id: int | None,
        project_id: int,
        sprint_id: int | None,
        title: str,
        description: str | None,
        status: ObjectiveStatus,
    ):
        self.id = id
        self.project_id = project_id
        self.sprint_id = sprint_id
        self.title = title
        self.description = description
        self.status = status
