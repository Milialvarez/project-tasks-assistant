from typing import List
from app.application.ports.objective_repository import ObjectiveRepository
from app.domain.entities.objective import Objective
from app.domain.exceptions import PersistenceError, ResourceNotFoundError
from app.infrastructure.db.mappers.objective_mapper import to_domain, to_model
from app.infrastructure.db.models.objective import Objective as ObjectiveModel
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
        except SQLAlchemyError as e:
            self.db.rollback()
            raise PersistenceError("Database error") from e

    def get_by_id(self, objective_id: int) -> Objective | None:
        model = self.db.query(ObjectiveModel).filter(ObjectiveModel.id == objective_id).first()
        if model is None:
            return None
        return to_domain(model) if model else None
    
    def update(self, objective: Objective)->Objective:
        model = self.db.query(ObjectiveModel).get(objective.id)
        if not model:
            raise ResourceNotFoundError("Objective not found")

        model.title = objective.title
        model.description = objective.description
        model.status = objective.status
        model.sprint_id = objective.sprint_id

        try:
            self.db.commit()
            self.db.refresh(model)
            return to_domain(model)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise PersistenceError("Database error") from e

    def delete(self, objective_id: int)-> None:
        model = self.db.query(ObjectiveModel).get(objective_id)
        if not model:
            raise ValueError("Objective not found")

        try:
            self.db.delete(model)
            self.db.commit()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise PersistenceError("Database error") from e

    def get(self, project_id: int | None, sprint_id: int | None)->List[Objective]:
        query = self.db.query(ObjectiveModel)

        if sprint_id is not None:
            query = query.filter(ObjectiveModel.sprint_id == sprint_id)
        if project_id is not None:
            query = query.filter(ObjectiveModel.project_id == project_id)

        return [to_domain(model) for model in query.all()]