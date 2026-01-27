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
        project_id: int,
        sprint_id: int | None,
        assigned_user_id: int | None,
        current_user_id: int,
    ):
        if not self.project_repository.get_by_id(project_id):
            raise ValueError("Project does not exist")

        if not self.project_member_repository.is_member(project_id, current_user_id):
            raise ValueError("You are not a member of this project")

        if assigned_user_id and not self.user_repository.exists(assigned_user_id):
            raise ValueError("Assigned user does not exist")

        return self.task_repository.filter(
            project_id=project_id,
            sprint_id=sprint_id,
            assigned_user_id=assigned_user_id,
        )
