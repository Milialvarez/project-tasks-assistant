from typing import List
from app.application.ports.task_comment_repository import CommentRepository
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.domain.entities.task_comment import TaskComment
from app.infrastructure.db.mappers.task_comment_mapper import to_domain, to_model
from app.infrastructure.db.models.task_comment import TaskComment as TaskCommentModel

class SqlAlchemyCommentRepository(CommentRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, comment: TaskComment) -> TaskComment:
        try:
            model = to_model(comment)
            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)
            return to_domain(model)
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def get_comments(self, task_id: int)->List[TaskComment]:
        query = self.db.query(TaskCommentModel)
        query = query.filter(TaskCommentModel.task_id == task_id)
        return [to_domain(model) for model in query.all()]