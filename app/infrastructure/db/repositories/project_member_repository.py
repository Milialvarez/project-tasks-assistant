from app.application.ports.project_member_repository import ProjectMemberRepository
from app.domain.exceptions import PersistenceError
from app.infrastructure.db.models.project_member import ProjectMember as Model
from app.infrastructure.db.mappers.project_member_mapper import to_model
from sqlalchemy.exc import SQLAlchemyError

class SqlAlchemyProjectMemberRepository(ProjectMemberRepository):

    def __init__(self, db):
        self.db = db

    def add_member(self, member):
        try:
            model = to_model(member)
            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)
            return member
        except SQLAlchemyError as e:
            self.db.rollback()
            raise PersistenceError("Database error") from e

    def is_member(self, project_id: int, user_id: int) -> bool:
        return (
            self.db.query(Model)
            .filter(Model.project_id == project_id, Model.user_id == user_id)
            .first()
            is not None
        )
