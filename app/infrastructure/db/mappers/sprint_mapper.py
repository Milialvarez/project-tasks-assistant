from app.domain.entities.sprint import Sprint
from app.infrastructure.db.models.sprint import Sprint as SprintModel

def to_domain(model: SprintModel) -> Sprint:
    return Sprint(
        id=model.id,
        project_id=model.project_id,
        name=model.name,
        description=model.description,
        started_at=model.started_at,
        ended_at=model.ended_at,
        status=model.status,
    )

def to_model(entity: Sprint) -> SprintModel:
    return SprintModel(
        id=entity.id,
        project_id=entity.project_id,
        name=entity.name,
        description=entity.description,
        started_at=entity.started_at,
        ended_at=entity.ended_at,
        status=entity.status,
    )
