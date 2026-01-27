from app.domain.entities.task import Task
from app.infrastructure.db.models.task import Task as TaskModel

def to_domain(model: TaskModel) -> Task:
    return Task(
        id=model.id,
        project_id=model.project_id,
        sprint_id=model.sprint_id,
        title=model.title,
        description=model.description,
        assigned_user_id=model.assigned_user_id,
        current_status=model.current_status,
        created_at=model.created_at,
        archived=model.archived,
    )

def to_model(entity: Task) -> TaskModel:
    return TaskModel(
        id=entity.id,
        project_id=entity.project_id,
        sprint_id=entity.sprint_id,
        title=entity.title,
        description=entity.description,
        assigned_user_id=entity.assigned_user_id,
        current_status=entity.current_status,
        archived=entity.archived,
    )
