from app.domain.entities.project_invitation import ProjectInvitation
from app.infrastructure.db.models.project_invitation import ProjectInvitation as ProjectInvitationModel

def to_domain(model: ProjectInvitationModel) -> ProjectInvitation:
    return ProjectInvitation(
        id=model.id,
        project_id=model.project_id,
        invited_user_id=model.invited_user_id,
        status=model.status,
        expires_at=model.expires_at,
        created_at=model.created_at,
    )

def to_model(entity: ProjectInvitation) -> ProjectInvitationModel:
    return ProjectInvitationModel(
        id=entity.id,
        project_id=entity.project_id,
        invited_user_id=entity.invited_user_id,
        status=entity.status,
        expires_at=entity.expires_at,
    )
