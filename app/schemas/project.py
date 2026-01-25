from abc import ABC


class ProjectCreate(ABC):
    name: str
    description: str | None

class ProjectUpdate(ABC):
    project_id: int
    name: str | None
    description: str | None