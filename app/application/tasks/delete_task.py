from app.application.ports.project_member_repository import ProjectMemberRepository
from app.application.ports.task_repository import TaskRepository


class DeleteTaskUseCase:
    def __init__(
        self,
        task_repository: TaskRepository,
        project_member_repository: ProjectMemberRepository,
    ):
        self.task_repository = task_repository
        self.project_member_repository = project_member_repository

    def execute(self, *, task_id: int, user_id: int):
        task = self.task_repository.get_by_id(task_id)

        if not task:
            raise ValueError("Task not found")

        if not self.project_member_repository.is_member(task.project_id, user_id):
            raise ValueError("User is not allowed to delete this task")

        self.task_repository.delete(task_id)
