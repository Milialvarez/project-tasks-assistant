from typing import List
from app.application.ports.project_repository import ProjectRepository
from app.application.ports.user_repository import UserRepository
from app.infrastructure.db.models.project import Project


class GetUserProjectsUseCase:
    def __init__(
        self,
        project_repository: ProjectRepository,
        user_repository: UserRepository,
    ):
        self.project_repository = project_repository
        self.user_repository = user_repository

    
    def execute(self, user_id: int) -> List[Project]:
        # validates user exists
        if not self.user_repository.exists(user_id):
            raise ValueError("User does not exist")

        return self.project_repository.get_projects_for_user(user_id)
