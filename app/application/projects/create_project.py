from app.infrastructure.db.models.project import Project
from app.infrastructure.db.models.project_member import ProjectMember
from app.infrastructure.db.enums import ProjectRole
from app.application.ports.project_repository import ProjectRepository
from app.application.ports.project_member_repository import ProjectMemberRepository
from app.application.ports.user_repository import UserRepository

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
        name: str,
        description: str | None,
        created_by: int,
    ) -> Project:
        if not name or not name.strip():
            raise ValueError("Project name cannot be empty")

        if not self.user_repository.exists(created_by):
            raise ValueError("Creator user does not exist")

        # crear proyecto
        project = Project(
            name=name.strip(),
            description=description,
            created_by=created_by,
        )
        project = self.project_repository.create(project)

        # agregar creador como manager
        member = ProjectMember(
            project_id=project.id,
            user_id=created_by,
            role=ProjectRole.manager,
        )
        self.project_member_repository.add_member(member)

        return project
