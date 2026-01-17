from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

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
    project_repository = SqlAlchemyProjectRepository(db)
    user_repository = SqlAlchemyUserRepository(db)

    use_case = CreateProjectUseCase(
        project_repository=project_repository,
        user_repository=user_repository,
    )

    project = use_case.execute(
        name=name,
        description=description,
        created_by=1,  # hardcodeado por ahora
    )

    return project
