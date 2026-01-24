class DeleteTaskUseCase:
    def __init__(
        self,
        task_repository,
        project_repository,
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

        self.task_repository.delete(task)
