from datetime import datetime

class ActivationToken:
    def __init__(
        self,
        *,
        id: int | None = None,
        user_id: int,
        token: str,
        expires_at: datetime,
    ):
        self.id = id
        self.user_id = user_id
        self.token = token
        self.expires_at = expires_at
