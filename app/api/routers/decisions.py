from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.application.decisions.create_decision import CreateDecision
from app.application.decisions.delete_decision import DeleteDecision
from app.application.decisions.get_decisions import GetDecisions
from app.application.decisions.update_decision import UpdateDecision
from app.core.database import get_db
from app.dependencies.auth import get_current_user_id
from app.infrastructure.db.repositories.decision_repository import SqlAlchemyDecisionRepository
from app.infrastructure.db.repositories.project_member_repository import SqlAlchemyProjectMemberRepository
from app.infrastructure.db.repositories.project_repository import SqlAlchemyProjectRepository
from app.infrastructure.db.repositories.task_repository import SqlAlchemyTaskRepository
from app.schemas.decision import DecisionCreate, DecisionResponse, DecisionUpdate

router = APIRouter(prefix="/decisions", tags=["Decisions"])

@router.post("/", response_model=DecisionResponse, status_code=status.HTTP_201_CREATED)
def create_decision(
    decision_data: DecisionCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    use_case = CreateDecision(
        decision_repository=SqlAlchemyDecisionRepository(db),
        project_member_repository=SqlAlchemyProjectMemberRepository(db),
        task_repository=SqlAlchemyTaskRepository(db),
    )

    return use_case.execute(decision_data, current_user_id)


@router.put("/{decision_id}", response_model=DecisionResponse)
def update_decision(
    decision_id: int,
    decision_data: DecisionUpdate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    use_case = UpdateDecision(decision_repository=SqlAlchemyDecisionRepository(db),
                              project_repository=SqlAlchemyProjectRepository(db))

    return use_case.execute(decision_id, decision_data, current_user_id)

@router.delete("/{decision_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_decision(
    decision_id: int,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    use_case = DeleteDecision(
                decision_repository=SqlAlchemyDecisionRepository(db),
                project_repository=SqlAlchemyProjectRepository(db))
    
    use_case.execute(decision_id, current_user_id)
    return {"message": "Decision deleted successfully"}

@router.get("/", response_model=list[DecisionResponse], status_code=200)
def get_decisions(
    project_id: int | None = None,
    task_id: int | None = None,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    if not project_id and not task_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="project_id is required when task_id is not provided",
        )

    use_case = GetDecisions(decision_repository=SqlAlchemyDecisionRepository(db),
                            project_member_repository=SqlAlchemyProjectMemberRepository(db),
                            task_repository=SqlAlchemyTaskRepository(db))
    return use_case.execute(project_id, task_id, current_user_id)

