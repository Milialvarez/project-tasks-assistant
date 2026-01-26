from app.application.ports.project_member_repository import ProjectMemberRepository
from app.application.ports.project_repository import ProjectRepository
from app.application.ports.sprint_repository import SprintRepository
from app.application.ports.task_repository import TaskRepository
from app.application.ports.user_repository import UserRepository
from app.schemas.task import TaskCreate
from app.infrastructure.db.models.task import Task


class CreateTaskUseCase:
    def __init__(
        self,
        project_repository: ProjectRepository,
        sprint_repository: SprintRepository,
        user_repository: UserRepository,
        task_repository: TaskRepository,
        project_member_repository: ProjectMemberRepository
    ):
        self.project_repository = project_repository
        self.sprint_repository = sprint_repository
        self.user_repository = user_repository
        self.task_repository = task_repository
        self.project_member_repository = project_member_repository

    def execute(self, *, task: TaskCreate) -> Task:
        # Validates project exists
        project = self.project_repository.get_by_id(task.project_id)
        if not project:
            raise ValueError("A task must belong to an existing project")

        # Validate (if comes) assigned user exists
        if task.assigned_user_id:
            user = self.user_repository.get_by_id(task.assigned_user_id)
            if not user:
                raise ValueError("Assigned user does not exist")
            if not self.project_member_repository.is_member(task.project_id, task.assigned_user_id):
                raise ValueError("A task can't be assigned to a not member of the project")

        # Validate (if comes) sprint exists
        if task.sprint_id:
            sprint = self.sprint_repository.get_by_id(task.sprint_id)
            if not sprint:
                raise ValueError("The sprint doesn't exists")

        new_task = Task(
            project_id=task.project_id,
            sprint_id=task.sprint_id,
            title=task.title,
            description=task.description,
            assigned_user_id=task.assigned_user_id,
            current_status=task.current_status,
        )

        # Persist the task in the db
        try:
            return self.task_repository.create(new_task)
        except Exception:
                raise RuntimeError("Failed to create the task")
