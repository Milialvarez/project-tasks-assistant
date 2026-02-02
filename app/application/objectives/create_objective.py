from app.application.ports.objective_repository import ObjectiveRepository
from app.application.ports.project_repository import ProjectRepository
from app.application.ports.sprint_repository import SprintRepository
from app.domain.entities.objective import Objective
from app.domain.enums import ObjectiveStatus
from app.schemas.objective import ObjectiveCreate


class CreateObjective:
    def __init__(
            self,
            *,
            objective_repo: ObjectiveRepository,
            sprint_repo: SprintRepository,
            project_repo: ProjectRepository
    ):
        self.objective_repo=objective_repo
        self.sprint_repo=sprint_repo
        self.project_member_repo=project_repo

    def execute(self, objective: ObjectiveCreate, user_id: int):
        if not self.project_member_repo.is_manager(objective.project_id, user_id):
            raise ValueError("You can't create an objective for this project because you're not the manager")
        
        if objective.sprint_id:
            if not self.sprint_repo.get_by_id(objective.sprint_id):
                raise ValueError("Sprint does not exist")
            
        domain_objective = Objective(
            id=None, 
            project_id=objective.project_id, 
            sprint_id=objective.sprint_id, 
            title=objective.title, 
            description=objective.description, 
            status=ObjectiveStatus.pending)
        
        try:
            return self.objective_repo.create(domain_objective)
        except Exception:
            raise RuntimeError("Failed to create objective")