from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.application.ai.explain_delays_use_case import ExplainProjectDelaysUseCase
from app.core.database import get_db


router = APIRouter(prefix="/ai", tags=["AI"])


@router.get("/projects/{project_id}/delays")
def explain_project_delays(
    project_id: int,
    sprint_id: int | None = None,
    db: Session = Depends(get_db),
):
    use_case = ExplainProjectDelaysUseCase(db)
    return use_case.execute(project_id, sprint_id)
