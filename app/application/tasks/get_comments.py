from app.application.ports.project_member_repository import ProjectMemberRepository
from app.application.ports.task_comment_repository import CommentRepository
from app.application.ports.task_repository import TaskRepository
from app.application.ports.user_repository import UserRepository
from app.domain.exceptions import NotProjectMemberError, ResourceNotFoundError


class GetComments:
    def __init__(
            self,
            *,
            task_repository: TaskRepository,
            project_member_repository: ProjectMemberRepository,
            comments_repository: CommentRepository,
            user_repository: UserRepository
    ):
        self.task_repository= task_repository
        self.project_member_repository= project_member_repository
        self.comment_repository= comments_repository
        self.user_repository= user_repository

    def execute(self, *, task_id: int, user_id:int):
        task = self.task_repository.get_by_id(task_id=task_id)
        if not task:
            raise ResourceNotFoundError("Task")
        
        if not self.user_repository.exists(user_id):
            raise ResourceNotFoundError("User")
        
        if not self.project_member_repository.is_member(project_id=task.project_id, user_id=user_id):
            raise NotProjectMemberError()
        
        return self.comment_repository.get_comments(task_id)