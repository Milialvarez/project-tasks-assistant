from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.application.objectives.create_objective import CreateObjective
from app.application.objectives.delete_objective import DeleteObjective
from app.application.objectives.get_objectives import GetObjectives
from app.application.objectives.update_objective import UpdateObjective
from app.core.database import get_db
from app.dependencies.auth import get_current_user_id
from app.infrastructure.db.repositories.objective_repository import SqlAlchemyObjectiveRepository
from app.infrastructure.db.repositories.project_member_repository import SqlAlchemyProjectMemberRepository
from app.infrastructure.db.repositories.project_repository import SqlAlchemyProjectRepository
from app.infrastructure.db.repositories.sprint_repository import SqlAlchemySprintRepository
from app.schemas.objective import ObjectiveCreate, ObjectiveResponse, ObjectiveUpdate

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
    
    return use_case.execute(objective, current_user_id)

@router.put("/{objective_id}", response_model=ObjectiveResponse, status_code=200)
def update_objective(objective_data: ObjectiveUpdate,
                     objective_id: int,
                     db: Session = Depends(get_db),
                     current_user_id: int = Depends(get_current_user_id)):
    use_case=UpdateObjective(objective_repo=SqlAlchemyObjectiveRepository(db),
                             project_member_repo=SqlAlchemyProjectMemberRepository(db),
                             sprint_repo=SqlAlchemySprintRepository(db))
    
    return use_case.execute(objective_data, objective_id, current_user_id)
    
@router.delete("/{objective_id}")
def delete_objective(objective_id: int,
                     db: Session = Depends(get_db),
                     current_user_id: int = Depends(get_current_user_id)):
    use_case=DeleteObjective(objective_repo=SqlAlchemyObjectiveRepository(db),
                             project_repo=SqlAlchemyProjectRepository(db))
        
    use_case.execute(objective_id, current_user_id)
    return {"message": "Objective deleted successfully"}

@router.get("/", response_model=list[ObjectiveResponse], status_code=status.HTTP_200_OK)
def get_objectives(
    project_id: int | None = None,
    sprint_id: int | None = None,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    """
    Get objectives filtered by project or sprint.
    
    Rules:
    - If sprint_id is provided, project_id is inferred from sprint.
    - If sprint_id is NOT provided, project_id is required.
    """

    if sprint_id is None and project_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="project_id is required when sprint_id is not provided",
        )

    use_case = GetObjectives(
        objective_repo=SqlAlchemyObjectiveRepository(db),
        sprint_repo=SqlAlchemySprintRepository(db),
        project_member_repo=SqlAlchemyProjectMemberRepository(db),
    )

    return use_case.execute(
        project_id=project_id,
        sprint_id=sprint_id,
        user_id=current_user_id,
    )
