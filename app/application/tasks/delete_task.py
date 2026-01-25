from app.application.ports.project_repository import ProjectRepository
from app.application.ports.task_repository import TaskRepository


class DeleteTaskUseCase:
    def __init__(
        self,
        task_repository: TaskRepository,
        project_repository: ProjectRepository,
    ):
        self.task_repository = task_repository
        self.project_repository = project_repository

    def execute(self, *, task_id: int, user_id: int):
        task = self.task_repository.get_by_id(task_id)

        if not task:
            raise ValueError("Task not found")

        is_manager = self.project_repository.is_manager(task.project_id, user_id)
        is_member = self.project_repository.is_member(task.project_id, user_id)

        if not is_manager and not is_member:
            raise ValueError("User is not allowed to delete this task")

        try:
            self.task_repository.delete(task)
        except Exception:
                raise RuntimeError("Failed to create sprint")
