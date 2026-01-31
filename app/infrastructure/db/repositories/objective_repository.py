from app.application.ports.objective_repository import ObjectiveRepository
from app.domain.entities.objective import Objective
from app.infrastructure.db.mappers.objective_mapper import to_domain, to_model
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError


class SqlAlchemyObjectiveRepository(ObjectiveRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, objective: Objective)->Objective:
        try:
            model = to_model(objective)
            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)
            return to_domain(model)
        except SQLAlchemyError:
            self.db.rollback()
            raise
