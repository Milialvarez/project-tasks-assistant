from app.application.ports.project_repository import ProjectRepository
from app.application.ports.sprint_repository import SprintRepository
from app.application.ports.user_repository import UserRepository
from app.domain.entities.sprint import Sprint
from app.domain.enums import SprintStatus
from app.domain.exceptions import NotProjectManagerError, PersistenceError, ResourceNotFoundError
from app.schemas.sprint import SprintCreate


class CreateSprintUseCase:
    def __init__(
        self,
        sprint_repository: SprintRepository,
        project_repository: ProjectRepository,
        user_repository: UserRepository,
    ):
        self.sprint_repository = sprint_repository
        self.project_repository = project_repository
        self.user_repository = user_repository

    def execute(
            self,
            *,
            sprint: SprintCreate,
            user_id: int
        ) -> Sprint:
            if not self.user_repository.exists(user_id):
                raise ResourceNotFoundError("User")

            if not self.project_repository.is_manager(sprint.project_id, user_id):
                raise NotProjectManagerError()

            sprint_entity = Sprint(
                project_id=sprint.project_id,
                name=sprint.name,
                description=sprint.description,
                started_at=None,
                ended_at=None,
                status=SprintStatus.planned,
            )

            try:
                return self.sprint_repository.create(sprint_entity)
            except Exception as e:
                raise PersistenceError("Failed to create sprint") from e
