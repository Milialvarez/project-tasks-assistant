from app.domain.entities.task_comment import TaskComment
from app.infrastructure.db.models.task_comment import TaskComment as TaskCommentModel

def to_domain(model: TaskCommentModel) -> TaskComment:
    return TaskComment(
        id=model.id,
        task_id=model.task_id,
        user_id=model.user_id,
        content=model.content,
        created_at=model.created_at,
    )

def to_model(entity: TaskComment) -> TaskCommentModel:
    return TaskCommentModel(
        id=entity.id,
        task_id=entity.task_id,
        user_id=entity.user_id,
        content=entity.content,
    )
