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
    project_repo = SqlAlchemyProjectRepository(db)
    user_repo = SqlAlchemyUserRepository(db)

    use_case = CreateProjectUseCase(
        project_repo=project_repo,
        user_repo=user_repo,
    )

    project = use_case.execute(
        name=name,
        description=description,
        created_by=1,  # hardcodeado por hasta que existan usuarios y sesiones
    )

    return project
