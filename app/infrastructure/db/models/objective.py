from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum
from app.infrastructure.db.base import Base
from app.infrastructure.db.enums import ObjectiveStatus

class Objective(Base):
    __tablename__ = "objective"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    sprint_id = Column(Integer, ForeignKey("sprint.id"))
    title = Column(String(150), nullable=False)
    description = Column(Text)
    status = Column(Enum(ObjectiveStatus), nullable=False)
