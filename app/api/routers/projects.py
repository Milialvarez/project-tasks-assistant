from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.application.projects.delete_project import DeleteProjectUseCase
from app.application.projects.get_user_projects import GetUserProjectsUseCase
from app.application.projects.update_project import UpdateProjectUseCase
from app.core.database import get_db
from app.application.projects.create_project import CreateProjectUseCase
from app.infrastructure.db.repositories.project_repository import SqlAlchemyProjectRepository
from app.infrastructure.db.repositories.user_repository import SqlAlchemyUserRepository

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.post("/")
def create_project(
    name: str,
    description: str | None = None,
    db: Session = Depends(get_db),
):
    """
    Creates a project
    
    :param name: represents the name of the project
    :type name: str
    :param description: represents the description of the project
    :type description: str | None
    :param db: db session available to execute the operation
    :type db: Session
    """
    project_repository = SqlAlchemyProjectRepository(db)
    user_repository = SqlAlchemyUserRepository(db)

    use_case = CreateProjectUseCase(
        project_repository=project_repository,
        user_repository=user_repository,
    )

    project = use_case.execute(
        name=name,
        description=description,
        created_by=1,  # hardcoded until the jwt implementation is working
    )

    return project

@router.get("/user/{user_id}")
def get_user_projects(
    user_id: int,
    db: Session = Depends(get_db),
):
    """
    Get all the projects of a user
    
    :param user_id: id of the user
    :type user_id: int
    :param db: db session available to execute the operation
    :type db: Session
    """
    project_repo = SqlAlchemyProjectRepository(db)
    user_repo = SqlAlchemyUserRepository(db)

    use_case = GetUserProjectsUseCase(
        project_repository=project_repo,
        user_repository=user_repo,
    )

    return use_case.execute(user_id)

@router.put("/{project_id}")
def update_project(
    project_id: int,
    name: str | None = None,
    description: str | None = None,
    db: Session = Depends(get_db),
):
    """
    Update a project
    
    :param project_id: id of the project that will be updated
    :type project_id: int
    :param name: optional name to replace the original
    :type name: str | None
    :param description: optional description to replace the original
    :type description: str | None
    :param db: db session available to execute the operation
    :type db: Session
    """
    project_repo = SqlAlchemyProjectRepository(db)

    use_case = UpdateProjectUseCase(project_repo)

    return use_case.execute(
        project_id=project_id,
        user_id=1,  # hardcoded
        name=name,
        description=description,
    )

@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
):
    """
    Delete a project
    
    :param project_id: id of the project that will be deleted
    :type project_id: int
    :param db: db session available to execute the operation
    :type db: Session
    """
    project_repo = SqlAlchemyProjectRepository(db)

    use_case = DeleteProjectUseCase(project_repo)

    use_case.execute(
        project_id=project_id,
        user_id=1,  # hardcoded
    )

    return {"message": "Project deleted successfully"}
