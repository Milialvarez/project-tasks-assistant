from sqlalchemy import Column, Integer, DateTime, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.sql import func
from app.infrastructure.db.base import Base
from app.domain.enums import InvitationStatus

class ProjectInvitation(Base):
    __tablename__ = "projects_invitation"
    __table_args__ = (
        UniqueConstraint("project_id", "invited_user_id"),
    )

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    invited_user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    status = Column(Enum(InvitationStatus), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
