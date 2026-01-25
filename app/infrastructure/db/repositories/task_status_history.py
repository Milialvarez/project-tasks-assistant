from sqlalchemy.orm import Session
from app.application.ports.task_status_history_repository import TaskStatusHistoryRepository
from app.infrastructure.db.models.task_status_history import TaskStatusHistory
from sqlalchemy.exc import SQLAlchemyError


class SqlAlchemyTaskStatusHistoryRepository(TaskStatusHistoryRepository):

    def __init__(self, db: Session):
        self.db = db

    def create(self, history: TaskStatusHistory):
        try:
            self.db.add(history)
            self.db.commit()
            self.db.refresh(history)
            return history
        except SQLAlchemyError as e:
            self.db.rollback()
            raise
