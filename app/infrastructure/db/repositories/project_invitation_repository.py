from app.application.ports.project_invitation_repository import ProjectInvitationRepository
from app.infrastructure.db.models.project_invitation import ProjectInvitation as Model
from app.infrastructure.db.mappers.project_invitation_mapper import to_domain, to_model
from app.domain.enums import InvitationStatus

class SqlAlchemyProjectInvitationRepository(ProjectInvitationRepository):

    def __init__(self, db):
        self.db = db

    def create(self, invitation):
        model = to_model(invitation)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return to_domain(model)

    def get_pending(self, project_id: int, user_id: int):
        model = (
            self.db.query(Model)
            .filter(
                Model.project_id == project_id,
                Model.invited_user_id == user_id,
                Model.status == InvitationStatus.pending,
            )
            .first()
        )
        return to_domain(model) if model else None

    def get_by_id(self, invitation_id: int):
        model = self.db.query(Model).get(invitation_id)
        return to_domain(model) if model else None

    def update(self, invitation):
        model = self.db.query(Model).get(invitation.id)
        model.status = invitation.status
        self.db.commit()
        self.db.refresh(model)
        return to_domain(model)
