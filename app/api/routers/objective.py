from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.application.objectives.create_objective import CreateObjective
from app.core.database import get_db
from app.dependencies.auth import get_current_user_id
from app.infrastructure.db.repositories.objective_repository import SqlAlchemyObjectiveRepository
from app.infrastructure.db.repositories.project_member_repository import SqlAlchemyProjectMemberRepository
from app.infrastructure.db.repositories.sprint_repository import SqlAlchemySprintRepository
from app.schemas.objective import ObjectiveCreate, ObjectiveResponse

router = APIRouter(prefix="/objectives", tags=["Objectives"])

@router.post("/", response_model=ObjectiveResponse, status_code=201)
def create_objective(objective: ObjectiveCreate, 
                     db:Session = Depends(get_db),
                     current_user_id: int = Depends(get_current_user_id)):
    """
    Docstring for create_objective
    
    :param objective: Objective schema with the data needed to create the instance
    :type objective: ObjectiveCreate
    :param db: db session available to execute the operation
    :type db: Session
    :param current_user_id: ID of the user that wants to execute the operation
    :type current_user_id: int
    """

    use_case = CreateObjective(objective_repo=SqlAlchemyObjectiveRepository(db),
                               sprint_repo=SqlAlchemySprintRepository(db),
                               project_member_repo=SqlAlchemyProjectMemberRepository(db))
    
    try:
        return use_case.execute(objective, current_user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError:
        raise HTTPException(status_code=500, detail="Internal server error")