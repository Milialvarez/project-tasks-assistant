from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.application.ports.task_repository import TaskRepository
from app.domain.entities.task import Task
from app.infrastructure.db.models.task import Task as TaskModel
from app.infrastructure.db.mappers.task_mapper import to_domain, to_model


class SqlAlchemyTaskRepository(TaskRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, task: Task) -> Task:
        try:
            model = to_model(task)
            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)
            return to_domain(model)
        except SQLAlchemyError:
            self.db.rollback()
            raise
        
    def get_by_id(self, task_id: int) -> Task | None:
        model = self.db.query(TaskModel).filter(TaskModel.id == task_id).first()
        if model is None:
            return None
        return to_domain(model) if model else None

    def filter(self, *, project_id, sprint_id, assigned_user_id)-> List[Task]:
        query = self.db.query(TaskModel)

        query = query.filter(TaskModel.project_id == project_id)
        query= query.filter(TaskModel.archived == False)

        if sprint_id is not None:
            query = query.filter(TaskModel.sprint_id == sprint_id)

        if assigned_user_id is not None:
            query = query.filter(TaskModel.assigned_user_id == assigned_user_id)

        return [to_domain(model) for model in query.all()]

    def update(self, task: Task) -> Task:
        model = self.db.query(TaskModel).get(task.id)
        if not model:
            raise ValueError("Task not found")

        model.title = task.title
        model.description = task.description
        model.sprint_id = task.sprint_id
        model.assigned_user_id = task.assigned_user_id
        model.current_status = task.current_status
        model.archived = task.archived

        try:
            self.db.commit()
            self.db.refresh(model)
            return to_domain(model)
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def delete(self, task_id: int) -> None:
        model = self.db.query(TaskModel).get(task_id)
        if not model:
            raise ValueError("Task not found")

        try:
            self.db.delete(model)
            self.db.commit()
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def get_archived(self, project_id: int, sprint_id: int | None) -> List[Task]:
        query = self.db.query(TaskModel)

        query = query.filter(TaskModel.project_id == project_id)
        query= query.filter(TaskModel.archived == True)

        if sprint_id is not None:
            query = query.filter(TaskModel.sprint_id == sprint_id)

        return [to_domain(model) for model in query.all()]