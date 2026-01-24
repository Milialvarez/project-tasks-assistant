from app.application.ports.task_repository import TaskRepository
from app.infrastructure.db.models.task import Task

class SqlAlchemyTaskRepository(TaskRepository):

    def __init__(self, db):
        self.db = db

    def create(self, task: Task) -> Task:
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def filter(
        self,
        *,
        project_id: int | None = None,
        sprint_id: int | None = None,
        assigned_user_id: int | None = None,
    ):
        query = self.db.query(Task)

        if project_id is not None:
            query = query.filter(Task.project_id == project_id)

        if sprint_id is not None:
            query = query.filter(Task.sprint_id == sprint_id)

        if assigned_user_id is not None:
            query = query.filter(Task.assigned_user_id == assigned_user_id)

        return query.all()