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
            blocker_repository: BlockerRepository,
            task_repository: TaskRepository,
            project_member_repository: ProjectMemberRepository,
            user_repository: UserRepository
    ):
        self.blocker_repository= blocker_repository
        self.task_repository= task_repository
        self.project_member_repository=project_member_repository
        self.user_repository=user_repository

    def execute(
        self,
        *,
        task_id: int,
        status: BlockerStatus | None = None,
        user_id: int
    ) -> List[TaskBlocker]:
        task = self.task_repository.get_by_id(task_id=task_id)
        if not task:
            raise ResourceNotFoundError("Task")
        
        if not self.user_repository.exists(user_id):
            raise ResourceNotFoundError("User")
        
        if not self.project_member_repository.is_member(project_id=task.project_id, user_id=user_id):
            raise NotProjectMemberError()
        
        if status and status not in BlockerStatus:
            raise InvalidStatusError()
        
        return self.blocker_repository.get_by_task_id(task_id=task_id, status=status)
