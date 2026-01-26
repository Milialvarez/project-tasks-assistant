from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException

from app.application.sprints.create_sprint import CreateSprintUseCase
from app.application.sprints.start_sprint import StartSprintUseCase
from app.application.sprints.update_sprint import UpdateSprintUseCase
from app.core.database import get_db
from app.dependencies.auth import get_current_user_id
from app.infrastructure.db.repositories.project_member_repository import SqlAlchemyProjectMemberRepository
from app.infrastructure.db.repositories.project_repository import SqlAlchemyProjectRepository
from app.infrastructure.db.repositories.sprint_repository import SqlAlchemySprintRepository
from app.infrastructure.db.repositories.user_repository import SqlAlchemyUserRepository
from app.schemas.sprint import SprintCreate, SprintUpdate
from sqlalchemy.orm import Session


router = APIRouter(prefix="/sprints", tags=["Sprints"])

@router.post("/")
def create_sprint(sprint: SprintCreate,
                  db: Session = Depends(get_db),
                  current_user_id: int = Depends(get_current_user_id)):
    """
    Docstring for create_sprint
    
    :param sprint: Sprint schema with the data needed to create a sprint
    :type sprint: SprintCreate
    :param db:  db session available to execute the operation
    :type db: Session
    :param current_user_id:  ID of the user that wants to execute the operation
    :type current_user_id: int
    """
    use_case = CreateSprintUseCase(
        sprint_repo=SqlAlchemySprintRepository(db),
        project_repo=SqlAlchemyProjectRepository(db),
        user_repo=SqlAlchemyUserRepository(db)
    )

    try:
        return use_case.execute(sprint, current_user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/")
def update_sprint(sprint: SprintUpdate, 
                  db: Session = Depends(get_db), 
                  current_user_id = Depends(get_current_user_id)):
    """
    Docstring for update_sprint
    
    :param sprint: sprint schema with the data needed to update an sprint
    :type sprint: SprintUpdate
    :param db: db session available to execute the operation
    :type db: Session
    :param current_user_id: ID of the user that wants to execute the operation
    """
    use_case = UpdateSprintUseCase(
        sprint_repo=SqlAlchemySprintRepository(db),
        project_member_repo=SqlAlchemyProjectMemberRepository(db),
        user_repo=SqlAlchemyUserRepository(db)
        )
    try:
        return use_case.execute(sprint, current_user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError:
        raise HTTPException(status_code=500, detail="Internal server error")
    
@router.patch("/{sprint_id}/start")
def start_sprint(
    sprint_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    use_case = StartSprintUseCase(
        sprint_repo=SqlAlchemySprintRepository(db),
        project_member_repo=SqlAlchemyProjectMemberRepository(db),
    )

    try:
        return use_case.execute(
            sprint_id=sprint_id,
            user_id=current_user_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
