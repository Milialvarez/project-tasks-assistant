from app.domain.entities.decision import Decision
from app.infrastructure.db.models.decision import Decision as DecisionModel

def to_domain(model: DecisionModel) -> Decision:
    return Decision(
        id=model.id,
        project_id=model.project_id,
        task_id=model.task_id,
        title=model.title,
        context=model.context,
        impact=model.impact,
        chosen_by=model.chosen_by,
        created_at=model.created_at,
    )

def to_model(entity: Decision) -> DecisionModel:
    return DecisionModel(
        id=entity.id,
        project_id=entity.project_id,
        task_id=entity.task_id,
        title=entity.title,
        context=entity.context,
        impact=entity.impact,
        chosen_by=entity.chosen_by,
    )
