from sqlalchemy import Column, Integer, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from app.infrastructure.db.base import Base
from app.domain.enums import TaskStatus

class TaskStatusHistory(Base):
    __tablename__ = "task_status_history"

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("task.id", ondelete="CASCADE"), nullable=False)
    previous_status = Column(Enum(TaskStatus), nullable=False)
    new_status = Column(Enum(TaskStatus), nullable=False)
    changed_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    changed_at = Column(DateTime, nullable=False, server_default=func.now())
