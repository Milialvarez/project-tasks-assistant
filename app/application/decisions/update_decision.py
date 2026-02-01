from http.client import HTTPException
from app.application.ports.decision_repository import DecisionRepository
from fastapi import status
from app.application.ports.project_repository import ProjectRepository
from app.schemas.decision import DecisionUpdate


class UpdateDecision:

    def __init__(
            self, 
            *,
            decision_repo: DecisionRepository,
            project_repo: ProjectRepository
            ):
            self.decision_repo = decision_repo
            self.project_repo=project_repo

    def execute(self, decision_id: int, data: DecisionUpdate, user_id: int):
        decision = self.decision_repo.get_by_id(decision_id)

        if not decision:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Decision not found",
            )
        
        if not self.project_repo.is_manager(decision.project_id, user_id) and user_id!= decision.chosen_by:
             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                 detail="You can't delete this decision because you're not manager of the project or the user who chose it")
        
        if data.title is not None:
             decision.title = data.title

        if data.context is not None:
             decision.context = data.context
        
        if data.impact is not None:
             decision.impact = data.impact

        try:
            return self.decision_repo.update(decision=decision)
        except Exception:
            raise RuntimeError("Failed to update decision")
