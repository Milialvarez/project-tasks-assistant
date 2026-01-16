from app.application.ports.project_repository import ProjectRepository
from app.infrastructure.db.models.project import Project

class SqlAlchemyProjectRepository(ProjectRepository):

    def __init__(self, db):
        self.db = db

    def create(self, project: Project):
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project
