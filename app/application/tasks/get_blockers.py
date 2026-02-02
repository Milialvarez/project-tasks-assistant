from typing import List

from app.application.ports.project_member_repository import ProjectMemberRepository
from app.application.ports.task_blocker_repository import BlockerRepository
from app.application.ports.task_repository import TaskRepository
from app.application.ports.user_repository import UserRepository
from app.domain.entities.task_blocker import TaskBlocker
from app.domain.enums import BlockerStatus
from app.domain.exceptions import InvalidStatusError, NotProjectMemberError, ResourceNotFoundError


class GetTaskBlockersUseCase:
    def __init__(
            self,
            *,
            blocker_repo: BlockerRepository,
            task_repo: TaskRepository,
            project_member_repo: ProjectMemberRepository,
            user_repo: UserRepository
    ):
        self.blocker_repo= blocker_repo
        self.task_repo= task_repo
        self.project_member_repo=project_member_repo
        self.user_repo=user_repo

    def execute(
        self,
        *,
        task_id: int,
        status: BlockerStatus | None = None,
        user_id: int
    ) -> List[TaskBlocker]:
        task = self.task_repo.get_by_id(task_id=task_id)
        if not task:
            raise ResourceNotFoundError("Task")
        
        if not self.user_repo.exists(user_id):
            raise ResourceNotFoundError("User")
        
        if not self.project_member_repo.is_member(project_id=task.project_id, user_id=user_id):
            raise NotProjectMemberError()
        
        if status and status not in BlockerStatus:
            raise InvalidStatusError()
        
        return self.blocker_repo.get_by_task_id(task_id=task_id, status=status)
