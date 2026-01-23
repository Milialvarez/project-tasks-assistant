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
