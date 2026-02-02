from datetime import datetime
from decimal import InvalidOperation
from app.application.ports.project_member_repository import ProjectMemberRepository
from app.application.ports.task_comment_repository import CommentRepository
from app.application.ports.task_repository import TaskRepository
from app.application.ports.user_repository import UserRepository
from app.domain.exceptions import PersistenceError, ResourceNotFoundError
from app.schemas.comment import CommentCreate


class UpdateComment:
    def __init__(
            self,
            *,
            comment_repo=CommentRepository,
            user_repo=UserRepository,
    ):
        self.comment_repo=comment_repo
        self.user_repo=user_repo

    def execute(self, comment_id: int, comment_data: CommentCreate, user_id: int):
        comment = self.comment_repo.get_by_id(comment_id)

        if not comment:
            raise ResourceNotFoundError("Comment")
        
        if not self.user_repo.exists(user_id):
            raise ResourceNotFoundError("User")
        
        if comment.user_id != user_id:
            raise InvalidOperation("You can't update this comment because you didn't write it")
        
        comment.content = comment_data.content
        comment.edited_at = datetime.now()

        try:
            self.comment_repo.update(comment)
        except Exception as e:
            raise PersistenceError("Failed to update task comment") from e
        
        