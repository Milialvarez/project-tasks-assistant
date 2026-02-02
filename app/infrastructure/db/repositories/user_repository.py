from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.application.ports.user_repository import UserRepository
from app.domain.exceptions import PersistenceError, ResourceNotFoundError
from app.infrastructure.db.models.user import User as UserModel
from app.infrastructure.db.mappers.user_mapper import to_model, to_domain
from app.domain.entities.user import User

class SqlAlchemyUserRepository(UserRepository):

    def __init__(self, db: Session):
        self.db = db

    def exists(self, user_id: int) -> bool:
        return (
            self.db.query(UserModel)
            .filter(UserModel.id == user_id)
            .first()
            is not None
        )

    def get_by_email(self, email: str) -> User | None:
        model = (
            self.db.query(UserModel)
            .filter(UserModel.email == email)
            .first()
        )
        return to_domain(model) if model else None

    def create(self, user: User) -> User:
        try:
            model = to_model(user)
            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)
            return to_domain(model)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise PersistenceError("Failed to create user") from e


    def activate_user(self, user_id: int) -> None:
        model = self.db.query(UserModel).filter(UserModel.id == user_id).first()

        if not model:
            raise ResourceNotFoundError("User")

        model.active = True
        try:
            self.db.commit()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise PersistenceError("Failed to activate user") from e

    def get_by_id(self, user_id: int) -> User | None:
        model = (
            self.db.query(UserModel)
            .filter(UserModel.id == user_id)
            .first()
        )
        return to_domain(model) if model else None
