from datetime import datetime
from app.domain.entities.project import Project
from app.domain.entities.project_member import ProjectMember
from app.domain.enums import ProjectRole
from app.application.ports.project_repository import ProjectRepository
from app.application.ports.project_member_repository import ProjectMemberRepository
from app.application.ports.user_repository import UserRepository
from app.domain.exceptions import PersistenceError, ResourceNotFoundError
from app.schemas.project import ProjectCreate

class CreateProjectUseCase:
    def __init__(
        self,
        project_repository: ProjectRepository,
        project_member_repository: ProjectMemberRepository,
        user_repository: UserRepository,
    ):
        self.project_repository = project_repository
        self.project_member_repository = project_member_repository
        self.user_repository = user_repository

    def execute(
        self,
        *,
        project: ProjectCreate,
        created_by: int,
    ) -> Project:
        if not project.name or not project.name.strip():
            raise ValueError("Project name cannot be empty")

        if not self.user_repository.exists(created_by):
            raise ResourceNotFoundError("User")

        # crear proyecto
        project = Project(
            name=project.name.strip(),
            description=project.description,
            created_by=created_by,
            created_at=datetime.now()
        )

        try:
            project = self.project_repository.create(project)

            # agregar creador como manager
            member = ProjectMember(
                project_id=project.id,
                user_id=created_by,
                role=ProjectRole.manager,
            )
            self.project_member_repository.add_member(member)
        except Exception as e:
                raise PersistenceError("Failed to create project")

        return project
