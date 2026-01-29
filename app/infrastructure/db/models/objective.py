from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum
from app.infrastructure.db.base import Base
from app.domain.enums import ObjectiveStatus

class Objective(Base):
    __tablename__ = "objective"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    sprint_id = Column(Integer, ForeignKey("sprint.id", ondelete="CASCADE"))
    title = Column(String(150), nullable=False)
    description = Column(Text)
    status = Column(Enum(ObjectiveStatus), nullable=False)
