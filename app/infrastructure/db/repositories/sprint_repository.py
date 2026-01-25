from app.application.ports.sprint_repository import SprintRepository
from app.infrastructure.db.models.sprint import Sprint


class SqlAlchemySprintRepository(SprintRepository):
    def __init__(self, db):
        self.db = db

    def create(self, sprint: Sprint):
        """
        Creates a project
        """
        self.db.add(sprint)
        self.db.commit()
        self.db.refresh(sprint)
        return sprint
