from app.application.ports.project_repository import ProjectRepository

class UpdateProjectUseCase:
    def __init__(self, project_repository: ProjectRepository):
        self.project_repository = project_repository

    def execute(
        self,
        *,
        project_id: int,
        user_id: int,
        name: str | None,
        description: str | None,
    ):
        project = self.project_repository.get_by_id(project_id)

        if not project:
            raise ValueError("Project not found")

        if project.created_by != user_id:
            raise ValueError("You cannot modify this project because you're not the creator")

        if name is not None:
            if not name.strip():
                raise ValueError("Project name cannot be empty")
            project.name = name.strip()

        if description is not None:
            project.description = description

        return self.project_repository.create(project)
