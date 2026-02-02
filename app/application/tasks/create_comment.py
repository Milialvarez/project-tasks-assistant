from datetime import datetime
from app.application.ports.project_member_repository import ProjectMemberRepository
from app.application.ports.task_comment_repository import CommentRepository
from app.application.ports.task_repository import TaskRepository
from app.application.ports.user_repository import UserRepository
from app.domain.entities.task_comment import TaskComment
from app.domain.exceptions import NotProjectMemberError, PersistenceError, ResourceNotFoundError
from app.schemas.comment import CommentCreate


class CreateComment:
    def __init__(
            self,
            *,
            user_repository: UserRepository,
            task_repository: TaskRepository,
            project_member_repository: ProjectMemberRepository,
            comment_repository: CommentRepository
    ):
        self.user_repository = user_repository
        self.task_repository = task_repository
        self.project_member_repository = project_member_repository
        self.comment_repository = comment_repository

    def execute(self, task_id: int, comment_data: CommentCreate, user_id: int):
        if not self.user_repository.exists(user_id=user_id):
            raise ResourceNotFoundError("User")
        task = self.task_repository.get_by_id(task_id)
        if not task:
            raise ResourceNotFoundError("Task")
        if not self.project_member_repository.is_member(project_id=task.project_id, user_id=user_id):
            raise NotProjectMemberError()
        
        comment = TaskComment(
            id=None,
            task_id=task_id,
            user_id=user_id,
            content=comment_data.content,
            created_at=datetime.now()
        )

        try:
            return self.comment_repository.create(comment)
        except Exception as e:
            raise PersistenceError("Failed to create task comment") from e