from app.application.ports.objective_repository import ObjectiveRepository
from app.application.ports.project_repository import ProjectRepository
from app.application.ports.sprint_repository import SprintRepository
from app.domain.exceptions import InvalidOperationError, NotProjectManagerError, PersistenceError, ResourceNotFoundError
from app.schemas.objective import ObjectiveUpdate


class UpdateObjective:
    def __init__(
            self,
            *,
            objective_repository=ObjectiveRepository,
            project_repository=ProjectRepository,
            sprint_repository=SprintRepository
    ):
        self.objective_repository=objective_repository
        self.project_member_repository=project_repository
        self.sprint_repository=sprint_repository

    def execute(self, objective_data: ObjectiveUpdate, objective_id: int, user_id: int):
        objective = self.objective_repository.get_by_id(objective_id)

        if not objective:
            raise ResourceNotFoundError("Objective")
        
        if not self.project_member_repository.is_manager(project_id=objective.project_id, user_id=user_id):
            raise NotProjectManagerError()
        
        if objective_data.title is not None:
            objective.title=objective_data.title

        if objective_data.description is not None:
            objective.description=objective_data.description

        if objective_data.status is not None:
            objective.status=objective_data.status

        sprint = self.sprint_repository.get_by_id(objective_data.sprint_id)
        if sprint is None:
            raise ResourceNotFoundError("Sprint")
        if sprint.project_id != objective.project_id:
            raise InvalidOperationError(
                    "The sprint does not belong to the objective's project"
                )

        objective.sprint_id = sprint.id


        try:
            return self.objective_repository.update(objective=objective)
        except Exception as e:
            raise PersistenceError("Failed to update objective") from e