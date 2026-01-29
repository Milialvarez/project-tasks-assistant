from datetime import datetime
from app.application.ports.project_member_repository import ProjectMemberRepository
from app.application.ports.task_blocker_repository import BlockerRepository
from app.application.ports.task_repository import TaskRepository
from app.application.ports.user_repository import UserRepository
from app.domain.entities.task_blocker import TaskBlocker
from app.domain.enums import BlockerStatus
from app.schemas.blocker import TaskBlockerCreate


class CreateBlocker:
    def __init__(
            self,
            *,
            user_repository: UserRepository,
            task_repository: TaskRepository,
            project_member_repository: ProjectMemberRepository,
            blocker_repository: BlockerRepository
    ):
        self.user_repository = user_repository
        self.task_repository = task_repository
        self.project_member_repository = project_member_repository
        self.blocker_repository = blocker_repository

    def execute(self, task_id: int, blocker_data: TaskBlockerCreate, user_id: int):
        if not self.user_repository.exists(user_id=user_id):
            raise ValueError("User doesn't exists")
        task = self.task_repository.get_by_id(task_id)
        if not task:
            raise ValueError("Task doesn't exists")
        if not self.project_member_repository.is_member(project_id=task.project_id, user_id=user_id):
            raise ValueError("You can't add a blocker here because you're not a member of this project")
        
        blocker = TaskBlocker(
            id=None,
            task_id=task_id,
            cause=blocker_data.cause,
            created_by=user_id,
            status=BlockerStatus.active,
            start_date=datetime.now(),
            solved_at=None
        )

        try:
            return self.blocker_repository.create(blocker)
        except Exception:
            raise RuntimeError("Failed to create task blocker")