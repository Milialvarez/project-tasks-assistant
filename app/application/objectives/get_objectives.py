from app.application.ports.objective_repository import ObjectiveRepository
from app.application.ports.project_member_repository import ProjectMemberRepository
from app.application.ports.sprint_repository import SprintRepository
from app.domain.exceptions import NotProjectMemberError, ResourceNotFoundError


class GetObjectives:
    def __init__(
            self,
            *,
            objective_repository: ObjectiveRepository,
            sprint_repository: SprintRepository,
            project_member_repository: ProjectMemberRepository
    ):
        self.objective_repository=objective_repository
        self.sprint_repository=sprint_repository
        self.project_member_repository=project_member_repository

    def execute(self,*,project_id: int | None, sprint_id: int | None, user_id: int):
        if project_id:
            if not self.project_member_repository.is_member(project_id=project_id, user_id=user_id):
                raise NotProjectMemberError()
            
        
        if sprint_id:
            sprint = self.sprint_repository.get_by_id(sprint_id=sprint_id)
            if not sprint:
                raise ResourceNotFoundError("Sprint")
            if not self.project_member_repository.is_member(project_id=sprint.project_id, user_id=user_id):
                raise NotProjectMemberError()
            
        return self.objective_repository.get(project_id, sprint_id)