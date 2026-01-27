from datetime import datetime

class Project:
    def __init__(
        self,
        *,
        id: int | None,
        name: str,
        description: str | None,
        created_by: int,
        created_at: datetime | None = None,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.created_by = created_by
        self.created_at = created_at
