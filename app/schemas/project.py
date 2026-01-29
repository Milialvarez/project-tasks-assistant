from abc import ABC
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ProjectCreate(BaseModel):
    name: str
    description: str | None

class ProjectUpdate(BaseModel):
    name: str | None
    description: str | None

class ProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_by: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }