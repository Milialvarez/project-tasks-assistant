from app.application.ports.project_member_repository import ProjectMemberRepository
from app.application.ports.task_repository import TaskRepository
from app.application.ports.task_status_history_repository import TaskStatusHistoryRepository
from app.application.ports.user_repository import UserRepository
from app.domain.exceptions import NotProjectMemberError, ResourceNotFoundError


class GetStatusHistory:
    def __init__(
        self,
        project_member_repo: ProjectMemberRepository,
        task_repo: TaskRepository,
        task_status_repo: TaskStatusHistoryRepository
    ):
        self.project_member_repo = project_member_repo
        self.task_repo = task_repo
        self.task_status_repo = task_status_repo

    def execute(self, task_id: int, user_id:int):
        task = self.task_repo.get_by_id(task_id)

        if not task:
            raise ResourceNotFoundError("Task")
        
        if not self.project_member_repo.is_member(project_id=task.project_id,user_id=user_id):
            raise NotProjectMemberError()
        
        return self.task_status_repo.get_by_task_id(task_id)
        
        