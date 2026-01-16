from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.infrastructure.db.base import Base

# model for project schema, represents a real life project
class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    creator = relationship("User")
