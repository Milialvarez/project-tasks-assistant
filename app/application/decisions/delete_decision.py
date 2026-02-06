from http.client import HTTPException
from app.application.ports.decision_repository import DecisionRepository
from fastapi import status

from app.application.ports.project_repository import ProjectRepository
from app.domain.exceptions import NotProjectManagerError, ResourceNotFoundError

class DeleteDecision:

    def __init__(
            self, 
            *,
            decision_repository: DecisionRepository,
            project_repository: ProjectRepository
            ):
            self.decision_repository = decision_repository
            self.project_repository = project_repository

    def execute(self, decision_id: int, user_id: int):
        decision = self.decision_repository.get_by_id(decision_id)

        if not decision:
            raise ResourceNotFoundError("Decision")

        if not self.project_repository.is_manager(...) and user_id != decision.chosen_by:
            raise NotProjectManagerError(
                "You are not allowed to delete this decision"
            )

        try:
            self.decision_repository.delete(decision)
        except Exception:
            raise RuntimeError("Failed to delete the decision")
        
