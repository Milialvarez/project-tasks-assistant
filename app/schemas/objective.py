
from pydantic import BaseModel
from app.domain.enums import ObjectiveStatus

class ObjectiveCreate(BaseModel):
    project_id: int
    sprint_id: int | None = None
    title: str
    description: str | None = None

class ObjectiveResponse(BaseModel):
    id: int
    project_id: int
    sprint_id: int | None = None
    title: str
    description: str | None = None
    status: ObjectiveStatus

    class Config:
        from_attributes = True  