from app.application.ports.task_blocker_repository import BlockerRepository
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.domain.entities.task_blocker import TaskBlocker
from app.infrastructure.db.mappers.task_blocker_mapper import to_domain, to_model

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
        except SQLAlchemyError:
            self.db.rollback()
            raise