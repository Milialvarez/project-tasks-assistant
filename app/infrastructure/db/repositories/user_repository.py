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

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def create(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def activate_user(self, user_id: int) -> None:
        user = self.db.query(User).filter(User.id == user_id).first()

        if not user:
            raise ValueError("User not found")

        user.active = True
        self.db.commit()

    def get_by_id(self, user_id: int):
        """
        Obtains an user by its ID
        """
        user = self.db.query(User).filter(User.id == user_id).first()
        return user