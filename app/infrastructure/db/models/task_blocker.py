from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from app.infrastructure.db.base import Base
from app.domain.enums import BlockerStatus

class TaskBlocker(Base):
    __tablename__ = "task_blocker"

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("task.id"), nullable=False)
    cause = Column(Text, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(Enum(BlockerStatus), nullable=False)
    start_date = Column(DateTime, nullable=False, server_default=func.now())
    solved_at = Column(DateTime)
