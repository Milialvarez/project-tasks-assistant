from app.application.ports.project_repository import ProjectRepository

class DeleteProjectUseCase:
    def __init__(self, project_repository: ProjectRepository):
        self.project_repository = project_repository

    def execute(self, *, project_id: int, user_id: int):
        project = self.project_repository.get_by_id(project_id)

        if not project:
            raise ValueError("Project not found")

        if project.created_by != user_id:
            raise ValueError("You cannot delete this project because you're not the creator")

        self.project_repository.delete(project)
