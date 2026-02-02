from typing import List
from app.application.ports.task_blocker_repository import BlockerRepository
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.domain.entities.task_blocker import TaskBlocker
from app.domain.enums import BlockerStatus
from app.domain.exceptions import PersistenceError, ResourceNotFoundError
from app.infrastructure.db.mappers.task_blocker_mapper import to_domain, to_model
from app.infrastructure.db.models.task_blocker import TaskBlocker as TaskBlockerModel

class SqlAlchemyBlockerRepository(BlockerRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, comment: TaskBlocker) -> TaskBlocker:
        try:
            model = to_model(comment)
            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)
            return to_domain(model)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise PersistenceError("Database error") from e

    def get_by_task_id(self, *, task_id: int, status: BlockerStatus | None = None) -> List[TaskBlocker]:

        query = self.db.query(TaskBlockerModel).filter(
            TaskBlockerModel.task_id == task_id
        )

        if status is not None:
            query = query.filter(TaskBlockerModel.status == status)

        blockers = query.all()

        return [to_domain(model) for model in blockers]
    
    def get_by_id(self, blocker_id:int) -> TaskBlocker | None:
        model = self.db.query(TaskBlockerModel).filter(TaskBlockerModel.id==blocker_id).first()
        if model is None:
            return None
        return to_domain(model) if model else None
    
    def update(self, blocker: TaskBlocker) -> TaskBlocker:
        model = self.db.query(TaskBlockerModel).get(blocker.id)
        if not model:
            raise ResourceNotFoundError("Task Blocker")

        try:
            model.cause = blocker.cause
            model.status = blocker.status
            model.solved_at = blocker.solved_at

            self.db.commit()
            self.db.refresh(model)
            return to_domain(model)

        except SQLAlchemyError as e:
            self.db.rollback()
            raise PersistenceError("Database error") from e
