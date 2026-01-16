from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.infrastructure.db.base import Base

class TaskComment(Base):
    __tablename__ = "task_comment"

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("task.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
