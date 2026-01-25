from datetime import datetime
from app.application.ports.project_invitation_repository import ProjectInvitationRepository
from app.application.ports.project_member_repository import ProjectMemberRepository
from app.infrastructure.db.enums import InvitationStatus, ProjectRole
from app.infrastructure.db.models.project_member import ProjectMember

class AcceptProjectInvitationUseCase:
    def __init__(self, invitation_repo: ProjectInvitationRepository, member_repo: ProjectMemberRepository):
        self.invitation_repo = invitation_repo
        self.member_repo = member_repo

    def execute(self, invitation_id: int, user_id: int):
        invitation = self.invitation_repo.get_by_id(invitation_id)

        if not invitation:
            raise ValueError("Invitation not found")

        if invitation.status != InvitationStatus.pending:
            raise ValueError("Invitation is no longer valid")

        if invitation.expires_at < datetime.utcnow():
            invitation.status = InvitationStatus.expired
            self.invitation_repo.update(invitation)
            raise ValueError("Invitation expired")

        member = ProjectMember(
            project_id=invitation.project_id,
            user_id=invitation.invited_user_id,
            role=ProjectRole.member,
        )

        self.member_repo.add_member(member)


        invitation.status = InvitationStatus.accepted
        self.invitation_repo.update(invitation)
