from app.application.ports.project_repository import ProjectRepository
from app.domain.exceptions import PersistenceError
from app.infrastructure.db.models.project import Project as Model
from app.infrastructure.db.models.project_member import ProjectMember
from app.infrastructure.db.mappers.project_mapper import to_domain, to_model
from sqlalchemy.exc import SQLAlchemyError
class SqlAlchemyProjectRepository(ProjectRepository):

    def __init__(self, db):
        self.db = db

    def create(self, project):
        try:
            model = to_model(project)
            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)
            return to_domain(model)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise PersistenceError("Database error") from e

    def update(self, project):
        try:
            model = self.db.query(Model).get(project.id)
            model.name = project.name
            model.description = project.description
            self.db.commit()
            self.db.refresh(model)
            return to_domain(model)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise PersistenceError("Database error") from e

    def get_projects_for_user(self, user_id: int):
        projects = (
            self.db.query(Model)
            .join(ProjectMember, ProjectMember.project_id == Model.id)
            .filter(ProjectMember.user_id == user_id)
            .all()
        )
        return [to_domain(p) for p in projects]

    def get_by_id(self, project_id: int):
        model = self.db.query(Model).filter(Model.id == project_id).first()
        if model is None:
            return None
        return to_domain(model) if model else None

    def delete(self, project):
        try:
            model = self.db.query(Model).get(project.id)
            self.db.delete(model)
            self.db.commit()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise PersistenceError("Database error") from e

    def is_manager(self, project_id: int, user_id: int) -> bool:
        return (
            self.db.query(Model)
            .filter(Model.id == project_id, Model.created_by == user_id)
            .first()
            is not None
        )
