from app.application.ports.project_member_repository import ProjectMemberRepository
from app.application.ports.task_repository import TaskRepository


class GetArchivedTask:
    def __init__(
            self,
            task_repo: TaskRepository,
            project_member_repo: ProjectMemberRepository
    ):
        self.task_repo=task_repo
        self.project_member_repo=project_member_repo

    def execute(self, project_id: int, sprint_id: int | None, user_id: int):
        if not self.project_member_repo.is_member(project_id=project_id, user_id=user_id):
            raise ValueError("You can't view this tasks because you're not a member of this repository")
        
        return self.task_repo.get_archived(project_id, sprint_id)