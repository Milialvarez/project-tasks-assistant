from app.application.ports.project_member_repository import ProjectMemberRepository
from app.application.ports.project_repository import ProjectRepository
from app.application.ports.sprint_repository import SprintRepository
from app.application.ports.user_repository import UserRepository
from app.domain.exceptions import NotProjectMemberError, ResourceNotFoundError


class GetProjectSprints:
    def __init__(
            self,
            sprint_repo: SprintRepository,
            project_repo: ProjectRepository,
            user_repo: UserRepository,
            project_member_repo: ProjectMemberRepository
        ):
        self.sprint_repo=sprint_repo
        self.user_repo=user_repo
        self.project_repo=project_repo
        self.project_member_repo=project_member_repo

    def execute(self,*, project_id: int, user_id: int):
        if not self.user_repo.exists(user_id):
                raise ResourceNotFoundError("User")
        if not self.project_repo.get_by_id(project_id):
             raise ResourceNotFoundError("Project")
        if not self.project_member_repo.is_member(project_id=project_id, user_id=user_id):
             raise NotProjectMemberError()
        
        return self.sprint_repo.get_sprints_by_project_id(project_id)
