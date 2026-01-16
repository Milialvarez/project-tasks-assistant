from sqlalchemy.orm import Session
from app.application.ports.user_repository import UserRepository
from app.infrastructure.db.models.user import User


class SqlAlchemyUserRepository(UserRepository):

    def __init__(self, db: Session):
        self.db = db

    def exists(self, user_id: int) -> bool:
        return (
            self.db.query(User)
            .filter(User.id == user_id)
            .first()
            is not None
        )
