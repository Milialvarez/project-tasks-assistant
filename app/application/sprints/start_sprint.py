from datetime import datetime
from app.application.ports.sprint_repository import SprintRepository
from app.application.ports.project_member_repository import ProjectMemberRepository
from app.domain.enums import SprintStatus
from app.domain.exceptions import NotProjectMemberError, ResourceNotFoundError

class StartSprintUseCase:
    def __init__(
        self,
        sprint_repository: SprintRepository,
        project_member_repository: ProjectMemberRepository,
    ):
        self.sprint_repository = sprint_repository
        self.project_member_repository = project_member_repository

    def execute(self, *, sprint_id: int, user_id: int):
        sprint = self.sprint_repository.get_by_id(sprint_id)

        if not sprint:
            raise ResourceNotFoundError("Sprint")

        if not self.project_member_repository.is_member(sprint.project_id, user_id):
            raise NotProjectMemberError()

        if sprint.started_at is not None:
            raise ValueError("Sprint already started")

        sprint.started_at = datetime.utcnow()
        sprint.status = SprintStatus.active

        return self.sprint_repository.update(sprint)
