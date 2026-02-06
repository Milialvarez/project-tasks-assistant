from app.application.ports.project_member_repository import ProjectMemberRepository
from app.application.ports.project_repository import ProjectRepository
from app.application.ports.sprint_repository import SprintRepository
from app.application.ports.user_repository import UserRepository
from app.domain.exceptions import NotProjectMemberError, ResourceNotFoundError


class GetProjectSprints:
    def __init__(
            self,
            sprint_repository: SprintRepository,
            project_repository: ProjectRepository,
            user_repository: UserRepository,
            project_member_repository: ProjectMemberRepository
        ):
        self.sprint_repository=sprint_repository
        self.user_repository=user_repository
        self.project_repository=project_repository
        self.project_member_repository=project_member_repository

    def execute(self,*, project_id: int, user_id: int):
        if not self.user_repository.exists(user_id):
                raise ResourceNotFoundError("User")
        if not self.project_repository.get_by_id(project_id):
             raise ResourceNotFoundError("Project")
        if not self.project_member_repository.is_member(project_id=project_id, user_id=user_id):
             raise NotProjectMemberError()
        
        return self.sprint_repository.get_sprints_by_project_id(project_id)
