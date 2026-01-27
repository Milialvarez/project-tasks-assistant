from app.application.ports.sprint_repository import SprintRepository
from sqlalchemy.exc import SQLAlchemyError
from app.infrastructure.db.mappers.sprint_mapper import to_domain, to_model

from app.domain.entities.sprint import Sprint

class SqlAlchemySprintRepository(SprintRepository):
    def __init__(self, db):
        self.db = db

    def create(self, sprint: Sprint):
        try:
            model = to_model(sprint)
            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)
            return to_domain(model)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise

    def get_by_id(self, sprint_id: int):
        sprint = self.db.query(Sprint).filter(Sprint.id == sprint_id).first()
        return to_domain(sprint)

    def update(self, sprint: Sprint):
        try:
            model = to_model(sprint)
            self.db.commit()
            self.db.refresh(model)
            return to_domain(model)
        except SQLAlchemyError:
            self.db.rollback()
            raise
