from app.application.ports.sprint_repository import SprintRepository
from app.infrastructure.db.models.sprint import Sprint
from sqlalchemy.exc import SQLAlchemyError

class SqlAlchemySprintRepository(SprintRepository):
    def __init__(self, db):
        self.db = db

    def create(self, sprint: Sprint):
        try:
            self.db.add(sprint)
            self.db.commit()
            self.db.refresh(sprint)
            return sprint
        except SQLAlchemyError as e:
            self.db.rollback()
            raise