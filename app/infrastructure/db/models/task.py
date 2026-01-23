from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from app.infrastructure.db.base import Base
from app.infrastructure.db.enums import TaskStatus

class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False) # a task always belongs to a project
    sprint_id = Column(Integer, ForeignKey("sprint.id")) # not necessary a task belong to a sprint
    title = Column(String(150), nullable=False)
    description = Column(Text)
    assigned_user_id = Column(Integer, ForeignKey("users.id"))
    current_status = Column(Enum(TaskStatus), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    archived = Column(Boolean, nullable=False, default=False)
