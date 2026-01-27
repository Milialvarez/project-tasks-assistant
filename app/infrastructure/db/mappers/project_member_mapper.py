from app.domain.entities.project_member import ProjectMember
from app.infrastructure.db.models.project_member import ProjectMember as ProjectMemberModel

def to_domain(model: ProjectMemberModel) -> ProjectMember:
    return ProjectMember(
        id=model.id,
        project_id=model.project_id,
        user_id=model.user_id,
        role=model.role,
        joined_at=model.joined_at,
    )

def to_model(entity: ProjectMember) -> ProjectMemberModel:
    return ProjectMemberModel(
        id=entity.id,
        project_id=entity.project_id,
        user_id=entity.user_id,
        role=entity.role,
    )
