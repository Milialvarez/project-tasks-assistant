from fastapi import APIRouter, Depends

from app.application.sprints.create_sprint import CreateSprintUseCase
from app.core.database import get_db
from app.dependencies.auth import get_current_user_id
from app.infrastructure.db.repositories.project_repository import SqlAlchemyProjectRepository
from app.infrastructure.db.repositories.sprint_repository import SqlAlchemySprintRepository
from app.infrastructure.db.repositories.user_repository import SqlAlchemyUserRepository
from app.schemas.sprint import SprintCreate
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
        user_repo=SqlAlchemyUserRepository
    )

    return use_case.execute(sprint, current_user_id)