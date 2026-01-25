from app.application.ports.project_member_repository import ProjectMemberRepository
from app.infrastructure.db.models.project_member import ProjectMember
from sqlalchemy.exc import SQLAlchemyError

class SqlAlchemyProjectMemberRepository(ProjectMemberRepository):

    def __init__(self, db):
        self.db = db

    def add_member(self, member: ProjectMember) -> ProjectMember:
        try:
            self.db.add(member)
            self.db.commit()
            self.db.refresh(member)
            return member
        except SQLAlchemyError as e:
            self.db.rollback()
            raise