from app.application.ports.objective_repository import ObjectiveRepository
from app.application.ports.project_repository import ProjectRepository
from app.domain.exceptions import NotProjectManagerError, PersistenceError, ResourceNotFoundError


class DeleteObjective:
    def __init__(
            self,
            *,
            objective_repository=ObjectiveRepository,
            project_repository=ProjectRepository
    ):
        self.objective_repository=objective_repository
        self.project_repository=project_repository

    def execute(self, objective_id: int, user_id: int):
        objective = self.objective_repository.get_by_id(objective_id=objective_id)

        if not objective:
            raise ResourceNotFoundError("Objective")

        if not self.project_repository.is_manager(objective.project_id, user_id):
            raise NotProjectManagerError()

        try:
            self.objective_repository.delete(objective_id)
        except Exception as e:
            raise PersistenceError("Failed to delete the objective") from e