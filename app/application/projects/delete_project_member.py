from app.application.ports.project_member_repository import ProjectMemberRepository
from app.application.ports.project_repository import ProjectRepository
from app.domain.exceptions import NotProjectManagerError, NotProjectMemberError, PersistenceError, ResourceNotFoundError


class DeleteProjectMember:
    def __init__(
            self,
            *,
            project_repo: ProjectRepository,
            project_member_repo: ProjectMemberRepository
    ):
        self.project_repo=project_repo
        self.project_member_repo=project_member_repo

    def execute(self, project_id: int, user_id: int, current_user_id: int):
        if not self.project_repo.get_by_id(project_id):
            raise ResourceNotFoundError("Project")
        
        if not self.project_repo.is_manager(project_id, current_user_id):
            raise NotProjectManagerError()
        
        if not self.project_member_repo.is_member(project_id, user_id):
            raise NotProjectMemberError()
        
        try:
            self.project_member_repo.delete(project_id, user_id)
        except Exception as e:
                raise PersistenceError("Failed to delete project member")