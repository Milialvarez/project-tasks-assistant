from app.application.ports.project_member_repository import ProjectMemberRepository
from app.application.ports.task_repository import TaskRepository
from app.application.ports.user_repository import UserRepository


class GetById:
    def __init__(
            self,
            *,
            task_repo: TaskRepository,
            user_repo: UserRepository,
            project_member_repo: ProjectMemberRepository
    ):
        self.task_repo=task_repo
        self.user_repo=user_repo
        self.project_member_repo=project_member_repo

    def execute(self, task_id, user_id):
        if not self.user_repo.exists(user_id):
            raise ValueError("User doesn't exists")
        
        task = self.task_repo.get_by_id(task_id)

        if not task:
            raise ValueError("There's no task with the provided ID")
        
        if not self.project_member_repo.is_member(task.project_id, user_id):
            raise ValueError("You can't see this task because you're not member of this project")
        
        return task