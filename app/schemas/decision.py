from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class DecisionCreate(BaseModel):
    project_id: int
    task_id: Optional[int] = None
    title: str
    context: str
    impact: Optional[str] = None

class DecisionUpdate(BaseModel):
    title: Optional[str] = None
    context: Optional[str] = None
    impact: Optional[str] = None

class DecisionResponse(BaseModel):
    id: int
    project_id: int
    task_id: Optional[int]
    title: str
    context: str
    impact: Optional[str]
    chosen_by: int
    created_at: datetime

    class Config:
        from_attributes = True
