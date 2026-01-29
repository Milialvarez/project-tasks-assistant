from sqlalchemy import Column, Integer, DateTime, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.sql import func
from app.infrastructure.db.base import Base
from app.domain.enums import ProjectRole

class ProjectMember(Base):
    __tablename__ = "project_members"
    __table_args__ = (
        UniqueConstraint("project_id", "user_id"),
    )

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role = Column(Enum(ProjectRole), nullable=False)
    joined_at = Column(DateTime, nullable=False, server_default=func.now())
