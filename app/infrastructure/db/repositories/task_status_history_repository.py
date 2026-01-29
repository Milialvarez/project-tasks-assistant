from sqlalchemy.orm import Session
from app.application.ports.task_status_history_repository import TaskStatusHistoryRepository
from sqlalchemy.exc import SQLAlchemyError
from app.domain.entities.task_status_history import TaskStatusHistory
from app.infrastructure.db.mappers.task_status_history_mapper import to_model, to_domain
from app.infrastructure.db.models.task_status_history import TaskStatusHistory as TaskStatusHistoryModel


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
        tasks = (
            self.db.query(TaskStatusHistoryModel)
            .filter(TaskStatusHistoryModel.task_id == task_id)
            .order_by(TaskStatusHistoryModel.changed_at.asc())
            .all()
        )

        tasks_domain: list[TaskStatusHistory] = []

        for task in tasks:
            tasks_domain.append(to_domain(task))

        return tasks_domain
