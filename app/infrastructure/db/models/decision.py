from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.infrastructure.db.base import Base

class Decision(Base):
    __tablename__ = "decisions"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    task_id = Column(Integer, ForeignKey("task.id", ondelete="CASCADE"))
    title = Column(String(150), nullable=False)
    context = Column(Text, nullable=False)
    impact = Column(Text)
    chosen_by = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
