from app.application.ports.project_invitation_repository import ProjectInvitationRepository
from app.domain.enums import InvitationStatus
from app.domain.exceptions import ResourceNotFoundError

class RejectProjectInvitationUseCase:
    def __init__(
            self, 
            invitation_repository: ProjectInvitationRepository
            ):
            self.invitation_repository = invitation_repository

    def execute(self, invitation_id: int, user_id: int):
        invitation = self.invitation_repository.get_by_id(invitation_id)

        if not invitation:
            raise ResourceNotFoundError("Invitation")

        if invitation.status != InvitationStatus.pending:
            raise ValueError("Invitation is no longer valid")

        if invitation.invited_user_id != user_id:
            raise ValueError("This invitation does not belong to you")

        invitation.status = InvitationStatus.rejected
        self.invitation_repository.update(invitation)
