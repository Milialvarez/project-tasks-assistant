from app.application.ports.project_member_repository import ProjectMemberRepository
from app.application.ports.project_repository import ProjectRepository
from app.application.ports.task_repository import TaskRepository
from app.application.ports.user_repository import UserRepository

class FilterTasksUseCase:
    def __init__(
        self,
        project_repository: ProjectRepository,
        project_member_repository: ProjectMemberRepository,
        user_repository: UserRepository,
        task_repository: TaskRepository,
    ):
        self.project_repository = project_repository
        self.project_member_repository = project_member_repository
        self.user_repository = user_repository
        self.task_repository = task_repository

    def execute(
        self,
        *,
        project_id: int | None,
        sprint_id: int | None,
        assigned_user_id: int | None,
        current_user_id: int,
    ):
        # NO SE PUEDE FILTRAR SIN PROYECTO
        if project_id is None:
            raise ValueError("project_id is required to filter tasks")

        project = self.project_repository.get_by_id(project_id)
        if not project:
            raise ValueError("Project does not exist")

        # VALIDAR QUE EL USUARIO PERTENECE AL PROYECTO

        if not self.project_repository.is_member(project_id, current_user_id):
            raise ValueError("You can't filter the tasks because you are not a member of this project")

        # validar usuario asignado si viene
        if assigned_user_id is not None:
            if not self.user_repository.exists(assigned_user_id):
                raise ValueError("Assigned user does not exist")

        # sprint se valida cuando exista repo
        # if sprint_id is not None:
        #     validar sprint

        return self.task_repository.filter(
            project_id=project_id,
            sprint_id=sprint_id,
            assigned_user_id=assigned_user_id,
        )
