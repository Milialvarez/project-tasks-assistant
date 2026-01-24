from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.application.tasks.create_task import CreateTaskUseCase
from app.application.tasks.delete_task import DeleteTaskUseCase
from app.application.tasks.filter_tasks import FilterTasksUseCase
from app.application.tasks.update_task import UpdateTaskUseCase
from app.core.database import get_db
from app.dependencies.auth import get_current_user_id
from app.infrastructure.db.repositories.project_repository import SqlAlchemyProjectRepository
from app.infrastructure.db.repositories.task_repository import SqlAlchemyTaskRepository
from app.infrastructure.db.repositories.task_status_history import SqlAlchemyTaskStatusHistoryRepository
from app.infrastructure.db.repositories.user_repository import SqlAlchemyUserRepository
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate


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
    
    
@router.get("/", response_model=list[TaskResponse])
def filter_tasks(
    project_id: int | None = None,
    sprint_id: int | None = None,
    assigned_user_id: int | None = None,
    db: Session = Depends(get_db),
):
    """
    Docstring for get_tasks_by_project
    
    :param project_id: ID of the project that will filter the tasks
    :type project_id: int
    :param db: db session available to execute the operation
    :type db: Session
    """
     
    use_case = FilterTasksUseCase(
        project_repository=SqlAlchemyProjectRepository(db),
        user_repository=SqlAlchemyUserRepository(db),
        task_repository=SqlAlchemyTaskRepository(db),
    )

    try:
        return use_case.execute(
            project_id=project_id,
            sprint_id=sprint_id,
            assigned_user_id=assigned_user_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Docstring for update_task
    
    :param task_id: ID of the task that will be updated
    :type task_id: int
    :param data: Task schema with the new data
    :type data: TaskUpdate
    :param db: session available to execute the operation
    :type db: Session
    :param current_user_id: user that wants to execute the operation
    :type current_user_id: int
    """
    use_case = UpdateTaskUseCase(
    task_repository=SqlAlchemyTaskRepository(db),
    user_repository=SqlAlchemyUserRepository(db),
    project_repository=SqlAlchemyProjectRepository(db),
    status_history_repository=SqlAlchemyTaskStatusHistoryRepository(db),
)

    try:
        return use_case.execute(
            task_id=task_id,
            user_id=current_user_id, 
            data=data,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{task_id}")
def delete_task(task_id: int, 
                db: Session = Depends(get_db),
                current_user_id: int = Depends(get_current_user_id)):
    """
    Docstring for delete_task
    
    :param task_id: ID of the task that will be deleted
    :type task_id: int
    :param db: session available to execute the operation
    :type db: Session
    :param current_user_id: User that wants to delete the task
    :type current_user_id: int
    """
    
    use_case = DeleteTaskUseCase(
    task_repository=SqlAlchemyTaskRepository(db),
    project_repository=SqlAlchemyProjectRepository(db),
)

    try:
        use_case.execute(task_id=task_id, user_id=current_user_id)
        return {"message": "Task deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))