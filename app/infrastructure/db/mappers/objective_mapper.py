from app.domain.entities.objective import Objective
from app.infrastructure.db.models.objective import Objective as ObjectiveModel

def to_domain(model: ObjectiveModel) -> Objective:
    return Objective(
        id=model.id,
        project_id=model.project_id,
        sprint_id=model.sprint_id,
        title=model.title,
        description=model.description,
        status=model.status,
    )

def to_model(entity: Objective) -> ObjectiveModel:
    return ObjectiveModel(
        id=entity.id,
        project_id=entity.project_id,
        sprint_id=entity.sprint_id,
        title=entity.title,
        description=entity.description,
        status=entity.status,
    )
