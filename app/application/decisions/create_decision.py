from datetime import datetime
from app.domain.entities.decision import Decision
from app.domain.exceptions import (
    NotProjectMemberError,
    ResourceNotFoundError,
    InvalidOperationError,
)
from app.application.ports.decision_repository import DecisionRepository
from app.application.ports.project_member_repository import ProjectMemberRepository
from app.application.ports.task_repository import TaskRepository
from app.schemas.decision import DecisionCreate


class CreateDecision:

    def __init__(
        self,
        *,
        decision_repository: DecisionRepository,
        project_member_repository: ProjectMemberRepository,
        task_repository: TaskRepository,
    ):
        self.decision_repository = decision_repository
        self.project_member_repository = project_member_repository
        self.task_repository = task_repository

    def execute(self, decision_data: DecisionCreate, user_id: int):

        if not self.project_member_repository.is_member(decision_data.project_id, user_id):
            raise NotProjectMemberError()

        if decision_data.task_id:
            task = self.task_repository.get_by_id(decision_data.task_id)

            if not task:
                raise ResourceNotFoundError("Task")

            if task.project_id != decision_data.project_id:
                raise InvalidOperationError(
                    "The task does not belong to the provided project"
                )

        decision = Decision(
            project_id=decision_data.project_id,
            task_id=decision_data.task_id,
            title=decision_data.title,
            context=decision_data.context,
            impact=decision_data.impact,
            chosen_by=user_id,
            created_at=datetime.now(),
        )

        return self.decision_repository.create(decision)
