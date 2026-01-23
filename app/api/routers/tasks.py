from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.task import TaskCreate


router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/")
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """
    Docstring for create_task
    
    :param task: Task Schema with all the data needed to create a task
    :type task: TaskCreate
    :param db: db session available to execute the operation
    :type db: Session
    """

    # use_case = CreateTaskUseCase(task_repository=)