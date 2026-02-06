from http.client import HTTPException
from app.application.ports.decision_repository import DecisionRepository
from fastapi import status
from app.application.ports.project_repository import ProjectRepository
from app.domain.exceptions import NotProjectManagerError, ResourceNotFoundError
from app.schemas.decision import DecisionUpdate


class UpdateDecision:

    def __init__(
            self, 
            *,
            decision_repository: DecisionRepository,
            project_repository: ProjectRepository
            ):
            self.decision_repository = decision_repository
            self.project_repository = project_repository

    def execute(self, decision_id: int, data: DecisionUpdate, user_id: int):
        decision = self.decision_repository.get_by_id(decision_id)

        if not decision:
            raise ResourceNotFoundError("Decision")

        if not self.project_repository.is_manager(...) and user_id != decision.chosen_by:
            raise NotProjectManagerError(
                "You are not allowed to update this decision"
            )

        
        if data.title is not None:
             decision.title = data.title

        if data.context is not None:
             decision.context = data.context
        
        if data.impact is not None:
             decision.impact = data.impact

        try:
            return self.decision_repository.update(decision=decision)
        except Exception:
            raise RuntimeError("Failed to update decision")
