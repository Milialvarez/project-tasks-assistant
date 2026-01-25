from app.application.ports.project_repository import ProjectRepository
from app.application.ports.sprint_repository import SprintRepository
from app.application.ports.user_repository import UserRepository
from app.infrastructure.db.models.sprint import Sprint
from app.schemas.sprint import SprintCreate


class CreateSprintUseCase:
    def __init__(
        self,
        sprint_repo: SprintRepository,
        project_repo: ProjectRepository,
        user_repo: UserRepository,
    ):
        self.sprint_repo = sprint_repo
        self.project_repo = project_repo
        self.user_repo = user_repo

    def execute(
            self,
            *,
            sprint: SprintCreate,
            user_id: int
        ) -> Sprint:
            if not self.user_repo.exists(user_id):
                raise ValueError("User does not exist")

            if not self.project_repo.is_manager(sprint.project_id, user_id):
                raise ValueError("User is not project manager")

            sprint_entity = Sprint(
                project_id=sprint.project_id,
                name=sprint.name,
                description=sprint.description,
                started_at=sprint.started_at,
                status=sprint.status,
            )

            try:
                return self.sprint_repo.create(sprint_entity)
            except Exception:
                raise RuntimeError("Failed to create sprint")
