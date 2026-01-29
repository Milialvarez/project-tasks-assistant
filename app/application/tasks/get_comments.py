from app.application.ports.project_member_repository import ProjectMemberRepository
from app.application.ports.task_comment_repository import CommentRepository
from app.application.ports.task_repository import TaskRepository
from app.application.ports.user_repository import UserRepository


class GetComments:
    def __init__(
            self,
            *,
            task_repo: TaskRepository,
            project_member_repo: ProjectMemberRepository,
            comments_repo: CommentRepository,
            user_repo: UserRepository
    ):
        self.task_repo= task_repo
        self.project_member_repo= project_member_repo
        self.comment_repo= comments_repo
        self.user_repo= user_repo

    def execute(self, *, task_id: int, user_id:int):
        task = self.task_repo.get_by_id(task_id=task_id)
        if not task:
            raise ValueError("Task doesn't exists")
        
        if not self.user_repo.exists(user_id):
            raise ValueError("User doesn't exists")
        
        if not self.project_member_repo.is_member(project_id=task.project_id, user_id=user_id):
            raise ValueError("You can't get this comments because you're not member of this repository")
        
        return self.comment_repo.get_comments(task_id)