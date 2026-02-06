from app.application.ports.project_repository import ProjectRepository
from app.domain.exceptions import NotProjectManagerError, PersistenceError, ResourceNotFoundError

class DeleteProjectUseCase:
    def __init__(
              self, 
              *,
              project_repository: ProjectRepository
              ):
                self.project_repository = project_repository

    def execute(self, *, project_id: int, user_id: int):
        project = self.project_repository.get_by_id(project_id)

        if not project:
            raise ResourceNotFoundError("Project")

        if not self.project_repository.is_manager(project_id, user_id):
            raise NotProjectManagerError()

        try:
            self.project_repository.delete(project)
        except Exception as e:
                raise PersistenceError("Failed to delete project")
