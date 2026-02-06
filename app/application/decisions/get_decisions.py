from typing import Optional
from app.application.ports.decision_repository import DecisionRepository
from app.application.ports.project_member_repository import ProjectMemberRepository
from app.application.ports.task_repository import TaskRepository
from app.domain.exceptions import NotProjectMemberError, ResourceNotFoundError


class GetDecisions:

    def __init__(
            self, 
            *,
            decision_repository: DecisionRepository,
            project_member_repository: ProjectMemberRepository,
            task_repository: TaskRepository
            ):
            self.decision_repository = decision_repository
            self.project_member_repository = project_member_repository
            self.task_repository = task_repository

    def execute(
        self,
        project_id: Optional[int],
        task_id: Optional[int],
        user_id: int
    ):
        if not project_id and not task_id:
         return [] 
    
        if project_id:    
            if not self.project_member_repository.is_member(project_id, user_id):
                 raise NotProjectMemberError()
        if task_id:
             task = self.task_repository.get_by_id(task_id)
             if not task:
                  raise ResourceNotFoundError("Task")
             if not self.project_member_repository.is_member(task.project_id, user_id):
                 raise NotProjectMemberError()
             
        return self.decision_repository.get_filtered(project_id, task_id)
