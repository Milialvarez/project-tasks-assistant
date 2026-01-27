from datetime import datetime
from app.application.ports.project_member_repository import ProjectMemberRepository
from app.application.ports.project_repository import ProjectRepository
from app.application.ports.sprint_repository import SprintRepository
from app.application.ports.task_repository import TaskRepository
from app.application.ports.user_repository import UserRepository
from app.domain.entities.task import Task
from app.schemas.task import TaskCreate


class CreateTaskUseCase:
    def __init__(
        self,
        project_repository: ProjectRepository,
        sprint_repository: SprintRepository,
        user_repository: UserRepository,
        task_repository: TaskRepository,
        project_member_repository: ProjectMemberRepository,
    ):
        self.project_repository = project_repository
        self.sprint_repository = sprint_repository
        self.user_repository = user_repository
        self.task_repository = task_repository
        self.project_member_repository = project_member_repository

    def execute(self, *, task: TaskCreate) -> Task:
        # project exists
        if not self.project_repository.get_by_id(task.project_id):
            raise ValueError("A task must belong to an existing project")

        # assigned user
        if task.assigned_user_id:
            user = self.user_repository.get_by_id(task.assigned_user_id)
            if not user:
                raise ValueError("Assigned user does not exist")

            if not self.project_member_repository.is_member(
                task.project_id, task.assigned_user_id
            ):
                raise ValueError("User is not member of the project")

        # sprint exists
        if task.sprint_id:
            if not self.sprint_repository.get_by_id(task.sprint_id):
                raise ValueError("Sprint does not exist")

        domain_task = Task(
            id=None,
            project_id=task.project_id,
            sprint_id=task.sprint_id,
            title=task.title.strip(),
            description=task.description,
            assigned_user_id=task.assigned_user_id,
            current_status=task.current_status,
            created_at=datetime.now(),
            archived=False,
        )

        return self.task_repository.create(domain_task)
