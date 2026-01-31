from app.application.ports.sprint_repository import SprintRepository
from sqlalchemy.exc import SQLAlchemyError
from app.domain.entities.sprint import Sprint
from app.infrastructure.db.models.sprint import Sprint as SprintModel
from app.infrastructure.db.mappers.sprint_mapper import to_domain, to_model

class SqlAlchemySprintRepository(SprintRepository):
    def __init__(self, db):
        self.db = db

    def create(self, sprint: Sprint):
        try:
            model = to_model(sprint)
            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)
            return to_domain(model)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise

    def get_by_id(self, sprint_id: int):
        sprint = self.db.query(SprintModel).filter(SprintModel.id == sprint_id).first()
        if sprint is None:
            return None
        return to_domain(sprint)

    def update(self, sprint: Sprint) -> Sprint:
        try:
            model = (
                self.db
                .query(SprintModel)
                .filter(SprintModel.id == sprint.id)
                .first()
            )

            if not model:
                raise ValueError("Sprint not found")

            model.name = sprint.name
            model.description = sprint.description
            model.started_at = sprint.started_at
            model.ended_at = sprint.ended_at
            model.status = sprint.status

            self.db.commit()
            self.db.refresh(model)

            return to_domain(model)

        except SQLAlchemyError:
            self.db.rollback()
            raise

    def get_sprints_by_project_id(self, project_id):
        sprints = (
            self.db.query(SprintModel)
            .filter(SprintModel.project_id == project_id)
            .all()
        )
        return [to_domain(s) for s in sprints]