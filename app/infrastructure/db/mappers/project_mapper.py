from app.domain.entities.project import Project
from app.infrastructure.db.models.project import Project as ProjectModel

def to_domain(model: ProjectModel) -> Project:
    return Project(
        id=model.id,
        name=model.name,
        description=model.description,
        created_by=model.created_by,
        created_at=model.created_at,
    )

def to_model(entity: Project) -> ProjectModel:
    return ProjectModel(
        id=entity.id,
        name=entity.name,
        description=entity.description,
        created_by=entity.created_by,
    )
