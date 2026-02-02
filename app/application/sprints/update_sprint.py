from app.application.ports.project_member_repository import ProjectMemberRepository
from app.application.ports.sprint_repository import SprintRepository
from app.application.ports.user_repository import UserRepository
from app.domain.enums import SprintStatus
from app.domain.exceptions import NotProjectMemberError, PersistenceError, ResourceNotFoundError
from app.schemas.sprint import SprintUpdate


class UpdateSprintUseCase:
    def __init__(
        self,
        sprint_repo: SprintRepository,
        project_member_repo: ProjectMemberRepository,
        user_repo: UserRepository,
    ):
        self.sprint_repo = sprint_repo
        self.project_member_repo = project_member_repo
        self.user_repo = user_repo

    def execute(
        self,
        *,
        sprint_data: SprintUpdate,
        user_id: int,
    ):
        sprint = self.sprint_repo.get_by_id(sprint_data.sprint_id)

        if not sprint:
            raise ResourceNotFoundError("Sprint")

        if not self.project_member_repo.is_member(sprint.project_id, user_id):
            raise NotProjectMemberError()


        if sprint_data.name is not None and sprint_data.name.strip():
            sprint.name = sprint_data.name.strip()

        if sprint_data.description is not None:
            sprint.description = sprint_data.description
        
        if sprint_data.ended_at:
            if sprint.started_at and sprint_data.ended_at <= sprint.started_at:
                raise ValueError("Ending date can't be before starting date")
            sprint.ended_at = sprint_data.ended_at
            sprint.status = SprintStatus.completed

        try:
            return self.sprint_repo.update(sprint)
        except Exception as e:
                raise PersistenceError("Failed to update project") from e

