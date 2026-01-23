from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.application.tasks.create_task import CreateTaskUseCase
from app.core.database import get_db
from app.infrastructure.db.repositories.project_repository import SqlAlchemyProjectRepository
from app.infrastructure.db.repositories.task_repository import SqlAlchemyTaskRepository
from app.infrastructure.db.repositories.user_repository import SqlAlchemyUserRepository
from app.schemas.task import TaskCreate, TaskResponse


router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """
    Docstring for create_task
    
    :param task: Task Schema with all the data needed to create a task
    :type task: TaskCreate
    :param db: db session available to execute the operation
    :type db: Session
    """

    use_case = CreateTaskUseCase(
        project_repository=SqlAlchemyProjectRepository(db),
        user_repository=SqlAlchemyUserRepository(db),
        task_repository=SqlAlchemyTaskRepository(db),
    )

    try:
        created_task = use_case.execute(task=task)
        return created_task
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
