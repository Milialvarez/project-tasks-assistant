from app.application.ports.objective_repository import ObjectiveRepository
from app.application.ports.project_repository import ProjectRepository
from app.application.ports.sprint_repository import SprintRepository
from app.domain.entities.objective import Objective
from app.domain.enums import ObjectiveStatus
from app.domain.exceptions import NotProjectManagerError, PersistenceError, ResourceNotFoundError
from app.schemas.objective import ObjectiveCreate


class CreateObjective:
    def __init__(
            self,
            *,
            objective_repository: ObjectiveRepository,
            sprint_repository: SprintRepository,
            project_repository: ProjectRepository
    ):
        self.objective_repository=objective_repository
        self.sprint_repository=sprint_repository
        self.project_member_repository=project_repository

    def execute(self, objective: ObjectiveCreate, user_id: int):
        if not self.project_member_repository.is_manager(objective.project_id, user_id):
            raise NotProjectManagerError()
        
        if objective.sprint_id:
            if not self.sprint_repository.get_by_id(objective.sprint_id):
                raise ResourceNotFoundError("Sprint")
            
        domain_objective = Objective(
            id=None, 
            project_id=objective.project_id, 
            sprint_id=objective.sprint_id, 
            title=objective.title, 
            description=objective.description, 
            status=ObjectiveStatus.pending)
        
        try:
            return self.objective_repository.create(domain_objective)
        except Exception as e:
            raise PersistenceError("Failed to create objective") from e