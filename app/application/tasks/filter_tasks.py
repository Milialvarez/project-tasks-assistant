from app.application.ports.project_repository import ProjectRepository
from app.application.ports.task_repository import TaskRepository
from app.application.ports.user_repository import UserRepository

class FilterTasksUseCase:
    def __init__(
        self,
        project_repository: ProjectRepository,
        user_repository: UserRepository,
        task_repository: TaskRepository
    ):
        self.project_repository = project_repository
        self.user_repository = user_repository
        self.task_repository = task_repository

    def execute(
        self,
        *,
        project_id: int | None = None,
        sprint_id: int | None = None,
        assigned_user_id: int | None = None,
    ):
        # validar proyecto
        if project_id is not None:
            if not self.project_repository.get_by_id(project_id):
                raise ValueError("Project does not exist")

        # validar usuario
        if assigned_user_id is not None:
            if not self.user_repository.exists(assigned_user_id):
                raise ValueError("User does not exist")

        # validación de sprint comentada hasta que exista
        # if sprint_id is not None:
        #     validar sprint cuando tenga repo

        return self.task_repository.filter(
            project_id=project_id,
            sprint_id=sprint_id,
            assigned_user_id=assigned_user_id,
        )
