from app.application.ports.objective_repository import ObjectiveRepository
from app.application.ports.project_repository import ProjectRepository
from app.application.ports.sprint_repository import SprintRepository
from app.schemas.objective import ObjectiveUpdate


class UpdateObjective:
    def __init__(
            self,
            *,
            objective_repo=ObjectiveRepository,
            project_repo=ProjectRepository,
            sprint_repo=SprintRepository
    ):
        self.objective_repo=objective_repo
        self.project_member_repo=project_repo
        self.sprint_repo=sprint_repo

    def execute(self, objective_data: ObjectiveUpdate, objective_id: int, user_id: int):
        objective = self.objective_repo.get_by_id(objective_id)

        if not objective:
            raise ValueError("Objective with the provided ID doesn't exists")
        
        if not self.project_member_repo.is_manager(project_id=objective.project_id, user_id=user_id):
            raise ValueError("You can't edit this objective because you're not the manager of this project")
        
        if objective_data.title is not None:
            objective.title=objective_data.title

        if objective_data.description is not None:
            objective.description=objective_data.description

        if objective_data.status is not None:
            objective.status=objective_data.status

        sprint = self.sprint_repo.get_by_id(objective_data.sprint_id)
        if sprint is None:
            raise ValueError("Sprint doesn't exists")
        if sprint.project_id != objective.project_id:
            raise ValueError("The sprint provided doesn't belongs to the objective's project")

        objective.sprint_id = sprint.id


        try:
            return self.objective_repo.update(objective=objective)
        except Exception:
            raise RuntimeError("Failed to update objective")