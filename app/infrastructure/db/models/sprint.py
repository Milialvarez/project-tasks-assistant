from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from app.infrastructure.db.base import Base
from app.infrastructure.db.enums import SprintStatus

class Sprint(Base):
    __tablename__ = "sprint"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    started_at = Column(DateTime)
    ended_at = Column(DateTime)
    status = Column(Enum(SprintStatus), nullable=False)