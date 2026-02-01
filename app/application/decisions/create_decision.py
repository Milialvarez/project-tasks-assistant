from datetime import datetime
from app.application.ports.decision_repository import DecisionRepository
from app.application.ports.project_member_repository import ProjectMemberRepository
from app.application.ports.task_repository import TaskRepository
from app.domain.entities.decision import Decision
from app.schemas.decision import DecisionCreate


class CreateDecision:

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

    def execute(self, decision_data: DecisionCreate, user_id: int):
        if not self.project_member_repo.is_member(decision_data.project_id, user_id):
             raise ValueError("You can't create a decision because you're not a member of this project")
        
        if decision_data.task_id:
             task= self.task_repo.get_by_id(decision_data.task_id)
             if not task:
                  raise ValueError("Task with the sent ID doesn't exists")
             if task.project_id != decision_data.project_id:
                  raise ValueError("The task provided doesn't belongs to the provided project")
             
        decision = Decision(
            project_id=decision_data.project_id,
            task_id=decision_data.task_id,
            title=decision_data.title,
            context=decision_data.context,
            impact=decision_data.impact,
            chosen_by=user_id,
            created_at=datetime.now()
        )

        try:
            return self.decision_repo.create(decision)
        except Exception:
            raise RuntimeError("Failed to create objective")
