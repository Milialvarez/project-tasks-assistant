from app.application.ports.project_member_repository import ProjectMemberRepository
from app.application.ports.task_repository import TaskRepository
from app.domain.exceptions import NotProjectMemberError


class GetArchivedTask:
    def __init__(
            self,
            task_repository: TaskRepository,
            project_member_repository: ProjectMemberRepository
    ):
        self.task_repository=task_repository
        self.project_member_repository=project_member_repository

    def execute(self, project_id: int, sprint_id: int | None, user_id: int):
        if not self.project_member_repository.is_member(project_id=project_id, user_id=user_id):
            raise NotProjectMemberError()
        
        return self.task_repository.get_archived(project_id, sprint_id)