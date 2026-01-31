from app.application.ports.project_member_repository import ProjectMemberRepository
from app.application.ports.task_comment_repository import CommentRepository
from app.application.ports.task_repository import TaskRepository
from app.application.ports.user_repository import UserRepository


class DeleteComment:
    def __init__(
            self,
            *,
            comment_repo:CommentRepository,
            user_repo:UserRepository,
    ):
        self.comment_repo=comment_repo
        self.user_repo=user_repo

    def execute(self, comment_id: int, user_id: int):
        comment = self.comment_repo.get_by_id(comment_id)

        if not comment:
            raise ValueError("Comment doesn't exists")
        
        if not self.user_repo.exists(user_id):
            raise ValueError("User doesn't exists")
        
        if comment.user_id != user_id:
            raise ValueError("You can't delete this comment because you didn't write it")
        
        try:
            self.comment_repo.delete(comment_id)
        except Exception:
            raise RuntimeError("Failed to delete task blocker")
        