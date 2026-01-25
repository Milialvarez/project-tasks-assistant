from app.application.ports.project_invitation_repository import ProjectInvitationRepository
from app.infrastructure.db.enums import InvitationStatus


class RejectProjectInvitationUseCase:
    def __init__(self, invitation_repo: ProjectInvitationRepository):
        self.invitation_repo = invitation_repo

    def execute(self, invitation_id: int):
        invitation = self.invitation_repo.get_by_id(invitation_id)

        if not invitation:
            raise ValueError("Invitation not found")

        invitation.status = InvitationStatus.rejected
        self.invitation_repo.update(invitation)
