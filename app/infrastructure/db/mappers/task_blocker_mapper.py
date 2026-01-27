from app.domain.entities.task_blocker import TaskBlocker
from app.infrastructure.db.models.task_blocker import TaskBlocker as TaskBlockerModel

def to_domain(model: TaskBlockerModel) -> TaskBlocker:
    return TaskBlocker(
        id=model.id,
        task_id=model.task_id,
        cause=model.cause,
        created_by=model.created_by,
        status=model.status,
        start_date=model.start_date,
        solved_at=model.solved_at,
    )

def to_model(entity: TaskBlocker) -> TaskBlockerModel:
    return TaskBlockerModel(
        id=entity.id,
        task_id=entity.task_id,
        cause=entity.cause,
        created_by=entity.created_by,
        status=entity.status,
        solved_at=entity.solved_at,
    )
