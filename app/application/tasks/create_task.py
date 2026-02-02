from datetime import datetime
from app.application.ports.project_member_repository import ProjectMemberRepository
from app.application.ports.project_repository import ProjectRepository
from app.application.ports.sprint_repository import SprintRepository
from app.application.ports.task_repository import TaskRepository
from app.application.ports.user_repository import UserRepository
from app.domain.entities.task import Task
from app.domain.exceptions import NotProjectMemberError, PersistenceError, ResourceNotFoundError
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
            raise ResourceNotFoundError("Project")

        # assigned user
        if task.assigned_user_id:
            user = self.user_repository.get_by_id(task.assigned_user_id)
            if not user:
                raise ResourceNotFoundError("Assigned User")

            if not self.project_member_repository.is_member(
                task.project_id, task.assigned_user_id
            ):
                raise NotProjectMemberError()

        # sprint exists
        if task.sprint_id:
            if not self.sprint_repository.get_by_id(task.sprint_id):
                raise ResourceNotFoundError("Sprint")

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
        try:
            return self.task_repository.create(domain_task)
        except Exception as e:
            raise PersistenceError("Failed at task creation")
