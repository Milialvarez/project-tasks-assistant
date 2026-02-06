from app.application.ports.project_member_repository import ProjectMemberRepository
from app.application.ports.task_repository import TaskRepository
from app.application.ports.user_repository import UserRepository
from app.domain.exceptions import NotProjectMemberError, ResourceNotFoundError


class GetById:
    def __init__(
            self,
            *,
            task_repository: TaskRepository,
            user_repository: UserRepository,
            project_member_repository: ProjectMemberRepository
    ):
        self.task_repository=task_repository
        self.user_repository=user_repository
        self.project_member_repository=project_member_repository

    def execute(self, task_id, user_id):
        if not self.user_repository.exists(user_id):
            raise ResourceNotFoundError("User")
        
        task = self.task_repository.get_by_id(task_id)

        if not task:
            raise ResourceNotFoundError("Task")
        
        if not self.project_member_repository.is_member(task.project_id, user_id):
            raise NotProjectMemberError()
        
        return task