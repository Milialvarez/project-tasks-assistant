from app.application.ports.objective_repository import ObjectiveRepository
from app.application.ports.project_repository import ProjectRepository


class DeleteObjective:
    def __init__(
            self,
            *,
            objective_repo=ObjectiveRepository,
            project_repo=ProjectRepository
    ):
        self.objective_repo=objective_repo
        self.project_repo=project_repo

    def execute(self, objective_id: int, user_id: int):
        objective = self.objective_repo.get_by_id(objective_id=objective_id)

        if not objective:
            raise ValueError("Objective not found")

        if not self.project_repo.is_manager(objective.project_id, user_id):
            raise ValueError("You can't delete this objective because you're not the manager of this project")

        try:
            self.objective_repo.delete(objective_id)
        except Exception:
            raise RuntimeError("Failed to delete the objective")