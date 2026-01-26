from app.application.ports.project_member_repository import ProjectMemberRepository
from app.application.ports.project_repository import ProjectRepository
from app.application.ports.sprint_repository import SprintRepository
from app.application.ports.task_repository import TaskRepository
from app.application.ports.task_status_history_repository import TaskStatusHistoryRepository
from app.application.ports.user_repository import UserRepository
from app.infrastructure.db.models.task_status_history import TaskStatusHistory

class UpdateTaskUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        task_repository: TaskRepository,
        status_history_repository: TaskStatusHistoryRepository,
        sprint_repository: SprintRepository,
        project_member_repository: ProjectMemberRepository
    ):
        self.task_repository = task_repository
        self.user_repository = user_repository
        self.status_history_repository = status_history_repository
        self.sprint_repository = sprint_repository
        self.project_member_repository = project_member_repository

    def execute(
        self,
        *,
        task_id: int,
        user_id: int,
        data,
    ):
        task = self.task_repository.get_by_id(task_id)

        if not task:
            raise ValueError("Task not found")

        if not self.project_member_repository.is_member(task.project_id, user_id):
            raise ValueError("User is not a member of the project")

        if data.assigned_user_id is not None:
            if not self.user_repository.exists(data.assigned_user_id):
                raise ValueError("Assigned user does not exist")

        if data.current_status and data.current_status != task.current_status:
            history = TaskStatusHistory(
                task_id=task.id,
                previous_status=task.current_status,
                new_status=data.current_status,
                changed_by=user_id,
            )
            self.status_history_repository.create(history)
            task.current_status = data.current_status

        if data.title is not None:
            if not data.title.strip():
                raise ValueError("Title cannot be empty")
            task.title = data.title.strip()

        if data.description is not None:
            task.description = data.description

        if data.sprint_id is not None:
            sprint = self.sprint_repository.get_by_id(data.sprint_id)
            if not sprint:
                raise ValueError("The sprint doesn't exists")
            task.sprint_id = data.sprint_id

        if data.assigned_user_id is not None:
            task.assigned_user_id = data.assigned_user_id

        if data.archived is not None:
            task.archived = data.archived

        try:
            return self.task_repository.update(task)
        except Exception:
                raise RuntimeError("Failed to create sprint")
