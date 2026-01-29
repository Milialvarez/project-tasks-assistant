from app.application.ports.task_comment_repository import CommentRepository
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.domain.entities.task_comment import TaskComment
from app.infrastructure.db.mappers.task_comment_mapper import to_domain, to_model

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