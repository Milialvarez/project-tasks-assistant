from typing import Optional
from app.application.ports.decision_repository import DecisionRepository
from app.application.ports.project_member_repository import ProjectMemberRepository
from app.application.ports.task_repository import TaskRepository


class GetDecisions:

    def __init__(
            self, 
            *,
            decision_repo: DecisionRepository,
            project_member_repo: ProjectMemberRepository,
            task_repo: TaskRepository
            ):
            self.decision_repo = decision_repo
            self.project_member_repo=project_member_repo
            self.task_repo=task_repo

    def execute(
        self,
        project_id: Optional[int],
        task_id: Optional[int],
        user_id: int
    ):
        if project_id:    
            if not self.project_member_repo.is_member(project_id, user_id):
                 raise ValueError("You can't see this decisions because you're not a member of this project")
        if task_id:
             task = self.task_repo.get_by_id(task_id)
             if not task:
                  raise ValueError("Task with the provided ID doesn't exists")
             if not self.project_member_repo.is_member(task.project_id, user_id):
                 raise ValueError("You can't see this decisions because you're not a member of this project")
             
        return self.decision_repo.get_filtered(project_id, task_id)
