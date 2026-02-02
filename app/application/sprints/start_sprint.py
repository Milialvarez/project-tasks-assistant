from datetime import datetime
from app.application.ports.sprint_repository import SprintRepository
from app.application.ports.project_member_repository import ProjectMemberRepository
from app.domain.enums import SprintStatus
from app.domain.exceptions import NotProjectMemberError, ResourceNotFoundError

class StartSprintUseCase:
    def __init__(
        self,
        sprint_repo: SprintRepository,
        project_member_repo: ProjectMemberRepository,
    ):
        self.sprint_repo = sprint_repo
        self.project_member_repo = project_member_repo

    def execute(self, *, sprint_id: int, user_id: int):
        sprint = self.sprint_repo.get_by_id(sprint_id)

        if not sprint:
            raise ResourceNotFoundError("Sprint")

        if not self.project_member_repo.is_member(sprint.project_id, user_id):
            raise NotProjectMemberError()

        if sprint.started_at is not None:
            raise ValueError("Sprint already started")

        sprint.started_at = datetime.utcnow()
        sprint.status = SprintStatus.active

        return self.sprint_repo.update(sprint)
