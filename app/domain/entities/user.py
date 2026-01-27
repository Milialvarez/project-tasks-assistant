from datetime import datetime

class User:
    def __init__(
        self,
        *,
        id: int | None,
        email: str,
        password_hash: str,
        name: str,
        active: bool,
        created_at: datetime | None = None,
    ):
        self.id = id
        self.email = email
        self.password_hash = password_hash
        self.name = name
        self.active = active
        self.created_at = created_at