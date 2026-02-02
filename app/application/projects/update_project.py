from app.application.ports.project_repository import ProjectRepository
from app.domain.exceptions import NotProjectManagerError, PersistenceError, ResourceNotFoundError
from app.schemas.project import ProjectUpdate

class UpdateProjectUseCase:
    def __init__(self, project_repository: ProjectRepository):
        self.project_repository = project_repository

    def execute(
        self,
        *,
        project_id: int,
        project_data: ProjectUpdate,
        user_id: int,
    ):
        project = self.project_repository.get_by_id(project_id=project_id)

        if not project:
            raise ResourceNotFoundError("Project")

        if not self.project_repository.is_manager(project_id=project_id, user_id=user_id):
            raise NotProjectManagerError()

        if project_data.name is not None:
            if not project_data.name.strip():
                raise ValueError("Project name cannot be empty")
            project.name = project_data.name.strip()

        if project_data.description is not None:
            project.description = project_data.description

        try:
            return self.project_repository.update(project)
        except Exception as e:
                raise PersistenceError("Failed to update project") from e
