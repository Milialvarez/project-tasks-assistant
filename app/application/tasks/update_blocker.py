from datetime import datetime
from app.application.ports.project_member_repository import ProjectMemberRepository
from app.application.ports.task_blocker_repository import BlockerRepository
from app.application.ports.task_repository import TaskRepository
from app.application.ports.task_status_history_repository import TaskStatusHistoryRepository
from app.application.ports.user_repository import UserRepository
from app.domain.entities.task_status_history import TaskStatusHistory
from app.domain.enums import BlockerStatus, TaskStatus
from app.domain.exceptions import InvalidStatusError, NotProjectMemberError, PersistenceError, ResourceNotFoundError
from app.schemas.blocker import BlockerUpdate

class UpdateBlockerUseCase:
    def __init__(
            self,
            *,
            blocker_repository:BlockerRepository,
            task_repository:TaskRepository,
            task_status_repository:TaskStatusHistoryRepository,
            user_repository:UserRepository,
            project_member_repository:ProjectMemberRepository
    ):
        self.blocker_repository=blocker_repository
        self.task_repository=task_repository
        self.task_status_history_repository=task_status_repository
        self.user_repository=user_repository
        self.project_member_repository=project_member_repository

    def execute(self, blocker_id: int, blocker_data: BlockerUpdate, user_id: int):

        blocker = self.blocker_repository.get_by_id(blocker_id)
        if not blocker:
            raise ResourceNotFoundError("Blocker")

        task = self.task_repository.get_by_id(blocker.task_id)
        if not task:
            raise ResourceNotFoundError("Task")

        if not self.project_member_repository.is_member(task.project_id, user_id):
            raise NotProjectMemberError(
                "You are not allowed to update blockers in this project"
            )

        if blocker_data.cause is not None:
            blocker.cause = blocker_data.cause

        if blocker_data.status is not None:
            if blocker_data.status != BlockerStatus.resolved:
                raise InvalidStatusError("Only 'resolved' status is allowed")
            blocker.status = BlockerStatus.resolved
            blocker.solved_at = datetime.now()

        try:
            updated_blocker = self.blocker_repository.update(blocker)

            if updated_blocker.status == BlockerStatus.resolved:
                history = TaskStatusHistory(
                    id=None,
                    task_id=task.id,
                    previous_status=task.current_status,
                    new_status=TaskStatus.in_progress,
                    changed_by=user_id,
                )
                self.task_status_history_repository.create(history)

                task.current_status = TaskStatus.in_progress
                self.task_repository.update(task)

            return updated_blocker

        except Exception as e:
            raise PersistenceError("Failed to update task blocker") from e
