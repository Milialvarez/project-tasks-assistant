from sqlalchemy.orm import Session
from app.application.ports.task_status_history_repository import TaskStatusHistoryRepository
from sqlalchemy.exc import SQLAlchemyError
from app.infrastructure.db.mappers.task_status_history_mapper import to_model, to_domain

from app.domain.entities.task_status_history import TaskStatusHistory


class SqlAlchemyTaskStatusHistoryRepository(TaskStatusHistoryRepository):

    def __init__(self, db: Session):
        self.db = db

    def create(self, history: TaskStatusHistory):
        try:
            model = to_model(history)
            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)
            return to_domain(model)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise

    def get_by_task_id(self, task_id: int) -> list[TaskStatusHistory]:
        return (
            self.db.query(TaskStatusHistory)
            .filter(TaskStatusHistory.task_id == task_id)
            .order_by(TaskStatusHistory.created_at.asc())
            .all()
        )
