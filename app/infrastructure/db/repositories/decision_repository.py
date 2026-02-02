from typing import List, Optional
from app.application.ports.decision_repository import DecisionRepository
from app.domain.entities.decision import Decision
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app.domain.exceptions import EntityAlreadyExistsError, PersistenceError
from app.infrastructure.db.models.decision import Decision as DecisionModel
from app.infrastructure.db.mappers.decision_mapper import to_domain, to_model


class SqlAlchemyDecisionRepository(DecisionRepository):

    def __init__(self, db: Session):
        self.db = db

    def create(self, decision: Decision) -> Decision:
        try:
            model = to_model(decision)
            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)
            return to_domain(model)
        except IntegrityError as e:
            self.db.rollback()
            raise EntityAlreadyExistsError("Decision already exists") from e
        except SQLAlchemyError as e:
            self.db.rollback()
            raise PersistenceError("Database error") from e

    def update(self, decision: Decision) -> Decision:
        model = self.db.query(DecisionModel).get(decision.id)
        if not model:
            raise ValueError("Objective not found")

        model.title = decision.title
        model.context = decision.context
        model.impact = decision.impact

        try:
            self.db.commit()
            self.db.refresh(model)
            return to_domain(model)
        except SQLAlchemyError:
            self.db.rollback()
            raise


    def delete(self, decision: Decision) -> None:
        model = self.db.query(DecisionModel).get(decision.id)
        if not model:
            raise ValueError("Decision not found")

        try:
            self.db.delete(model)
            self.db.commit()
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def get_by_id(self, decision_id: int) -> Optional[Decision]:
        model = self.db.query(DecisionModel).filter(DecisionModel.id == decision_id).first()
        if model is None:
            return None
        return to_domain(model) if model else None

    def get_filtered(
        self,
        project_id: Optional[int],
        task_id: Optional[int],
    ) -> List[Decision]:

        query = self.db.query(DecisionModel)

        if task_id:
            query = query.filter(DecisionModel.task_id == task_id)
        else:
            query = query.filter(DecisionModel.project_id == project_id)

        return [to_domain(model) for model in query.order_by(DecisionModel.created_at.desc()).all()]
