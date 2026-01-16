from app.infrastructure.db.models.project import Project
from app.application.ports.project_repository import ProjectRepository
from app.application.ports.user_repository import UserRepository

class CreateProjectUseCase:
    def __init__(
        self,
        project_repository: ProjectRepository,
        user_repository: UserRepository,
    ):
        self.project_repository = project_repository
        self.user_repository = user_repository

    def execute(
        self,
        *,
        name: str,
        description: str | None,
        created_by: int,
    ) -> Project:
        if not name or not name.strip():
            raise ValueError("Project name cannot be empty")

        if not self.user_repository.exists(created_by):
            raise ValueError("Creator user does not exist")

        project = Project(
            name=name.strip(),
            description=description,
            created_by=created_by,
        )

        return self.project_repository.create(project)
