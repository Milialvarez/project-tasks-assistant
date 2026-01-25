from datetime import datetime, timedelta
from app.application.ports.project_invitation_repository import ProjectInvitationRepository
from app.application.ports.project_member_repository import ProjectMemberRepository
from app.application.ports.project_repository import ProjectRepository
from app.application.ports.user_repository import UserRepository
from app.infrastructure.db.models.project_invitation import ProjectInvitation
from app.infrastructure.db.enums import InvitationStatus
from app.infrastructure.services.email_service import EmailService

class InviteProjectMemberUseCase:
    def __init__(
        self,
        project_repo: ProjectRepository,
        user_repo: UserRepository,
        invitation_repo: ProjectInvitationRepository,
        member_repo: ProjectMemberRepository,
        email_service: EmailService,
    ):
        self.project_repo = project_repo
        self.user_repo = user_repo
        self.invitation_repo = invitation_repo
        self.member_repo = member_repo
        self.email_service = email_service

    def execute(
        self,
        *,
        project_id: int,
        invited_email: str,
        current_user_id: int,
    ):
        # validar manager
        if not self.project_repo.is_manager(project_id, current_user_id):
            raise ValueError("Only project managers can invite members")

        invited_user = self.user_repo.get_by_email(invited_email)
        if not invited_user:
            raise ValueError("User does not exist")

        if self.member_repo.is_member(project_id, invited_user.id):
            raise ValueError("User is already a project member")

        if self.invitation_repo.get_pending(project_id, invited_user.id):
            raise ValueError("Invitation already sent")

        invitation = ProjectInvitation(
            project_id=project_id,
            invited_user_id=invited_user.id,
            status=InvitationStatus.pending,
            expires_at=datetime.utcnow() + timedelta(days=7),
        )

        invitation = self.invitation_repo.create(invitation)

        self.email_service.send_project_invitation(
            to_email=invited_email,
            invitation_id=invitation.id,
        )

        return invitation
