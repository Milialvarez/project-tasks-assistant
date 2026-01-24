from app.infrastructure.db.models.task_status_history import TaskStatusHistory


class UpdateTaskUseCase:
    def __init__(
        self,
        task_repository,
        user_repository,
        project_repository,
        status_history_repository,
    ):
        self.task_repository = task_repository
        self.user_repository = user_repository
        self.project_repository = project_repository
        self.status_history_repository = status_history_repository

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

        is_manager = self.project_repository.is_manager(task.project_id, user_id)
        is_member = self.project_repository.is_member(task.project_id, user_id)

        if not is_manager and not is_member:
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
            task.sprint_id = data.sprint_id

        if data.assigned_user_id is not None:
            task.assigned_user_id = data.assigned_user_id

        if data.archived is not None:
            task.archived = data.archived

        return self.task_repository.update(task)
