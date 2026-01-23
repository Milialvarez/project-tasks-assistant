from app.application.ports.task_repository import TaskRepository


class SqlAlchemyProjectRepository(TaskRepository):

    def __init__(self, db):
        self.db = db