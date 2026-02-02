from app.application.ports.objective_repository import ObjectiveRepository
from app.application.ports.project_member_repository import ProjectMemberRepository
from app.application.ports.sprint_repository import SprintRepository
from app.domain.exceptions import NotProjectMemberError, ResourceNotFoundError


class GetObjectives:
    def __init__(
            self,
            *,
            objective_repo: ObjectiveRepository,
            sprint_repo: SprintRepository,
            project_member_repo: ProjectMemberRepository
    ):
        self.objective_repo=objective_repo
        self.sprint_repo=sprint_repo
        self.project_member_repo=project_member_repo

    def execute(self,*,project_id: int | None, sprint_id: int | None, user_id: int):
        if project_id:
            if not self.project_member_repo.is_member(project_id=project_id, user_id=user_id):
                raise NotProjectMemberError()
            
        
        if sprint_id:
            sprint = self.sprint_repo.get_by_id(sprint_id=sprint_id)
            if not sprint:
                raise ResourceNotFoundError("Sprint")
            if not self.project_member_repo.is_member(project_id=sprint.project_id, user_id=user_id):
                raise NotProjectMemberError()
            
        return self.objective_repo.get(project_id, sprint_id)