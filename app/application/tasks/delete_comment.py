from decimal import InvalidOperation
from app.application.ports.task_comment_repository import CommentRepository
from app.application.ports.user_repository import UserRepository
from app.domain.exceptions import PersistenceError, ResourceNotFoundError


class DeleteComment:
    def __init__(
            self,
            *,
            comment_repository:CommentRepository,
            user_repository:UserRepository,
    ):
        self.comment_repository=comment_repository
        self.user_repository=user_repository

    def execute(self, comment_id: int, user_id: int):
        
        comment = self.comment_repository.get_by_id(comment_id)

        if not comment:
            raise ResourceNotFoundError("Task Comment")
        
        if not self.user_repository.exists(user_id):
            raise ResourceNotFoundError("Error")
        
        if comment.user_id != user_id:
            raise InvalidOperation("You can't delete this comment because you didn't write it")
        
        try:
            self.comment_repository.delete(comment_id)
        except Exception as e:
            raise PersistenceError("Failed to delete task blocker")
        