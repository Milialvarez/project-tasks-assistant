# domain/entities/project_invitation.py
from datetime import datetime
from app.domain.enums import InvitationStatus

class ProjectInvitation:
    def __init__(
        self,
        *,
        id: int | None,
        project_id: int,
        invited_user_id: int,
        status: InvitationStatus,
        expires_at: datetime,
        created_at: datetime | None = None,
    ):
        self.id = id
        self.project_id = project_id
        self.invited_user_id = invited_user_id
        self.status = status
        self.expires_at = expires_at
        self.created_at = created_at
