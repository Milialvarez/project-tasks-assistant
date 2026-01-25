from app.application.ports.project_invitation_repository import ProjectInvitationRepository
from app.infrastructure.db.models.project_invitation import ProjectInvitation
from app.infrastructure.db.enums import InvitationStatus

class SqlAlchemyProjectInvitationRepository(ProjectInvitationRepository):

    def __init__(self, db):
        self.db = db

    def create(self, invitation: ProjectInvitation) -> ProjectInvitation:
        self.db.add(invitation)
        self.db.commit()
        self.db.refresh(invitation)
        return invitation

    def get_pending(self, project_id: int, user_id: int):
        return (
            self.db.query(ProjectInvitation)
            .filter(
                ProjectInvitation.project_id == project_id,
                ProjectInvitation.invited_user_id == user_id,
                ProjectInvitation.status == InvitationStatus.pending,
            )
            .first()
        )

    def get_by_id(self, invitation_id: int):
        return (
            self.db.query(ProjectInvitation)
            .filter(ProjectInvitation.id == invitation_id)
            .first()
        )

    def update(self, invitation: ProjectInvitation):
        self.db.add(invitation)
        self.db.commit()
        self.db.refresh(invitation)
        return invitation
