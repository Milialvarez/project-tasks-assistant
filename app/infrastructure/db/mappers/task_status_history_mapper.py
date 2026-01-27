from app.domain.entities.task_status_history import TaskStatusHistory
from app.infrastructure.db.models.task_status_history import TaskStatusHistory as TaskStatusHistoryModel

def to_domain(model: TaskStatusHistoryModel) -> TaskStatusHistory:
    return TaskStatusHistory(
        id=model.id,
        task_id=model.task_id,
        previous_status=model.previous_status,
        new_status=model.new_status,
        changed_by=model.changed_by,
        changed_at=model.changed_at,
    )

def to_model(entity: TaskStatusHistory) -> TaskStatusHistoryModel:
    return TaskStatusHistoryModel(
        id=entity.id,
        task_id=entity.task_id,
        previous_status=entity.previous_status,
        new_status=entity.new_status,
        changed_by=entity.changed_by,
    )
