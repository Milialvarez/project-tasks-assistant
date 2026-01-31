from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.application.tasks.create_blocker import CreateBlocker
from app.application.tasks.create_comment import CreateComment
from app.application.tasks.create_task import CreateTaskUseCase
from app.application.tasks.delete_comment import DeleteComment
from app.application.tasks.delete_task import DeleteTaskUseCase
from app.application.tasks.filter_tasks import FilterTasksUseCase
from app.application.tasks.get_archived_tasks import GetArchivedTask
from app.application.tasks.get_blockers import GetTaskBlockersUseCase
from app.application.tasks.get_by_id import GetById
from app.application.tasks.get_comments import GetComments
from app.application.tasks.get_status_history import GetStatusHistory
from app.application.tasks.update_blocker import UpdateBlockerUseCase
from app.application.tasks.update_comment import UpdateComment
from app.application.tasks.update_task import UpdateTaskUseCase
from app.core.database import get_db
from app.dependencies.auth import get_current_user_id
from app.domain.enums import BlockerStatus
from app.infrastructure.db.repositories.project_member_repository import SqlAlchemyProjectMemberRepository
from app.infrastructure.db.repositories.project_repository import SqlAlchemyProjectRepository
from app.infrastructure.db.repositories.sprint_repository import SqlAlchemySprintRepository
from app.infrastructure.db.repositories.task_blocker_repository import SqlAlchemyBlockerRepository
from app.infrastructure.db.repositories.task_comment_repository import SqlAlchemyCommentRepository
from app.infrastructure.db.repositories.task_repository import SqlAlchemyTaskRepository
from app.infrastructure.db.repositories.task_status_history_repository import SqlAlchemyTaskStatusHistoryRepository
from app.infrastructure.db.repositories.user_repository import SqlAlchemyUserRepository
from app.schemas.blocker import BlockerUpdate, TaskBlockerCreate, TaskBlockerResponse
from app.schemas.comment import CommentCreate, CommentResponse
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate


router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
):
    """
    Docstring for create_task
    
    :param task: Task Schema with all the data needed to create a task
    :type task: TaskCreate
    :param db: db session available to execute the operation
    :type db: Session
    """
    use_case = CreateTaskUseCase(
        project_repository=SqlAlchemyProjectRepository(db),
        sprint_repository=SqlAlchemySprintRepository(db),
        user_repository=SqlAlchemyUserRepository(db),
        task_repository=SqlAlchemyTaskRepository(db),
        project_member_repository=SqlAlchemyProjectMemberRepository(db),
    )

    try:
        return use_case.execute(task=task)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    
@router.get("/", response_model=list[TaskResponse])
def filter_tasks(
    project_id: int | None = None,
    sprint_id: int | None = None,
    assigned_user_id: int | None = None,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """
    Docstring for filter_tasks
    Filter tasks by project (required), sprint or assigned user. Always verifies the user
    who wants to get the task is member of the project with the sent ID
    
    :param project_id: ID of the project to filter
    :type project_id: int | None
    :param sprint_id: Id of the sprint to filter
    :type sprint_id: int | None
    :param assigned_user_id: ID of the user assigned to a task to filter
    :type assigned_user_id: int | None
    :param current_user_id: ID of the user who wants to execute the operation
    :type current_user_id: int
    :param db: db session available to execute the operation
    :type db: Session
    """

    use_case = FilterTasksUseCase(
        project_repository=SqlAlchemyProjectRepository(db),
        project_member_repository=SqlAlchemyProjectMemberRepository(db),
        user_repository=SqlAlchemyUserRepository(db),
        task_repository=SqlAlchemyTaskRepository(db),
    )

    try:
        return use_case.execute(
            project_id=project_id,
            sprint_id=sprint_id,
            assigned_user_id=assigned_user_id,
            current_user_id=current_user_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError:
        raise HTTPException(status_code=500, detail="Internal server error")


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
    status_history_repository=SqlAlchemyTaskStatusHistoryRepository(db),
    project_member_repository=SqlAlchemyProjectMemberRepository(db)
)

    try:
        return use_case.execute(
            task_id=task_id,
            user_id=current_user_id, 
            data=data,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError:
        raise HTTPException(status_code=500, detail="Internal server error")


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
    project_member_repository=SqlAlchemyProjectMemberRepository(db),
)

    try:
        use_case.execute(task_id=task_id, user_id=current_user_id)
        return {"message": "Task deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError:
        raise HTTPException(status_code=500, detail="Internal server error")
    
@router.get('/{task_id}/history')
def get_status_history(task_id: int, 
                       db: Session = Depends(get_db), 
                       current_user_id: int = Depends(get_current_user_id)):
    """
    Docstring for get_status_history
    
    :param task_id: ID of the task to filter
    :type task_id: int
    :param db: session available to execute the operation
    :type db: Session
    :param current_user_id: User that wants to view the status history
    :type current_user_id: int
    """

    use_case = GetStatusHistory(
        task_repo=SqlAlchemyTaskRepository(db),
        project_member_repo=SqlAlchemyProjectMemberRepository(db),
        task_status_repo=SqlAlchemyTaskStatusHistoryRepository(db),
    )


    try:
        return use_case.execute(task_id, current_user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError:
        raise HTTPException(status_code=500, detail="Internal server error")
    
@router.post("/{task_id}/comment", response_model=CommentResponse, status_code=201)
def create_task_comment(task_id: int,
                        comment: CommentCreate, 
                        db: Session = Depends(get_db), 
                        current_user_id: int = Depends(get_current_user_id)):
    """
    Docstring for create_task_comment
    
    :param comment: comment data to create the instance
    :type comment: CommentCreate
    :param db: session available to execute the operation
    :type db: Session
    :param current_user_id: ID of the user that wants to execute the operation
    :type current_user_id: int
    """
    use_case=CreateComment(user_repository=SqlAlchemyUserRepository(db),
                           task_repository=SqlAlchemyTaskRepository(db),
                           project_member_repository=SqlAlchemyProjectMemberRepository(db),
                           comment_repository=SqlAlchemyCommentRepository(db))
    try:
        return use_case.execute(task_id=task_id, comment_data=comment, user_id=current_user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError:
        raise HTTPException(status_code=500, detail="Internal server error")
    
@router.post("/{task_id}/blocker", response_model=TaskBlockerResponse)
def create_task_blocker(task_id: int, 
                        blocker: TaskBlockerCreate,
                        db: Session = Depends(get_db), 
                        current_user_id: int = Depends(get_current_user_id)):
    """
    Docstring for create_task_blocker
    
    :param task_id: ID of the task needed to add the blocker
    :type task_id: int
    :param db: session available to execute the operation
    :type db: Session
    :param current_user_id: ID of the user that wants to add the blocker
    :type current_user_id: int
    """
    use_case = CreateBlocker(
                user_repository=SqlAlchemyUserRepository(db),
                task_repository=SqlAlchemyTaskRepository(db),
                project_member_repository=SqlAlchemyProjectMemberRepository(db),
                blocker_repository=SqlAlchemyBlockerRepository(db),
                status_history_repository=SqlAlchemyTaskStatusHistoryRepository(db),
            )

    try:
        return use_case.execute(task_id=task_id, blocker_data=blocker, user_id=current_user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError:
        raise HTTPException(status_code=500, detail="Internal server error")
    
@router.get("/{task_id}/comments", response_model=list[CommentResponse], status_code=200)
def get_task_comments(task_id: int, 
                      db: Session = Depends(get_db), 
                      current_user_id: int=Depends(get_current_user_id)):
    use_case=GetComments(task_repo=SqlAlchemyTaskRepository(db),
                         project_member_repo=SqlAlchemyProjectMemberRepository(db),
                         comments_repo=SqlAlchemyCommentRepository(db),
                         user_repo=SqlAlchemyUserRepository(db))
    
    try:
        return use_case.execute(task_id=task_id, user_id=current_user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError:
        raise HTTPException(status_code=500, detail="Internal server error")
    
@router.get("/{task_id}/blockers", response_model=list[TaskBlockerResponse], status_code=200
)
def get_task_blockers(
    task_id: int,
    status: BlockerStatus | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user_id=Depends(get_current_user_id),
):
    use_case = GetTaskBlockersUseCase(blocker_repo=SqlAlchemyBlockerRepository(db),
                                      task_repo=SqlAlchemyTaskRepository(db),
                                      project_member_repo=SqlAlchemyProjectMemberRepository(db),
                                      user_repo=SqlAlchemyUserRepository(db))
    try:
        return use_case.execute(task_id=task_id, status=status, user_id=current_user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError:
        raise HTTPException(status_code=500, detail="Internal server error")
    
@router.get("/archived", response_model=list[TaskResponse], status_code=200)
def get_archived_tasks(project_id: int,
                       sprint_id: int | None = None, 
                       db:Session = Depends(get_db),
                       current_user_id: int = Depends(get_current_user_id)):
    """
    Docstring for get_archived_tasks
    
    :param project_id: Param to filter the tasks by the project they belong to
    :type project_id: int
    :param sprint_id: Optional param to filter tasks that belongs to a specified sprint
    :type sprint_id: int | None
    :param db: session available to execute the operation
    :type db: Session
    :param current_user_id: ID of the user that wants to execute the operation
    :type current_user_id: int
    """
    use_case=GetArchivedTask(task_repo=SqlAlchemyTaskRepository(db),
                             project_member_repo=SqlAlchemyProjectMemberRepository(db),
                             )
    try:
        return use_case.execute(project_id, sprint_id, current_user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError:
        raise HTTPException(status_code=500, detail="Internal server error")
    
@router.get("/{task_id}", response_model=TaskResponse, status_code=200)
def get_by_id(task_id: int,
              db: Session = Depends(get_db),
              current_user_id: int = Depends(get_current_user_id)):
    use_case=GetById(task_repo=SqlAlchemyTaskRepository(db),
                     user_repo=SqlAlchemyUserRepository(db),
                     project_member_repo=SqlAlchemyProjectMemberRepository(db))
    try:
        return use_case.execute(task_id=task_id, user_id=current_user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError:
        raise HTTPException(status_code=500, detail="Internal server error")
    
@router.put("/blocker/{blocker_id}", response_model=TaskBlockerResponse, status_code=201)
def update_blocker(blocker_id: int,
                   blocker: BlockerUpdate,
                   db: Session = Depends(get_db), 
                   current_user_id: int = Depends(get_current_user_id)):
    use_case=UpdateBlockerUseCase(blocker_repo=SqlAlchemyBlockerRepository(db),
                                  task_repo=SqlAlchemyTaskRepository(db),
                                  task_status_repo=SqlAlchemyTaskStatusHistoryRepository(db),
                                  user_repo=SqlAlchemyUserRepository(db),
                                  project_member_repo=SqlAlchemyProjectMemberRepository(db))
    try:
        return use_case.execute(blocker_id=blocker_id, blocker_data=blocker, user_id=current_user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError:
        raise HTTPException(status_code=500, detail="Internal server error")
    
@router.put("/comment/{comment_id}", response_model=CommentResponse, status_code=200)
def update_comment(comment_id: int, 
                   comment:CommentCreate, 
                   db:Session=Depends(get_db), 
                   current_user_id: int = Depends(get_current_user_id)):
    use_case=UpdateComment(comment_repo=SqlAlchemyCommentRepository(db),
                           user_repo=SqlAlchemyUserRepository(db))
    try:
        return use_case.execute(comment_id=comment_id, blocker_data=comment, user_id=current_user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError:
        raise HTTPException(status_code=500, detail="Internal server error")
    
@router.delete("/comment/{comment_id}")
def delete_comment(comment_id: int,
                   db: Session = Depends(get_db),
                   current_user_id: int = Depends(get_current_user_id)):
    use_case=DeleteComment(comment_repo=SqlAlchemyCommentRepository(db),
                           user_repo=SqlAlchemyUserRepository(db))
    try:
        use_case.execute(comment_id, current_user_id)
        return {"message": "Task Comment deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError:
        raise HTTPException(status_code=500, detail="Internal server error")
    